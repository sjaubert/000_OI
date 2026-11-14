# Génère la trame de journée à 8 h 20 (plan + banque de réserves) pour le formateur
import os
T = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tex')

# (type, code, titre, durée) ; type : B bloc, S socle, R réserve de rang 1 planifiée, F bilan
PLAN = [
 ('B', '', 'Bloc 1 · Prendre Ellistat en main', 0),
 ('S', 'E1', 'Mon premier projet', 10),
 ('S', 'E2', 'Saisir, coller, corriger', 15),
 ('S', 'E3', 'Régler une colonne', 15),
 ('S', 'E4', 'Mon premier histogramme', 20),
 ('B', '', 'Bloc 2 · Nos instruments sont-ils capables ? (en binôme)', 0),
 ('S', 'M1', 'La résolution d\'abord', 15),
 ('S', 'M2', 'Dix mesures, une cale', 20),
 ('S', 'TP 1 (M3)', 'Mon micromètre est-il juste ?', 45),
 ('S', 'TP 2 (M7)', 'Jusqu\'où peut-il aller ?', 15),
 ('S', 'TP 3 (M4)', 'Pied à coulisse contre micromètre', 30),
 ('S', 'TP 4 (M5)', 'Avec ou sans cliquet', 30),
 ('S', 'TP 5 (M6)', 'La cale dans la main', 25),
 ('R', 'M16', 'Deux grades, un micromètre (cales 0 et 1)', 30),
 ('R', 'M9', 'Deux opérateurs, une cale', 30),
 ('B', '', 'Bloc 3 · Compter les défauts', 0),
 ('S', 'A1', 'Défectueuse ou défauts ?', 15),
 ('S', 'A2', 'Ma première carte p, à la main', 35),
 ('S', 'A3', 'La même carte dans Ellistat', 20),
 ('S', 'A4', 'Le procédé se dérègle', 30),
 ('S', 'A6', 'Compter les défauts : la carte c', 30),
 ('R', 'A5', 'p ou np ? Et si les lots changent de taille ?', 25),
 ('B', '', 'Bloc 4 · Lire une carte, sans logiciel', 0),
 ('R', 'C1', 'La carte sonne-t-elle ?', 30),
 ('F', '', 'Bilan : un résultat et une décision par binôme', 15),
]

# banque : (bloc, code, titre, durée, quand / remarque)
BANQUE = [
 ('Ellistat', 'E5', 'Une ligne, un sous-groupe', 20, 'niveau 2, sur le bloc 1 si le groupe est à l\'aise'),
 ('Ellistat', 'E6', 'Garder une trace', 10, 'écran non vérifié : à essayer avant'),
 ('Instruments', 'M8', 'Juste partout ?', 45, 'cinq cales, linéarité ; écrans vus le 14/11 ; niveau 3'),
 ('Instruments', 'M10', 'Fabriquer son étalon', 25, 'coffret de 83 cales ; à faire avant M14'),
 ('Instruments', 'M14', 'Trois étalons pour la butée', 60, 'après M10 ; la réserve la plus longue du bloc 2 qui reste concrète'),
 ('Instruments', 'M13', 'Bon ou mauvais : sommes-nous d\'accord ?', 45, 'niveau 3 ; seule réserve qui exige 20 butées physiques numérotées, dont plusieurs proches de 11,85 et 12,00, et un pied à coulisse par contrôleur'),
 ('Instruments', 'M15', 'Le micromètre dérive-t-il ?', 60, 'fil rouge possible : une cale témoin mesurée 3 fois dans la journée ; carte X-barre R en fin de journée ; niveau 3'),
 ('Attributs', 'A9', 'La taille du lot compte', 20, 'sans Ellistat, après A4'),
 ('Attributs', 'A7', 'La carte u', 25, 'niveau 3, après A6'),
 ('Attributs', 'A8', 'Quelle période de référence ?', 25, 'après A4'),
 ('Cartes aux mesures', 'C2', 'La machine est-elle capable ?', 30, 'Cp et Cpk à la main, niveau 1'),
 ('Cartes aux mesures', 'C3', 'La voiture et le garage', 30, 'simulateur, niveau 2, après C2'),
 ('Cartes aux mesures', 'C6', 'Cinquante butées qui dérivent', 30, 'niveau 2, après C2'),
 ('Cartes aux mesures', 'C4', 'Ma carte, à la main puis dans Ellistat', 60, 'niveau 2, calculs longs'),
 ('Cartes aux mesures', 'C7', 'Trois enquêtes', 60, 'niveau 2, présentation de 5 minutes'),
]

