# Génère les fiches (LaTeX), le guide formateur et les données du catalogue à partir des fichiers acts_*.py
import json, os, re, unicodedata, subprocess, sys
from acts_E import E
from acts_M import M
from acts_A import A
from acts_C import C
from acts_G import G
ICI = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(ICI, 'tex'); os.makedirs(TEX, exist_ok=True)
BLOCS = {'E': ("Prise en main d'Ellistat", E), 'M': ("Le moyen de mesure", M), 'A': ("Cartes aux attributs", A), 'C': ("Cartes aux mesures et capabilité", C), 'G': ("Mallettes GUNT : plaques et arbres", G)}
ORG = {'seul': 'seul', 'binome': 'en binôme', 'trinome': 'en trinôme', 'groupe': 'en groupe', 'rotation': 'rotation sur postes'}

def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return re.sub(r'[^A-Za-z0-9]+', '_', s).strip('_')
def tex(s):
    for a, b in [('\\', r'\textbackslash{}'), ('&', r'\&'), ('%', r'\%'), ('#', r'\#'), ('_', r'\_'), ('×', r'$\times$'), ('p̄', r'$\bar p$')]:
        s = s.replace(a, b)
    return s
def nomfiche(a): return f"{a['code']}_{slug(a['titre'])}"

# ---------- relevés ----------
def grille(n, titre):
    lig = []
    for r in range(0, n, 5):
        c = []
        for k in range(r, r + 5): c += [rf"\scriptsize {k+1}" if k < n else "", ""]
        lig.append(" & ".join(c) + r"\\\hline")
    return (rf"\textbf{{{titre}}}\par\vspace{{2pt}}" + "\n" + r"{\renewcommand{\arraystretch}{1.45}\begin{tabularx}{\linewidth}{|*{5}{>{\centering\arraybackslash}p{5mm}|>{\centering\arraybackslash}X|}}\hline" + "\n" + "\n".join(lig) + "\n" + r"\end{tabularx}}\par")
def grille3(n, titre):
    lig = []
    for r in range(0, n, 3):
        c = []
        for k in range(r, r + 3): c += [rf"\scriptsize {k+1}" if k < n else "", ""]
        lig.append(" & ".join(c) + r"\\\hline")
    return (rf"\textbf{{{titre}}}\par\vspace{{2pt}}" + "\n" + r"{\renewcommand{\arraystretch}{1.4}\begin{tabularx}{\linewidth}{|*{3}{>{\centering\arraybackslash}p{5mm}|>{\centering\arraybackslash}X|}}\hline" + "\n" + "\n".join(lig) + "\n" + r"\end{tabularx}}")
