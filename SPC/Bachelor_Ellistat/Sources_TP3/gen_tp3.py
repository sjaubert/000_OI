"""TP 3 : données SIMULÉES et recalcul de tous les chiffres. Usage : python3 -I gen_tp3.py <base_Donnees_Ellistat> <sortie>"""
import sys, json
import numpy as np
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from rr_lib import cg_stats, rr_anova, read_rr
from openpyxl import Workbook
BASE, OUT = sys.argv[1], sys.argv[2]
T48, LSI48, LSS48 = 0.4, 47.8, 48.2        # Ø g = 48 ± 0,2 (dessin GUNT PT105.10.00.011)
T19, LSI19, LSS19 = 0.3, 18.7, 19.0        # q = 19 +0,0/-0,3 (dessin GUNT PT102.10.00.012)
q = lambda v, r: np.round(np.round(np.asarray(v) / r) * r, 4)

def cg_series(seed, true, bias, sig, res, n=25):
    rng = np.random.default_rng(seed); return q(true + bias + rng.normal(0, sig, n), res)

def find(cond, gen, rng_seeds=range(1, 20000)):
    for s in rng_seeds:
        v = gen(s)
        if cond(v): return s, v
    raise SystemExit("aucune graine")

# ---- Cg, cale 48 mm
s48m, x48m = find(lambda x: 2.5 <= cg_stats(x, T48, 48.0)['cg'] <= 4.5, lambda s: cg_series(s, 48.0, 0.002, 0.0035, 0.01))
s48p, x48p = find(lambda x: 1.15 <= cg_stats(x, T48, 48.0)['cg'] <= 1.45 and cg_stats(x, T48, 48.0)['cgk'] < 1.33,
                  lambda s: cg_series(s, 48.0, 0.003, 0.009, 0.02))
# ---- Cg, cale 19 mm (micromètre 0-25 supposé disponible, à confirmer)
s19m, x19m = find(lambda x: 2.0 <= cg_stats(x, T19, 19.0)['cg'] <= 4.5, lambda s: cg_series(s, 19.0, 0.002, 0.0035, 0.01))
s19p, x19p = find(lambda x: 0.8 <= cg_stats(x, T19, 19.0)['cg'] <= 1.15, lambda s: cg_series(s, 19.0, 0.003, 0.009, 0.02))

# ---- R&R arbres : même lot que la base (micromètre 0,01), version pied à coulisse 0,02
A = read_rr(f"{BASE}/RR_arbres_diametre48_simule.xlsx")        # (10, 3, 2)
truth = A.mean(axis=(1, 2))
def rr_caliper(seed):
    rng = np.random.default_rng(seed); opb = np.array([0.012, -0.010, 0.000])
    d = truth[:, None, None] + opb[None, :, None] + rng.normal(0, 0.012, (10, 3, 2))
    return q(d, 0.02)
srr, Cal = find(lambda d: 28 <= rr_anova(d, T48)['pct_GRR_T'] <= 34 and rr_anova(d, T48)['ndc'] >= 5, rr_caliper)
r_mic = rr_anova(A, T48); r_cal = rr_anova(Cal, T48)

res = dict(
  seeds=dict(cg48_mic=s48m, cg48_pied=s48p, cg19_mic=s19m, cg19_pied=s19p, rr_pied=srr),
  cg48_mic=cg_stats(x48m, T48, 48.0), cg48_pied=cg_stats(x48p, T48, 48.0),
  cg19_mic=cg_stats(x19m, T19, 19.0), cg19_pied=cg_stats(x19p, T19, 19.0),
  rr_mic=r_mic, rr_pied=r_cal,
  resolution_sur_T={ 'pied_48': 0.02/T48, 'mic_48': 0.01/T48, 'pied_19': 0.02/T19, 'mic_19': 0.01/T19 },
)
json.dump(res, open(f"{OUT}/resultats_tp3.json", "w"), indent=1, default=float)

def save(path, header, rows):
    wb = Workbook(); ws = wb.active; ws.title = "Donnees"; ws.append(header)
    for r in rows: ws.append(r)
    wb.save(path)
save(f"{OUT}/Cg_cale48_simule.xlsx", ["Micrometre", "Pied_a_coulisse"], [[float(a), float(b)] for a, b in zip(x48m, x48p)])
save(f"{OUT}/Cg_cale19_simule.xlsx", ["Micrometre", "Pied_a_coulisse"], [[float(a), float(b)] for a, b in zip(x19m, x19p)])
hdr = ["Piece", "A_r1", "A_r2", "B_r1", "B_r2", "C_r1", "C_r2"]
save(f"{OUT}/RR_arbres_pied_simule.xlsx", hdr, [[i + 1] + [float(v) for v in Cal[i].reshape(-1)] for i in range(10)])
save(f"{OUT}/RR_arbres_micrometre_simule.xlsx", hdr, [[i + 1] + [float(v) for v in A[i].reshape(-1)] for i in range(10)])
# grille de relevé vierge avec ordre de passage tiré au sort (graine fixe)
rng = np.random.default_rng(2026)
wb = Workbook(); ws = wb.active; ws.title = "Releve_R&R"
ws.append(["Operateur", "Serie", "Ordre", "Arbre_no", "Instrument", "Valeur_mm", "Duree_s"])
for op in "ABC":
    for serie in (1, 2):
        perm = rng.permutation(10) + 1
        for k, a in enumerate(perm, 1): ws.append([op, serie, k, int(a), "", None, None])
wb.save(f"{OUT}/Releve_RR_arbres_vierge.xlsx")
print(json.dumps(res, indent=1, default=float))
