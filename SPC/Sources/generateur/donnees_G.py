# Jeux simulés du bloc G (mallettes GUNT PT102 et PT105) et calculs de référence des corrigés.
# Tous les jeux sont fictifs, tirés avec une graine fixe. Résolutions supposées : pied à coulisse 0,02 mm, micromètre 0,01 mm.
import json, os, sys
import numpy as np
from scipy import stats
import openpyxl
from openpyxl.styles import Font

OUT = sys.argv[1] if len(sys.argv) > 1 else '.'
os.makedirs(OUT, exist_ok=True)
J = {}   # jeux pour la page « Données à copier »
R = {}   # résultats de référence

def rnd(x, res): return np.round(np.asarray(x, float) / res) * res

def fr(v, dec):  # texte avec virgule
    return ('%.*f' % (dec, v)).replace('.', ',')

def ecrire(cle, nom, entete, lignes, dec):
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'Donnees'; ws.append(entete)
    for r in lignes: ws.append(r)
    for c in ws[1]: c.font = Font(name='Arial', bold=True)
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.font = Font(name='Arial')
            if isinstance(c.value, float): c.number_format = '0.' + '0' * dec
    for col in ws.columns: ws.column_dimensions[col[0].column_letter].width = 14
    wb.save(os.path.join(OUT, nom))
    txt = [[(fr(v, dec) if isinstance(v, float) else str(v)) for v in r] for r in lignes]
    J[cle] = {'nom': nom, 'entete': entete, 'lignes': txt}

# ---------------------------------------------------------------- G1 : linéarité du pied à coulisse sur 150 mm
rng = np.random.default_rng(7101)
vrai = [10, 50, 60, 90, 100, 140, 150]
res1 = 0.02
lignes = []; err = []; xs = []
mes1 = {}
for v in vrai:
    m = rnd(v - 0.004 + 0.00022 * v + 0.011 * rng.standard_normal(5), res1)
    mes1[v] = m
    lignes.append([float(v)] + [float(x) for x in m])
    xs += [v] * 5; err += list(m - v)
ecrire('lin7', 'Linearite_7_points_pied_a_coulisse_simule.xlsx', ['Valeur_vraie', 'M1', 'M2', 'M3', 'M4', 'M5'], lignes, 2)
xs = np.array(xs, float); err = np.array(err)
lr = stats.linregress(xs, err)
n = len(xs); sxx = ((xs - xs.mean()) ** 2).sum(); resid = err - (lr.intercept + lr.slope * xs); s_res = np.sqrt((resid ** 2).sum() / (n - 2))
t_int = lr.intercept / (s_res * np.sqrt(1 / n + xs.mean() ** 2 / sxx)); p_int = 2 * stats.t.sf(abs(t_int), n - 2)
R['G1'] = dict(biais={v: float(np.mean(mes1[v]) - v) for v in vrai}, moy={v: float(np.mean(mes1[v])) for v in vrai}, s={v: float(np.std(mes1[v], ddof=1)) for v in vrai},
               pente=float(lr.slope), p_pente=float(lr.pvalue), t_pente=float(lr.slope / lr.stderr), ordonnee=float(lr.intercept), t_int=float(t_int), p_int=float(p_int), r2=float(lr.rvalue ** 2),
               zero=float(-lr.intercept / lr.slope), biais_max=float(max(abs(np.mean(mes1[v]) - v) for v in vrai)))

# ---------------------------------------------------------------- G2 : R&R sur dix arbres, Ø48 ± 0,2
rng = np.random.default_rng(7102)
res2 = 0.01
vraies = np.array([47.93, 47.99, 48.04, 48.11, 48.02, 47.88, 48.17, 47.96, 48.08, 48.21])
vraies = vraies + 0.0 * vraies
biais_op = {'A': 0.000, 'B': 0.004, 'C': -0.003}
sig_e = 0.0045
X = np.zeros((10, 3, 2))
for j, o in enumerate('ABC'):
    for r in range(2):
        X[:, j, r] = rnd(vraies + biais_op[o] + sig_e * rng.standard_normal(10), res2)
lignes = [[i + 1] + [float(X[i, j, r]) for j in range(3) for r in range(2)] for i in range(10)]
lignes = [[int(l[0])] + l[1:] for l in lignes]
ecrire('rrarbres', 'RR_arbres_diametre48_simule.xlsx', ['Piece', 'A_r1', 'A_r2', 'B_r1', 'B_r2', 'C_r1', 'C_r2'], lignes, 2)