def releve(r):
    if r is None: return ""
    k = r[0]
    if k == 'grille': return grille(r[1], tex(r[2]))
    if k == 'deux':
        return (r"\begin{minipage}[t]{0.485\linewidth}" + grille3(r[1], tex(r[2])) + r"\end{minipage}\hfill\begin{minipage}[t]{0.485\linewidth}" + grille3(r[1], tex(r[3])) + r"\end{minipage}\par")
    if k == 'table':
        h, rows = r[1], r[2]; n = len(h) - 1
        s = r"{\renewcommand{\arraystretch}{1.5}\begin{tabularx}{\linewidth}{|l|*{%d}{>{\centering\arraybackslash}X|}}\hline" % n + "\n"
        s += " & ".join(rf"\textbf{{{tex(x)}}}" for x in h) + r"\\\hline" + "\n"
        for x in rows: s += tex(x) + " & " * n + r"\\\hline" + "\n"
        return s + r"\end{tabularx}}\par"
    if k == 'situations':
        h, rows = r[1], r[2]
        s = r"{\renewcommand{\arraystretch}{1.5}\begin{tabularx}{\linewidth}{|c|X|p{30mm}|p{17mm}|p{14mm}|}\hline" + "\n"
        s += r" & " + " & ".join(rf"\textbf{{\small {tex(x)}}}" for x in h) + r"\\\hline" + "\n"
        for i, x in enumerate(rows): s += f"{i+1} & {tex(x)} & & & " + r"\\\hline" + "\n"
        return s + r"\end{tabularx}}\par"
    if k == 'temps':
        n = r[1]; t = [30 * i for i in range(n)]
        s = r"Référence (moyenne de 3 mesures à la température de la salle) : \champ{22mm} mm\par\vspace{3pt}" + "\n"
        s += r"{\renewcommand{\arraystretch}{1.5}\small\begin{tabularx}{\linewidth}{|l|*{%d}{>{\centering\arraybackslash}X|}}\hline" % n + "\n"
        s += r"\textbf{Temps (s)} & " + " & ".join(str(x) for x in t) + r"\\\hline" + "\n" + rf"\textbf{{{tex(r[2])}}}" + " & " * n + r"\\\hline\end{tabularx}}\par\vspace{4pt}" + "\n"
        s += r"\begin{center}\begin{tikzpicture}[x=1.45cm,y=0.5cm]\draw[gray!45,very thin] (0,0) grid (10,6);\draw[thick] (0,0)--(10,0);\draw[thick] (0,0)--(0,6);" + "".join(rf"\node[below,font=\scriptsize] at ({i},0) {{{30*i}}};" for i in range(11)) + r"\node[below,font=\scriptsize] at (5,-0.55) {temps (s)};\node[rotate=90,font=\scriptsize] at (-0.55,3) {mesure : un carreau = 0,001 mm};\end{tikzpicture}\end{center}"
        return s
    if k == 'etalons':
        s = r"{\renewcommand{\arraystretch}{1.45}\begin{tabularx}{\linewidth}{|c|X|c|}\hline" + "\n"
        s += r"\textbf{Étalon visé} & \textbf{Cales choisies (mm)} & \textbf{Somme (mm)}\\\hline" + "\n"
        for v in ("11,850", "11,925", "12,000"): s += v + r" mm & & \\\hline" + "\n"
        s += r"\end{tabularx}}\par\vspace{5pt}" + "\n"
        s += r"{\renewcommand{\arraystretch}{1.15}\small\begin{tabularx}{\linewidth}{|l|*{3}{>{\centering\arraybackslash}X|}}\hline" + "\n"
        s += r"\textbf{Mesure} & \textbf{11,850} & \textbf{11,925} & \textbf{12,000}\\\hline" + "\n"
        for i in range(1, 11): s += f"{i} & & & " + r"\\\hline" + "\n"
        for lab in ("Moyenne (mm)", r"Biais = moyenne $-$ étalon (µm)", r"$|\text{biais}| / s$ (à la main)", "Cg (Ellistat)", "Cgk (Ellistat)"):
            s += r"\textbf{" + lab + r"} & & & \\\hline" + "\n"
        return s + r"\end{tabularx}}\par"
    if k == 'derive':
        s = r"{\renewcommand{\arraystretch}{1.5}\small\begin{tabularx}{\linewidth}{|c|p{12mm}|p{11mm}|*{5}{>{\centering\arraybackslash}X|}p{17mm}|p{14mm}|}\hline" + "\n"
        s += r"\textbf{N°} & \textbf{Heure} & \textbf{Qui} & 1 & 2 & 3 & 4 & 5 & \textbf{Moy.} & \textbf{Étendue}\\\hline" + "\n"
        for i in range(1, 9): s += f"{i}" + " & " * 9 + r"\\\hline" + "\n"
        s += r"\end{tabularx}}\par\vspace{4pt}" + "\n"
        s += r"{\renewcommand{\arraystretch}{1.35}\begin{tabularx}{\linewidth}{|X|c|c|}\hline & \textbf{À la main} & \textbf{Ellistat}\\\hline" + "\n"
        for lab in [r"Moyenne générale $\bar{\bar X}$ \quad / \quad étendue moyenne $\bar R$ (passages 1 à 6)", "Limite supérieure des moyennes", "Limite inférieure des moyennes", "Limite supérieure des étendues"]:
            s += lab + r" & \hspace{28mm} & \hspace{28mm}\\\hline" + "\n"
        return s + r"\end{tabularx}}\par"
    if k == 'grades':
        s = r"{\renewcommand{\arraystretch}{1.35}\small\begin{tabularx}{\linewidth}{|l|*{3}{>{\centering\arraybackslash}X|}}\hline" + "\n"
        s += r"\textbf{Écart limite de longueur (µm)} & \textbf{Grade 0} & \textbf{Grade 1} & \textbf{Grade 2}\\\hline" + "\n"
        s += r"Cale jusqu'à 10 mm & $\pm 0{,}12$ & $\pm 0{,}20$ & $\pm 0{,}45$\\\hline" + "\n"
        s += r"Cale de plus de 10 mm à 25 mm & $\pm 0{,}14$ & $\pm 0{,}30$ & $\pm 0{,}60$\\\hline" + "\n"
        s += r"\end{tabularx}}\par{\footnotesize ISO 3650, valeurs relevées sur des pages de revendeurs : le certificat de vos cales fait foi.}\par\vspace{5pt}" + "\n"
        return s + releve(('deux', 15, 'Cale céramique grade 0 (mm)', 'Cale acier grade 1 (mm)'))
    if k == 'cotes':
        s = r"{\renewcommand{\arraystretch}{1.5}\begin{tabularx}{\linewidth}{|l|*{2}{>{\centering\arraybackslash}X|}}\hline" + "\n"
        s += r"\textbf{Opérateur} & \textbf{Écart moyen aux cotes (µm)} & \textbf{Plus grand écart, en valeur absolue (µm)}\\\hline" + "\n"
        for o in "ABC": s += o + r" & & \\\hline" + "\n"
        s += r"\end{tabularx}}\par\vspace{5pt}" + "\n"
        s += r"{\renewcommand{\arraystretch}{1.5}\begin{tabularx}{\linewidth}{|*{4}{>{\centering\arraybackslash}X|}}\hline" + "\n"
        s += r"\textbf{EV (mm)} & \textbf{AV (mm)} & \textbf{\%GRR} & \textbf{Catégories distinctes}\\\hline" + "\n"
        s += r"\rule{0pt}{7mm} & & & \\\hline" + "\n"
        return s + r"\end{tabularx}}\par"
    if k == 'lin':
        s = r"{\renewcommand{\arraystretch}{1.45}\small\begin{tabularx}{\linewidth}{|l|*{10}{>{\centering\arraybackslash}X|}p{15mm}|p{15mm}|}\hline" + "\n"
        s += r"\textbf{Cale} & " + " & ".join(rf"\scriptsize {i}" for i in range(1, 11)) + r" & \textbf{\scriptsize Moyenne} & \textbf{\scriptsize Biais (µm)}\\\hline" + "\n"
        for c in (5, 10, 15, 20, 25): s += f"{c} mm" + " & " * 12 + r"\\\hline" + "\n"
        return s + r"\end{tabularx}}\par{\small Biais = moyenne $-$ valeur de la cale. 1 µm = 0,001 mm.}\par"
    if k == 'tri':
        n = r[1]
        s = r"{\renewcommand{\arraystretch}{1.45}\small\setlength{\tabcolsep}{2pt}\begin{tabularx}{\linewidth}{|l|*{%d}{>{\centering\arraybackslash}X|}}\hline" % n + "\n"
        s += r"\textbf{" + (r[2] if len(r) > 2 and r[2] else "Butée") + r"} & " + " & ".join(rf"\scriptsize {i}" for i in range(1, n + 1)) + r"\\\hline" + "\n"
        for lab in ("Passage 1", "Passage 2", "Référence"): s += lab + " & " * n + r"\\\hline" + "\n"
        return s + r"\end{tabularx}}\par{\small B = bonne, M = mauvaise. La ligne « Référence » se remplit à la fin, avec le formateur.}\par"
    if k == 'lots':
        n, mode = r[1], r[2]; par = 10 if n <= 20 else 12; s = ""
        l1 = "Lot" if mode == 'p' else "Unité"; l2 = "Défectueuses" if mode == 'p' else "Défauts"
        for d in range(0, n, par):
            idx = list(range(d + 1, min(d + par, n) + 1)); vide = par - len(idx)
            s += r"{\renewcommand{\arraystretch}{1.35}\small\begin{tabularx}{\linewidth}{|l|*{%d}{>{\centering\arraybackslash}X|}}\hline" % par + "\n"
            s += rf"\textbf{{{l1}}} & " + " & ".join(str(i) for i in idx) + " & " * vide + r"\\\hline" + "\n" + rf"\textbf{{{l2}}}" + " & " * par + r"\\\hline\end{tabularx}}\par\vspace{2pt}" + "\n"
        ymax = 12 if mode == 'p' else 14; xs = 15.6 / n
        s += r"\begin{center}\begin{tikzpicture}[x=%.3fcm,y=0.31cm]" % xs
        s += rf"\draw[gray!45,very thin] (0,0) grid ({n},{ymax});\draw[thick] (0,0)--({n},0);\draw[thick] (0,0)--(0,{ymax});"
        s += "".join(rf"\node[left,font=\scriptsize] at (0,{y}) {{{y}}};" for y in range(0, ymax + 1, 2))
        s += "".join(rf"\node[below,font=\scriptsize] at ({i},0) {{{i}}};" for i in range(1, n + 1) if n <= 20 or i % 5 == 0 or i == 1)
        if mode == 'p': s += "".join(rf"\node[right,font=\scriptsize] at ({n},{y}) {{{2*y} \%}};" for y in range(0, ymax + 1, 2))
        s += rf"\node[rotate=90,font=\scriptsize] at (-{1.1/xs:.2f},{ymax/2}) {{{'pièces défectueuses' if mode=='p' else 'défauts'}}};\node[below,font=\scriptsize] at ({n/2},-1.3) {{{'lot' if mode=='p' else 'unité'}}};"
        return s + r"\end{tikzpicture}\end{center}"
    if k == 'xbar':
        s = r"{\renewcommand{\arraystretch}{1.45}\begin{tabularx}{\linewidth}{|l|*{6}{>{\centering\arraybackslash}X|}}\hline" + "\n" + r"\textbf{Sous-groupe} & 1 & 2 & 3 & 4 & 5 & 6\\\hline Moyenne & & & & & & \\\hline Étendue $R$ & & & & & & \\\hline\end{tabularx}}\par\vspace{3pt}" + "\n"
        s += r"{\renewcommand{\arraystretch}{1.4}\begin{tabularx}{\linewidth}{|X|c|c|}\hline & \textbf{À la main} & \textbf{Ellistat}\\\hline" + "\n"
        for lab in [r"Moyenne générale $\bar{\bar X}$ \quad / \quad étendue moyenne $\bar R$", "Limite supérieure des moyennes", "Limite inférieure des moyennes", "Limite supérieure des étendues", "Écart-type court terme", "Cp \\quad / \\quad Cpk", "Pp \\quad / \\quad Ppk"]:
            s += lab + r" & \hspace{28mm} & \hspace{28mm}\\\hline" + "\n"
        return s + r"\end{tabularx}}\par"
    if k == 'lin7':
        s = r"{\renewcommand{\arraystretch}{1.5}\small\setlength{\tabcolsep}{3pt}\begin{tabularx}{\linewidth}{|l|*{5}{>{\centering\arraybackslash}X|}>{\centering\arraybackslash}p{15mm}|>{\centering\arraybackslash}p{15mm}|}\hline" + "\n"
        s += r"\textbf{Longueur} & " + " & ".join(rf"\scriptsize {i}" for i in range(1, 6)) + r" & \textbf{\scriptsize Moyenne} & \textbf{\scriptsize Biais (µm)}\\\hline" + "\n"
        for c in (10, 50, 60, 90, 100, 140, 150): s += f"{c} mm" + " & " * 7 + r"\\\hline" + "\n"
        return s + r"\end{tabularx}}\par{\small Biais = moyenne $-$ valeur de la cale. 1 µm = 0,001 mm.}\par"
    if k == 'decentre':
        s = r"{\renewcommand{\arraystretch}{1.5}\small\begin{tabularx}{\linewidth}{|l|*{5}{>{\centering\arraybackslash}X|}}\hline" + "\n"
        s += r"\textbf{Cote} & \textbf{Nominal} & \textbf{Limite basse} & \textbf{Limite haute} & \textbf{Milieu} & \textbf{$T$}\\\hline" + "\n"
        for c in "bd": s += rf"{c} & & & & & " + r"\\\hline" + "\n"
        s += r"\end{tabularx}}\par\vspace{5pt}" + "\n"
        return s + releve(('deux', 20, 'Cote b (mm)', 'Cote d (mm)'))
    raise ValueError(k)


