"""Génère les deux séries simulées du TP carte u et recalcule tous les chiffres.
Usage : python3 -I gen_series.py <dossier_sortie>
Les séries sont SIMULÉES (loi de Poisson, graine fixée). Aucune donnée réelle."""
import sys, json, math
import numpy as np
from scipy import stats

OUT = sys.argv[1]
LAM0 = 0.040          # taux de défaillance de référence, par heure de marche (MTBF 25 h)
SHIFT = 2.0           # facteur de dérive à partir de la semaine W_SHIFT
W_SHIFT = 60
N1, NREF = 78, 52     # 78 semaines au total, phase I = semaines 1 à 52

def hours_series(rng, n):
    h = []
    for w in range(1, n + 1):
        r = rng.random()
        if w in (17, 18, 35, 51, 52, 53, 70):   # semaines d'arrêt ou de jours fériés
            h.append(int(rng.choice([40, 56])))
        elif r < 0.62:
            h.append(80)
        elif r < 0.90:
            h.append(120)
        else:
            h.append(56)
    return np.array(h)

def u_limits(ubar, n):
    ucl = ubar + 3 * np.sqrt(ubar / n)
    lcl = np.maximum(0.0, ubar - 3 * np.sqrt(ubar / n))
    return lcl, ucl

def longest_run_same_side(x, centre):
    side = np.sign(x - centre); best = cur = 0; prev = 0
    for s in side:
        if s != 0 and s == prev: cur += 1
        elif s != 0: cur = 1
        else: cur = 0
        prev = s if s != 0 else prev
        best = max(best, cur)
    return best

def longest_monotone(x):
    best = up = dn = 1
    for i in range(1, len(x)):
        up = up + 1 if x[i] > x[i-1] else 1
        dn = dn + 1 if x[i] < x[i-1] else 1
        best = max(best, up, dn)
    return best

def make_series1(seed):
    rng = np.random.default_rng(seed)
    h = hours_series(rng, N1)
    lam = np.where(np.arange(1, N1 + 1) >= W_SHIFT, LAM0 * SHIFT, LAM0)
    n = rng.poisson(lam * h)
    return h, n

def evaluate1(h, n):
    ref = slice(0, NREF)
    ubar = n[ref].sum() / h[ref].sum()
    lcl, ucl = u_limits(ubar, h)
    u = n / h
    out_ref = [(i + 1) for i in range(NREF) if u[i] > ucl[i]]
    out_all = [(i + 1) for i in range(N1) if u[i] > ucl[i] and i >= NREF]
    cbar = n[ref].mean(); ccl = cbar + 3 * math.sqrt(cbar)
    c_out_ref = [(i + 1) for i in range(NREF) if n[i] > ccl]
    run = longest_run_same_side(u[ref], ubar)
    mono = longest_monotone(u[ref])
    return dict(ubar=ubar, ucl=ucl, lcl=lcl, u=u, out_ref=out_ref, out_ii=out_all,
                cbar=cbar, ccl=ccl, c_out_ref=c_out_ref, run=run, mono=mono)

chosen1 = None
for seed in range(1, 5000):
    h, n = make_series1(seed)
    e = evaluate1(h, n)
    if (not e['out_ref'] and e['run'] <= 6 and e['mono'] <= 4
            and len(e['c_out_ref']) >= 1 and all(h[i-1] == 120 for i in e['c_out_ref'])
            and e['out_ii'] and 63 <= e['out_ii'][0] <= 66
            and all(w >= W_SHIFT for w in e['out_ii'])):
        chosen1 = (seed, h, n, e); break
assert chosen1, "aucune graine adaptée (série 1)"
seed1, h1, n1, e1 = chosen1

# ---------------- série 2 : parc de 6 presses, taux variable d'une semaine à l'autre
def make_series2(seed, cv=0.30):
    rng = np.random.default_rng(seed)
    weeks = 52
    h = rng.choice([420, 480, 540, 360], size=weeks, p=[0.25, 0.5, 0.15, 0.10])
    lam_w = LAM0 * rng.gamma(shape=1 / cv**2, scale=cv**2, size=weeks)
    n = rng.poisson(lam_w * h)
    return h, n

def laney_u(h, n):
    ubar = n.sum() / h.sum(); u = n / h
    z = (u - ubar) / np.sqrt(ubar / h)
    mr = np.abs(np.diff(z)).mean(); sz = mr / 1.128
    ucl = ubar + 3 * sz * np.sqrt(ubar / h)
    lcl = np.maximum(0.0, ubar - 3 * sz * np.sqrt(ubar / h))
    return ubar, sz, lcl, ucl

def evaluate2(h, n):
    ubar = n.sum() / h.sum(); u = n / h
    lcl, ucl = u_limits(ubar, h)
    out_u = [i + 1 for i in range(len(h)) if u[i] > ucl[i] or u[i] < lcl[i]]
    X2 = float(((n - h * ubar) ** 2 / (h * ubar)).sum()); ddl = len(h) - 1
    p = float(stats.chi2.sf(X2, ddl))
    ub, sz, l2, ucl2 = laney_u(h, n)
    out_l = [i + 1 for i in range(len(h)) if u[i] > ucl2[i] or u[i] < l2[i]]
    return dict(ubar=ubar, out_u=out_u, X2=X2, ddl=ddl, p=p, sz=sz, out_l=out_l,
                ucl=ucl, lcl=lcl, ucl2=ucl2, lcl2=l2, u=u)