def anova_rr(X, T, K=3, pool_p=0.25):
    p, o, r = X.shape
    gm = X.mean(); mp = X.mean(axis=(1, 2)); mo = X.mean(axis=(0, 2)); mpo = X.mean(axis=2)
    SSp = o * r * ((mp - gm) ** 2).sum(); SSo = p * r * ((mo - gm) ** 2).sum()
    SSpo = r * ((mpo - mp[:, None] - mo[None, :] + gm) ** 2).sum(); SSe = ((X - mpo[:, :, None]) ** 2).sum()
    df = dict(p=p - 1, o=o - 1, po=(p - 1) * (o - 1), e=p * o * (r - 1))
    MS = dict(p=SSp / df['p'], o=SSo / df['o'], po=SSpo / df['po'], e=SSe / df['e'])
    Fpo = MS['po'] / MS['e']; ppo = stats.f.sf(Fpo, df['po'], df['e'])
    if ppo > pool_p:
        mse = (SSpo + SSe) / (df['po'] + df['e']); var_po = 0; pooled = True
    else:
        mse = MS['e']; var_po = max(0, (MS['po'] - MS['e']) / r); pooled = False
    EV = np.sqrt(mse)
    AV2 = max(0, (MS['o'] - (MS['po'] if not pooled else mse)) / (p * r)); AV = np.sqrt(AV2)
    INT = np.sqrt(var_po)
    GRR = np.sqrt(EV ** 2 + AV ** 2 + var_po)
    PV = np.sqrt(max(0, ((MS['p'] - (MS['po'] if not pooled else mse)) / (o * r))))
    TV = np.sqrt(GRR ** 2 + PV ** 2)
    d = dict(EV=EV, AV=AV, INT=INT, GRR=GRR, PV=PV, TV=TV, Fpo=Fpo, ppo=ppo, pooled=pooled,
             pct_T=100 * 2 * K * GRR / T, pct_TV=100 * GRR / TV, ndc=np.sqrt(2) * PV / GRR,
             Fo=MS['o'] / (MS['po'] if not pooled else mse), df=df)
    return {k: (float(v) if not isinstance(v, (bool, dict)) else v) for k, v in d.items()}

R['G2'] = {T: anova_rr(X, T) for T in (0.4, 0.2, 0.1)}
R['G2']['moyennes_op'] = {o: float(X[:, j, :].mean()) for j, o in enumerate('ABC')}
R['G2']['vraies'] = vraies.tolist()

# ---------------------------------------------------------------- G3 : cotes décentrées sur vingt arbres (b = 30,3 +0,4 ; d = 55,2 -0,4)
rng = np.random.default_rng(7103)
res3 = 0.02
b = rnd(30.31 + 0.055 * rng.standard_normal(20), res3)
d = rnd(55.19 + 0.060 * rng.standard_normal(20), res3)
lignes = [[i + 1, float(b[i]), float(d[i])] for i in range(20)]
lignes = [[int(l[0])] + l[1:] for l in lignes]
ecrire('decentre', 'Arbres_cotes_decentrees_simule.xlsx', ['Arbre', 'b_30_3', 'd_55_2'], lignes, 2)

def cap(x, lsi, lss):
    m = np.mean(x); s = np.std(x, ddof=1)
    return dict(n=len(x), m=float(m), s=float(s), Pp=float((lss - lsi) / (6 * s)), Ppk=float(min(lss - m, m - lsi) / (3 * s)),
                bas=int((np.asarray(x) < lsi - 1e-9).sum()), haut=int((np.asarray(x) > lss + 1e-9).sum()),
                p_bas=float(100 * stats.norm.cdf((lsi - m) / s)), p_haut=float(100 * stats.norm.sf((lss - m) / s)),
                milieu=(lsi + lss) / 2, T=lss - lsi)
R['G3'] = dict(b=cap(b, 30.3, 30.7), b_faux=cap(b, 29.9, 30.7), d=cap(d, 54.8, 55.2), d_faux=cap(d, 54.8, 55.6))
R['G3']['b_cible'] = dict(Cp=0.4 / (6 * R['G3']['b']['s']))
R['G3']['sigma_max_133'] = 0.4 / (6 * 1.33)

# ---------------------------------------------------------------- G4 : tri de vingt plaques, profondeur q = 19 +0,0 -0,3 (18,70 à 19,00)
rng = np.random.default_rng(88)
q_vrai = np.array([18.84, 18.92, 18.97, 18.71, 18.86, 18.78, 19.04, 18.90, 18.74, 18.99, 18.82, 18.68, 18.95, 18.88, 19.02, 18.80, 18.93, 18.76, 18.69, 18.91])
ref = np.where((q_vrai >= 18.70) & (q_vrai <= 19.00), 'B', 'M')
biais_c = {'A': 0.000, 'B': 0.022, 'C': -0.015}
dec = {}
for o in 'ABC':
    for r in (1, 2):
        lu = rnd(q_vrai + biais_c[o] + 0.03 * rng.standard_normal(20), 0.05)
        dec[(o, r)] = np.where((lu >= 18.70 - 1e-9) & (lu <= 19.00 + 1e-9), 'B', 'M')
lignes = [[i + 1, str(ref[i])] + [str(dec[(o, r)][i]) for o in 'ABC' for r in (1, 2)] for i in range(20)]
lignes = [[int(l[0])] + l[1:] for l in lignes]
ecrire('tri20', 'Tri_20_plaques_simule.xlsx', ['Plaque', 'Reference', 'A_p1', 'A_p2', 'B_p1', 'B_p2', 'C_p1', 'C_p2'], lignes, 0)