PLANS = {
 'G1': ("Plan de la plaque PT102", "plan_plaque_PT102.pdf", "Distanzplatte (plaque d'écartement), dessin PT102.10.00.012",
        [(r"$a$", r"105, aucun écart écrit", r"classe m, plage 30 à 120 : $\pm 0{,}3$"),
         (r"$o$", r"\hspace{2pt}\carre{}\ 34, avec $+0{,}1$ et $-0{,}1$", r"écrit sur le plan : $+0{,}1$ et $-0{,}1$")]),
 'G2': ("Plan de l'arbre PT105", "plan_arbre_PT105.pdf", "Welle (arbre), dessin PT105.10.00.011",
        [(r"$g$", r"\O\ 48 avec $\pm 0{,}2$", r"écrit sur le plan : $\pm 0{,}2$")]),
 'G3': ("Plan de l'arbre PT105", "plan_arbre_PT105.pdf", "Welle (arbre), dessin PT105.10.00.011",
        [(r"$b$", r"30,3 avec $+0{,}4$ (un seul écart écrit)", r"convention de cette fiche : l'autre écart vaut $0$"),
         (r"$d$", r"55,2 avec $-0{,}4$ (un seul écart écrit)", r"convention de cette fiche : l'autre écart vaut $0$")]),
 'G4': ("Plan de la plaque PT102", "plan_plaque_PT102.pdf", "Distanzplatte (plaque d'écartement), dessin PT102.10.00.012",
        [(r"$q$", r"19 avec $+0{,}0$ et $-0{,}3$", r"écrit sur le plan : $+0{,}0$ et $-0{,}3$")]),
 'G5': ("Plan de la plaque PT102", "plan_plaque_PT102.pdf", "Distanzplatte (plaque d'écartement), dessin PT102.10.00.012",
        [(r"$a$", r"105, aucun écart écrit", r"classe m, plage 30 à 120 : $\pm 0{,}3$"),
         (r"$d$", r"75 avec $+0{,}3$ et $-0{,}0$", r"écrit sur le plan : $+0{,}3$ et $0$"),
         (r"$m$", r"6,5, aucun écart écrit", r"classe m, plage au-delà de 6 jusqu'à 30 : $\pm 0{,}2$"),
         (r"$n$", r"\hspace{2pt}\carre{}\ 28, avec $+0{,}1$ et $-0{,}3$", r"écrit sur le plan : $+0{,}1$ et $-0{,}3$"),
         (r"$o$", r"\hspace{2pt}\carre{}\ 34, avec $+0{,}1$ et $-0{,}1$", r"écrit sur le plan : $+0{,}1$ et $-0{,}1$"),
         (r"$q$", r"19 avec $+0{,}0$ et $-0{,}3$", r"écrit sur le plan : $+0{,}0$ et $-0{,}3$"),
         (r"$r$", r"16 avec $+0{,}0$ et $-0{,}3$", r"écrit sur le plan : $+0{,}0$ et $-0{,}3$")]),
}
BOX_SUR_PLAN = {'G4'}   # fiche d'une page : l'encadré « Lire le plan » est sur la page du plan