chosen2 = None
for seed in range(1, 5000):
    h, n = make_series2(seed)
    e = evaluate2(h, n)
    if 4 <= len(e['out_u']) <= 7 and len(e['out_l']) == 0 and 1.4 <= e['sz'] <= 1.9 and e['p'] < 1e-4 \
       and longest_run_same_side(e['u'], e['ubar']) <= 6:
        chosen2 = (seed, h, n, e); break
assert chosen2, "aucune graine adaptée (série 2)"
seed2, h2, n2, e2 = chosen2

# ---------------- MTBF / taux avec intervalle de Poisson exact (khi-deux)
def poisson_ci(N, T, conf=0.95):
    a = 1 - conf
    lo = stats.chi2.ppf(a / 2, 2 * N) / (2 * T) if N > 0 else 0.0
    hi = stats.chi2.ppf(1 - a / 2, 2 * N + 2) / (2 * T)
    return lo, hi

def rate_block(hh, nn):
    N, T = int(nn.sum()), float(hh.sum())
    lam = N / T; lo, hi = poisson_ci(N, T)
    return dict(N=N, T=T, lam=lam, lo=lo, hi=hi, mtbf=1 / lam, mtbf_lo=1 / hi, mtbf_hi=1 / lo)

pre = rate_block(h1[:NREF], n1[:NREF])
pre_late = rate_block(h1[NREF:W_SHIFT - 1], n1[NREF:W_SHIFT - 1])
post = rate_block(h1[W_SHIFT - 1:], n1[W_SHIFT - 1:])

# vérification indépendante de l'intervalle exact : bornes telles que P(X>=N|lo)=a/2 et P(X<=N|hi)=a/2
def check_ci(N, T, lo, hi):
    return (abs(stats.poisson.sf(N - 1, lo * T) - 0.025) < 1e-6, abs(stats.poisson.cdf(N, hi * T) - 0.025) < 1e-6)
assert all(check_ci(pre['N'], pre['T'], pre['lo'], pre['hi']))
assert all(check_ci(post['N'], post['T'], post['lo'], post['hi']))

# ---------------- ARL théorique à 100 h de marche par semaine (carte u, règle 1 seule)
def arl_table(ubar, hrs=80):
    ucl = ubar + 3 * math.sqrt(ubar / hrs)
    kmax = math.floor(ucl * hrs)          # alarme si N > kmax
    rows = []
    for ratio in (1.0, 1.5, 2.0, 3.0):
        p = stats.poisson.sf(kmax, ratio * ubar * hrs)
        rows.append((ratio, float(p), float(1 / p)))
    return kmax, rows
kmax80, arl80 = arl_table(e1['ubar'], 80)
kmax120, arl120 = arl_table(e1['ubar'], 120)

res = dict(
    seed1=seed1, seed2=seed2, LAM0=LAM0, SHIFT=SHIFT, W_SHIFT=W_SHIFT, NREF=NREF,
    s1=dict(ubar=e1['ubar'], cbar=e1['cbar'], ccl=e1['ccl'], c_out_ref=e1['c_out_ref'], out_ii=e1['out_ii'],
            run=e1['run'], mono=e1['mono'], total_h_ref=int(h1[:NREF].sum()), total_n_ref=int(n1[:NREF].sum()),
            weeks_h=dict(zip(*[x.tolist() for x in np.unique(h1, return_counts=True)]))),
    pre=pre, pre_late=pre_late, post=post,
    arl=dict(kmax80=kmax80, rows80=arl80, kmax120=kmax120, rows120=arl120),
    s2=dict(ubar=e2['ubar'], out_u=e2['out_u'], X2=e2['X2'], ddl=e2['ddl'], p=e2['p'], sz=e2['sz'],
            out_l=e2['out_l'], ratio=e2['X2'] / e2['ddl'], total_h=int(h2.sum()), total_n=int(n2.sum())),
)
json.dump(res, open(f"{OUT}/resultats.json", "w"), indent=1, default=float)

# exports xlsx (une feuille, en-tête en ligne 1, comme les jeux de la base)
from openpyxl import Workbook
def save(path, header, rows):
    wb = Workbook(); ws = wb.active; ws.title = "Donnees"; ws.append(header)
    for r in rows: ws.append(r)
    wb.save(path)
save(f"{OUT}/Pannes_cellule_C2_simule.xlsx", ["Semaine", "Heures_marche", "Pannes"],
     [[i + 1, int(h1[i]), int(n1[i])] for i in range(N1)])
save(f"{OUT}/Pannes_parc_presses_simule.xlsx", ["Semaine", "Heures_marche", "Pannes"],
     [[i + 1, int(h2[i]), int(n2[i])] for i in range(len(h2))])
np.save(f"{OUT}/s1_h.npy", h1); np.save(f"{OUT}/s1_n.npy", n1)
np.save(f"{OUT}/s2_h.npy", h2); np.save(f"{OUT}/s2_n.npy", n2)
print(json.dumps(res, indent=1, default=float))