def kappa(e, o):
    e = np.asarray(e); o = np.asarray(o); po = (e == o).mean()
    pe = sum((e == c).mean() * (o == c).mean() for c in 'BM')
    return float((po - pe) / (1 - pe)) if pe < 1 else float('nan')
R['G4'] = {'ref_B': int((ref == 'B').sum()), 'ref_M': int((ref == 'M').sum()), 'ref': ''.join(ref)}
tout_e, tout_o = [], []
for o in 'ABC':
    e = np.concatenate([ref, ref]); dd = np.concatenate([dec[(o, 1)], dec[(o, 2)]])
    tout_e.append(e); tout_o.append(dd)
    mauv = (e == 'M'); bon = (e == 'B')
    contra = int((dec[(o, 1)] != dec[(o, 2)]).sum())
    toujours = int(((dec[(o, 1)] == ref) & (dec[(o, 2)] == ref)).sum())
    R['G4'][o] = dict(kappa=kappa(e, dd), accord=float(100 * (e == dd).mean()), taux_erreur=float(100 * ((dd == 'B') & mauv).sum() / mauv.sum()),
                      fausse_alarme=float(100 * ((dd == 'M') & bon).sum() / bon.sum()), contradictions=contra, toujours_ok=toujours)
R['G4']['kappa_global_min'] = min(R['G4'][o]['kappa'] for o in 'ABC')
R['G4']['erreur_global_max'] = max(R['G4'][o]['taux_erreur'] for o in 'ABC')
R['G4']['kappa_poole'] = kappa(np.concatenate(tout_e), np.concatenate(tout_o))
R['G4']['tous_d_accord'] = int(sum(1 for i in range(20) if len({str(dec[(o, r)][i]) for o in 'ABC' for r in (1, 2)}) == 1))
R['G4']['tous_egal_ref'] = int(sum(1 for i in range(20) if all(str(dec[(o, r)][i]) == str(ref[i]) for o in 'ABC' for r in (1, 2))))
R['G4']['desaccords_plaques'] = [i + 1 for i in range(20) if len({str(dec[(o, r)][i]) for o in 'ABC' for r in (1, 2)}) > 1]

# ---------------------------------------------------------------- G5 : neuf cotes sur vingt plaques
rng = np.random.default_rng(7105)
cotes = ['a', 'b', 'c', 'd', 'm', 'n', 'o', 'q', 'r']
tol = {'a': (105, -0.3, 0.3), 'b': (40, -0.3, 0.3), 'c': (44, -0.3, 0.3), 'd': (75, 0.0, 0.3), 'm': (6.5, -0.2, 0.2), 'n': (28, -0.3, 0.1), 'o': (34, -0.1, 0.1), 'q': (19, -0.3, 0.0), 'r': (16, -0.3, 0.0)}
cent = {'a': 105.02, 'b': 40.00, 'c': 44.03, 'd': 75.14, 'm': 6.52, 'n': 27.93, 'o': 34.02, 'q': 18.97, 'r': 15.96}
sg = {'a': 0.060, 'b': 0.055, 'c': 0.060, 'd': 0.050, 'm': 0.050, 'n': 0.050, 'o': 0.045, 'q': 0.045, 'r': 0.050}
tab = {c: rnd(cent[c] + sg[c] * rng.standard_normal(20), 0.02) for c in cotes}
# Les cotes b et c (positions d'axe) ne sont pas mesurables directement au pied à coulisse : le tirage les génère (pour garder les mêmes valeurs) mais elles ne sont pas publiées.
cotes7 = ['a', 'd', 'm', 'n', 'o', 'q', 'r']
lignes = [[i + 1] + [float(tab[c][i]) for c in cotes7] for i in range(20)]
lignes = [[int(l[0])] + l[1:] for l in lignes]
ecrire('cotes7', 'Plaques_7_cotes_simule.xlsx', ['Plaque'] + cotes7, lignes, 2)
R['G5'] = {}
for c in cotes7:
    nom, lo, hi = tol[c]; lsi, lss = nom + lo, nom + hi
    x = tab[c]; k = cap(x, lsi, lss) | dict(lsi=lsi, lss=lss, rej=int(((x < lsi - 1e-9) | (x > lss + 1e-9)).sum()), rej_bas=int((x < lsi - 1e-9).sum()), rej_haut=int((x > lss + 1e-9).sum()))
    R['G5'][c] = k
R['G5']['tot'] = sum(R['G5'][c]['rej'] for c in cotes7)

json.dump({'J': J, 'R': R}, open(os.path.join(OUT, 'donnees_G.json'), 'w', encoding='utf-8'), ensure_ascii=False, default=lambda o: o.tolist() if hasattr(o, 'tolist') else str(o), indent=1)
print('ok')