def lire_plan(code):
    pl = PLANS[code]
    rows = " \\\\\\hline\n".join(" & ".join(r) for r in pl[3])
    s = r"\providecommand{\carre}{\fbox{\rule{0pt}{1.1ex}\rule{1.1ex}{0pt}}}" + "\n" + r"\begin{tcolorbox}[boite,left=5pt,right=5pt,top=3pt,bottom=3pt]\footnotesize" + "\n"
    s += r"\textbf{\color{uimm}Lire le plan GUNT (dernière page).} Le cartouche du plan est écrit en allemand et en anglais. À la ligne « Allgemeintoleranzen / General tolerance », on lit \textbf{ISO 2768-mK}. Cela veut dire : toute cote \textbf{sans écart écrit} a la tolérance générale de la classe \textbf{m} (« medium »), donnée par le tableau ci-dessous. Une cote \textbf{avec un écart écrit} garde cet écart, et la tolérance générale ne s'applique pas. Limite haute = nominal + écart supérieur. Limite basse = nominal + écart inférieur. \O\ : diamètre. \carre{} : carré, on lit son côté. « A-A », « B-B » : coupes. Les symboles d'état de surface et d'arêtes, en bas à droite, ne servent pas dans cette fiche." + "\n"
    s += r"\par\vspace{6pt}\noindent\renewcommand{\arraystretch}{1.2}\setlength{\tabcolsep}{4pt}" + "\n"
    s += r"\begin{tabular}{|l|c|c|c|c|c|}\hline" + "\n"
    s += r"\textbf{Dimension nominale (mm)} & 0,5 à 3 & au-delà de 3 à 6 & au-delà de 6 à 30 & au-delà de 30 à 120 & au-delà de 120 à 400\\\hline" + "\n"
    s += r"\textbf{Écart de la classe m (mm)} & $\pm 0{,}1$ & $\pm 0{,}1$ & $\pm 0{,}2$ & $\pm 0{,}3$ & $\pm 0{,}5$\\\hline" + "\n"
    s += r"\end{tabular}" + "\n"
    s += r"\par\vspace{1pt}{\scriptsize Source : ISO 2768-1:1989, tolérances générales des dimensions linéaires, reprises dans la fiche GUNT « PT105f Tolérances ».}" + "\n"
    s += r"\par\vspace{4pt}\textbf{Les cotes de cette fiche}\par\vspace{2pt}" + "\n"
    s += r"\begin{tabularx}{\linewidth}{|c|>{\raggedright\arraybackslash}X|>{\raggedright\arraybackslash}X|}\hline" + "\n"
    s += r"\textbf{Cote} & \textbf{Ce que le plan écrit} & \textbf{Écart à utiliser}\\\hline" + "\n"
    s += rows + r" \\\hline" + "\n"
    s += r"\end{tabularx}" + "\n"
    s += r"\end{tcolorbox}"
    return s