def hm(m):
    return '%d h %02d' % (m // 60, m % 60)

def tex_plan():
    rows = []; cum = 0; socle = 0; res = 0
    for t, c, ti, d in PLAN:
        if t == 'B':
            rows.append('\\rowcolor{fond}\\multicolumn{6}{|l|}{\\textbf{\\color{uimm}%s}}\\\\ \\hline' % ti)
            continue
        cum += d
        if t == 'S' or t == 'F': socle += d
        if t == 'R': res += d
        tag = {'S': '', 'R': 'R1', 'F': ''}[t]
        fill = '\\rowcolor{orange!10}' if t == 'R' else ''
        rows.append('%s%s & %s & %d min & %s & %s & \\\\ \\hline' % (fill, c, ti, d, hm(cum), tag))
    return '\n'.join(rows), cum, socle, res

def tex_banque():
    rows = []; tot = 0; cur = None
    for b, c, ti, d, q in BANQUE:
        if b != cur:
            rows.append('\\rowcolor{fond}\\multicolumn{4}{|l|}{\\textbf{\\color{uimm}%s}}\\\\ \\hline' % b); cur = b
        tot += d
        rows.append('%s & %s & %d min & %s \\\\ \\hline' % (c, ti, d, q))
    return '\n'.join(rows), tot

def build():
    plan, cum, socle, res = tex_plan()
    banque, tot = tex_banque()
    src = r'''\documentclass[10pt,a4paper]{article}
\input{commun.tex}
\usepackage{colortbl}
\pied{Journée du 25/11/2026 · Trame de 8 h 20 et réserves · formateur}
\begin{document}
\thispagestyle{fancy}
\bandeau{Journée du 25/11/2026 · 4 stagiaires · formateur}{Trame de %(hcum)s et banque de réserves}{Si le groupe va vite, on ne s'arrête pas : on prend la réserve suivante}
\vspace{2pt}
\begin{tcolorbox}[boite,left=5pt,right=5pt,top=2pt,bottom=2pt]\small
\textbf{Principe.} Le plan ci-dessous fait \textbf{%(hcum)s} d'activités, pauses non comprises : le tronc de %(hsocle)s (bilan compris) plus %(hres)s de réserves de rang 1 (lignes orangées) placées là où elles prolongent le sujet. En dessous, une banque de %(hbanque)s de réserves classées par bloc. Les durées sont celles des fiches, prévues pour un groupe moyen : tu as observé que ce groupe va plus vite. Note la durée réelle de chaque activité dans la dernière colonne : ce sera ta mesure pour la prochaine fois.
\end{tcolorbox}
\par\vspace{4pt}
\renewcommand{\arraystretch}{1.28}\small
\begin{tabularx}{\linewidth}{|>{\bfseries}p{19mm}|>{\raggedright\arraybackslash}X|r|r|c|p{17mm}|}\hline
\rowcolor{uimm}\color{white}\textbf{Fiche} & \color{white}\textbf{Activité} & \color{white}\textbf{Prévu} & \color{white}\textbf{Cumul} & \color{white}\textbf{Rang} & \color{white}\textbf{Réel}\\\hline
%(plan)s
\end{tabularx}
\par\smallskip
\footnotesize Les TP 1 à 5 sont les trames terrain d'une page (fiches M3, M7, M4, M5, M6). Les durées des TP sont celles des trames, plus courtes que celles des fiches. Les pauses et les consignes de début de journée ne sont pas comptées.
\newpage
\titre{Banque de réserves, par bloc}
\renewcommand{\arraystretch}{1.28}\small
\begin{tabularx}{\linewidth}{|>{\bfseries}p{11mm}|>{\raggedright\arraybackslash}p{58mm}|r|>{\raggedright\arraybackslash}X|}\hline
\rowcolor{uimm}\color{white}\textbf{Fiche} & \color{white}\textbf{Activité} & \color{white}\textbf{Durée} & \color{white}\textbf{Quand, remarque}\\\hline
%(banque)s
\end{tabularx}
\par\smallskip
\footnotesize Total de la banque : %(hbanque)s, soit au total %(htout)s avec le plan. Les fiches M11, M12, M17, C5 et C8 (R\&R complet, trois cales, dossier complet) ne sont pas dans la banque : trop avancées pour ce groupe.

\titre{Règles de bascule}
\begin{enumerate}[leftmargin=16pt,itemsep=2pt]
\item \textbf{À la fin de chaque bloc}, compare le cumul réel au cumul prévu. En avance de 10 minutes ou plus : lance la réserve suivante \emph{du même bloc} avant de passer au bloc suivant. Prolonger un sujet connu perd moins le groupe qu'ouvrir une notion nouvelle.
\item \textbf{Ordre des réserves}. Instruments : M10, M14, M8, M13. Attributs : A9, A8, A7. Cartes aux mesures : C2, C3, C6, puis C4 ou C7. Les réserves de rang 1 du plan passent avant celles de la banque.
\item \textbf{Si la séance va vite dès le matin} : ajoute E5 au bloc 1, puis M10 et M14 au bloc 2 (cales et coffret, activité très concrète).
\item \textbf{Si le groupe est en retard} : retire d'abord les réserves de rang 1, puis TP 5, puis A6. Le tronc minimal reste E1 à E3, M1, TP 1, TP 4, A1, A2, A4.
\item \textbf{À placer en fin de journée} : un bilan de 15 minutes, jamais une activité nouvelle.
\end{enumerate}

\titre{Ce qui reste à vérifier avant la séance}
\begin{itemize}[leftmargin=14pt,itemsep=1pt]
\item Les durées des fiches sont des estimations, pas des temps mesurés avec ce groupe.
\item Les écrans Ellistat ont été vus pour les fiches E1 à E3, M3, M8, M13, A3 à A8. Ceux de E4 (avec tolérances), E6 et des réserves M10, M14, M15, C4, C6 et C7 sont à dérouler une fois sur ton compte.
\item Butées : aucune n'est nécessaire pour le plan ; seule M13 en demande 20. Les « 30 butées » de E3, E4, E5, C4 et C6 sont des données numériques. Autre matériel : le coffret de 83 cales sert à M10 et M14. Les cales de grade 0 et 1 servent à M16. M9 et M15 demandent deux personnes par instrument.
\end{itemize}
\end{document}
''' % dict(plan=plan, banque=banque, hcum=hm(cum), hsocle=hm(socle), hres=hm(res), hbanque=hm(tot), htout=hm(cum + tot))
    open(os.path.join(T, 'Trame_journee_8h_formateur.tex'), 'w', encoding='utf-8').write(src)
    print('plan', cum, 'socle', socle, 'res', res, 'banque', tot)

if __name__ == '__main__':
    build()