COUPE = {'A2', 'A4', 'A6', 'M6', 'M14', 'M15', 'M16', 'M17', 'G1', 'G2', 'G3', 'G5'}   # fiches sur deux pages : coupure avant les questions
TAG = {'E': r"\tagE\ ", 'W': r"\tagW\ ", 'M': ""}
def fiche(a, bloc):
    L = [r"\documentclass[10pt,a4paper]{article}", r"\input{commun.tex}", rf"\pied{{Base SPC · fiche {a['code']} · {tex(a['titre'])}}}", r"\begin{document}", r"\thispagestyle{fancy}"]
    L.append(rf"\entete{{{a['code']}}}{{{tex(a['titre'])}}}{{{tex(a['question'])}}}{{{tex(bloc)}}}{{{a['duree']} min}}{{{ORG[a['org']['mode']]}}}{{{a['niveau']}}}")
    L.append(r"\begin{tcolorbox}[boite]" + rf"\textbf{{Le but.}} {tex(a['but'])}\par\textbf{{Il vous faut.}} " + " · ".join(tex(m) for m in a['materiel']) + r"\end{tcolorbox}")
    if a.get('encadre'):
        L.append(r"\begin{tcolorbox}[boite]" + a['encadre'] + r"\end{tcolorbox}")
    if a['predire']:
        L.append(r"\begin{tcolorbox}[pred]" + a['predire'] + r"\reponse\end{tcolorbox}")
    L.append(r"\titre{À faire}")
    L.append(r"\begin{enumerate}[label=\textcolor{cyan}{\textbf{\arabic*.}},leftmargin=15pt,itemsep=1.5pt]")
    for e in a['etapes']:
        k, t = e.split('|', 1); L.append(r"\item " + TAG[k] + t)
    L.append(r"\end{enumerate}")
    if a['releve']:
        L.append(r"\vspace{3pt}" + releve(a['releve']))
    if a['code'] in COUPE: L.append(r"\newpage")
    L.append(r"\titre{J'observe, je décide}")
    L.append(r"\begin{enumerate}[label=\textcolor{cyan}{\textbf{Q\arabic*.}},leftmargin=22pt]")
    for q, n in a['questions']:
        L.append(r"\item " + q + (rf"\reponse[{n}]" if n else r"\par\vspace{5pt}"))
    L.append(r"\end{enumerate}")
    L.append(r"\begin{tcolorbox}[retenir]" + a['retenir'] + r"\end{tcolorbox}")
    if a['plus']: L.append(r"\begin{tcolorbox}[plus]" + a['plus'] + r"\end{tcolorbox}")
    if a['code'].startswith('G') and a['code'] not in BOX_SUR_PLAN:
        L.append(lire_plan(a['code']))
    if a['code'].startswith('G'):
        res = []
        for lab, h in a['liens']:
            u = "https://sjaubert.github.io/000_OI/SPC/" + (h[3:] if h.startswith('../') else 'Activites/' + h)
            res.append(tex(lab) + r" : \href{" + u.replace('#', r'\#') + r"}{\nolinkurl{" + u.split('#')[0] + "}}")
        if res: L.append(r"\vfill{\footnotesize\color{uimm}\textbf{Ressources de la base :}" + (" " if len(res) == 1 else r"\par ") + r"\par ".join(res) + "}")
    else:
        res = [tex(l[0]) for l in a['liens']]
        if res: L.append(r"\vfill{\footnotesize\color{uimm}\textbf{Ressources de la base :} " + " · ".join(res) + ".}")
    if a['code'].startswith('G'):
        pl = PLANS[a['code']]
        L.append(r"\newpage")
        L.append(r"\titre{" + pl[0] + "}")
        if a['code'] in BOX_SUR_PLAN:
            L.append(lire_plan(a['code']))
            L.append(r"\begin{center}\includegraphics[width=0.74\textheight,height=0.97\linewidth,keepaspectratio,angle=90]{" + pl[1] + "}\\end{center}")
        else:
            L.append(r"{\small Pour lire ce plan et ses tolérances, voir l'encadré « Lire le plan GUNT » de la page précédente.\par}\vspace{2pt}")
            L.append(r"\begin{center}\includegraphics[width=0.90\textheight,height=0.97\linewidth,keepaspectratio,angle=90]{" + pl[1] + "}\\end{center}")
        L.append(r"\vfill{\footnotesize\color{uimm}Plan : GUNT Hamburg, " + pl[2] + ".}")
    L.append(r"\end{document}")
    return "\n".join(L)

def toutes():
    return [(b, nom, a) for b, (nom, lst) in BLOCS.items() for a in lst]

def ecrire_fiches():
    for b, nom, a in toutes():
        open(os.path.join(TEX, nomfiche(a) + '.tex'), 'w', encoding='utf-8').write(fiche(a, nom))

def guide():
    L = []
    for b, (nom, lst) in BLOCS.items():
        L.append(rf"\section*{{Bloc {b} · {tex(nom)}}}")
        for a in lst:
            f = a['formateur']
            L.append(r"\begin{tcolorbox}[act]" + rf"\textbf{{{a['code']} · {tex(a['titre'])}}} \hfill {{\small {a['duree']} min · {ORG[a['org']['mode']]} · niveau {a['niveau']}" + (" · Ellistat" if a['ellistat'] else "") + (" · mesures" if a['mesure'] else "") + r"}\end{tcolorbox}")
            if f['prep']: L.append(r"\textbf{Préparation.} " + " ".join(f['prep']) + r"\par")
            if f['anim']: L.append(r"\textbf{Animation.} " + " ".join(f['anim']) + r"\par")
            L.append(rf"\textbf{{\color{{ok}}Corrigé de la fiche {a['code']}.}} " + r"\par ".join(f['corrige']) + r"\par")
            if f.get('secours'): L.append(r"{\small\textbf{Repli ou remarque.} " + f['secours'] + r"}\par")
            L.append(r"\vspace{3pt}")
    return "\n".join(L)

def tableau_activites():
    s = r"{\small\renewcommand{\arraystretch}{1.12}\begin{longtable}{@{}l p{74mm} r l c c c@{}}\toprule" + "\n" + r"\textbf{Code} & \textbf{Activité} & \textbf{Durée} & \textbf{Organisation} & \textbf{Niveau} & \textbf{Ellistat} & \textbf{Mesures}\\\midrule\endhead" + "\n"
    for b, (nom, lst) in BLOCS.items():
        s += rf"\multicolumn{{7}}{{@{{}}l}}{{\textbf{{\color{{uimm}}Bloc {b} · {tex(nom)}}} \quad ({sum(a['duree'] for a in lst)} min)}}\\" + "\n"
        for a in lst:
            s += rf"{a['code']} & {tex(a['titre'])} & {a['duree']} min & {ORG[a['org']['mode']]} & {a['niveau']} & {'oui' if a['ellistat'] else ''} & {'oui' if a['mesure'] else ''}\\" + "\n"
    return s + r"\bottomrule\end{longtable}}"

def catalogue():
    out = []
    for b, nom, a in toutes():
        liens = []
        for lab, h in a['liens']:
            liens.append([lab, h[3:] if h.startswith('../') else 'Activites/' + h])
        out.append(dict(code=a['code'], bloc=b, blocNom=nom, titre=a['titre'], question=a['question'], niveau=a['niveau'], duree=a['duree'], org=a['org'], ellistat=a['ellistat'], mesure=a['mesure'],
                        but=a['but'], materiel=a['materiel'], besoin=a['besoin'], fiche='Activites/' + nomfiche(a) + '.pdf', liens=liens, **({'note': a['note']} if a.get('note') else {})))
    return out

if __name__ == '__main__':
    ecrire_fiches()
    open(os.path.join(TEX, 'guide_corps.tex'), 'w', encoding='utf-8').write(guide())
    open(os.path.join(TEX, 'guide_tableau.tex'), 'w', encoding='utf-8').write(tableau_activites())
    json.dump(catalogue(), open(os.path.join(ICI, 'catalogue.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    tot = {b: sum(a['duree'] for a in lst) for b, (nom, lst) in BLOCS.items()}
    print(len(toutes()), 'activités ;', tot, '; total', sum(tot.values()), 'min')
