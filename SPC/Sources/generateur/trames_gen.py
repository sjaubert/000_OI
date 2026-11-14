# Génère les trames « terrain » (une page par TP) et la page de repères du formateur
import os, subprocess, glob
T = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tex')

def grille(n, cols):
    rows = []
    cells = ['\\rule{0pt}{8.5mm}{\\tiny\\color{gray}%d}' % (i + 1) for i in range(n)]
    for r in range(0, n, cols):
        row = cells[r:r + cols]
        row += [''] * (cols - len(row))
        rows.append(' & '.join(row) + ' \\\\ \\hline')
    spec = '|' + 'p{%dmm}|' % int(170 / cols - 3) * cols
    return '\\par\\vspace{2pt}{\\setlength{\\tabcolsep}{2pt}\\begin{tabular}{%s}\\hline\n%s\n\\end{tabular}}\\par' % (spec, '\n'.join(rows))

def temps_table():
    heads = ['0', '30', '60', '90', '120', '150', '180', '210', '240', '270', '300']
    top = ' & '.join('\\textbf{%s}' % h for h in heads)
    return ('\\par\\vspace{2pt}{\\setlength{\\tabcolsep}{2pt}\\renewcommand{\\arraystretch}{1.1}'
            '\\begin{tabular}{|l|' + 'p{11.3mm}|' * 11 + '}\\hline\n'
            '\\textbf{Temps (s)} & ' + top + ' \\\\ \\hline\n'
            '\\rule{0pt}{8mm}\\textbf{Mesure} & ' + ' & '.join([''] * 11) + ' \\\\ \\hline\n\\end{tabular}}\\par')

HEAD = r'''\documentclass[11pt,a4paper]{article}
\input{trame.tex}
\pied{Journée du 25/11/2026 · Trame terrain %(num)s · %(titre)s}
\begin{document}
\thispagestyle{fancy}
\bandeau{Journée du 25/11/2026 · TP %(num)s sur 5 · durée %(duree)s · en binôme}{%(titre)s}{%(question)s}
\vspace{-2pt}
\begin{tcolorbox}[boite,left=5pt,right=5pt,top=2pt,bottom=2pt]\small\textbf{Il vous faut.} %(materiel)s\end{tcolorbox}
'''

TPS = []

TPS.append(dict(num='1', fichier='Trame_TP1_micrometre_juste', titre='Mon micromètre est-il juste ?',
 question='Puis-je me fier à ce micromètre pour contrôler une pièce à 0,15 mm de tolérance ?', duree='45 min',
 materiel='un micromètre 0-25 mm (notez son numéro), la cale de 10 mm, un chiffon ou des gants, Ellistat.',
 corps=r'''
\etape{1}{Je prédis}
Mon micromètre sera-t-il capable pour une tolérance de 0,15 mm ?\quad \cb oui \quad \cb non \quad \cb je ne sais pas
\etape{2}{Je mesure}
Mesurer la cale de 10 mm \textbf{25 fois}, au cliquet. \textbf{Retirer puis remettre la cale} à chaque mesure. Noter toutes les valeurs, avec les trois décimales (10,000 et non 10). Micromètre n° \champ{15mm}
''' + grille(25, 7) + r'''
\etape{3}{Je saisis dans Ellistat}
\begin{enumerate}[label=\textbf{\alph*.},leftmargin=16pt,itemsep=1pt]
\item \menu{Gage R\&R}, onglet \menu{Justesse}, bouton \menu{ajouter une justesse}.
\item Remplir : \textbf{Nom} = votre prénom ; \textbf{Nombre de mesures} 25 ; \textbf{Valeur vraie} 10,000 ; \textbf{LSI} 9,925 ; \textbf{LSS} 10,075 ; \textbf{Valeur de k} 3. Valider.
\item Taper les 25 mesures dans la liste « Mesures », une par ligne, avec toutes les décimales.
\end{enumerate}
\etape{4}{Je lis un seul chiffre}
\chiffre{Dans le tableau « Résultats statistiques », ligne \textbf{Cgk} :\hfill Cgk = \champ{30mm}\hfill\ \par\smallskip\small Repère du livret Bosch : un instrument est capable quand Cgk dépasse \textbf{1,33}.}
\etape{5}{Je décide}
Pour une tolérance de 0,15 mm, mon micromètre est\quad \cb capable \quad \cb pas capable.\quad Ma prédiction était\quad \cb juste \quad \cb fausse.
\par\vspace{2pt}
\motnouveau{\textbf{Cgk} : une note unique pour dire si l'instrument est à la fois \emph{groupé} (mêmes valeurs d'une mesure à l'autre) et \emph{centré} (proche de la vraie valeur de la cale).}
'''))

TPS.append(dict(num='4', fichier='Trame_TP4_avec_ou_sans_cliquet', titre='Avec ou sans cliquet',
 question='La façon de serrer change-t-elle la mesure ?', duree='30 min',
 materiel='le même micromètre à cliquet, la même cale de 10 mm, Ellistat. Même opérateur pour les deux séries.',
 corps=r'''
\etape{1}{Je prédis}
Si je serre à la main, sans le cliquet, mes valeurs seront :\quad \cb plus grandes \quad \cb plus petites \quad \cb plus dispersées \quad \cb pareilles
\etape{2}{Je mesure}
\textbf{Série A, avec le cliquet} : 15 mesures, toujours le même nombre de crans. \textbf{Série B, sans le cliquet} : 15 mesures en serrant le tambour à la main, comme d'habitude, sans forcer. Retirer la cale à chaque mesure. Noter les trois décimales.
\par\smallskip\textbf{Série A (avec cliquet)}
''' + grille(15, 8) + r'''
\par\smallskip\textbf{Série B (sans cliquet)}
''' + grille(15, 8) + r'''
\etape{3}{Je saisis dans Ellistat}
\begin{enumerate}[label=\textbf{\alph*.},leftmargin=16pt,itemsep=1pt]
\item Dans une grille, deux colonnes nommées \textbf{Cliquet} et \textbf{Main} : taper les 15 valeurs de chaque série.
\item \menu{Stats Desc.}, onglet \menu{Détail}. Cliquer sur le nom de la colonne dans la liste « Échantillons » à gauche.
\end{enumerate}
\etape{4}{Je lis un seul chiffre}
\chiffre{Dans le tableau « PARAMÈTRES », ligne \textbf{Ecart type}, pour chaque série :\par\medskip
Avec cliquet : \champ{28mm}\hfill Sans cliquet : \champ{28mm}\hfill\ }
\etape{5}{Je décide}
La série la plus dispersée est\quad \cb avec cliquet \quad \cb sans cliquet.\par\smallskip
Consigne à afficher au poste (une phrase) : \par\vspace{1pt}\reponse[2]
\motnouveau{\textbf{Écart type} : la taille de la dispersion des mesures. Plus il est petit, plus les valeurs sont groupées. Les deux séries sont mesurées par la même personne : seule la façon de serrer change.}
'''))

TPS.append(dict(num='5', fichier='Trame_TP5_cale_dans_la_main', titre='La cale dans la main',
 question='La chaleur des doigts se voit-elle au micromètre ?', duree='25 min',
 materiel='un micromètre, la cale la plus longue qu\'il peut mesurer (20 mm au 0-25, 30 mm au 25-50), un chronomètre, Ellistat.',
 corps=r'''
\etape{1}{Je prédis}
Une cale d'acier tenue 3 minutes dans la main fermée s'allonge de (1 µm = 0,001 mm) :\par\smallskip\cb 0,1 µm \quad \cb 3 µm \quad \cb 30 µm \quad \cb pas du tout
\etape{2}{Je mesure}
\begin{enumerate}[label=\textbf{\alph*.},leftmargin=16pt,itemsep=1pt]
\item Mesurer \textbf{3 fois} la cale à la température de la salle. Moyenne = \textbf{référence} : \champ{25mm} mm
\item Garder la cale \textbf{3 minutes} dans la main fermée.
\item La poser et la mesurer \textbf{aussitôt}, puis toutes les 30 secondes pendant 5 minutes, sans la reprendre en main.
\end{enumerate}
''' + temps_table() + r'''
\etape{3}{Je saisis dans Ellistat}
Dans une grille, une colonne \textbf{Chaleur} : taper les 11 mesures \textbf{dans l'ordre du temps}. \menu{Stats Desc.}, onglet \menu{Détail}, cliquer sur la colonne : le graphique « Moyenne » montre les points dans l'ordre. Dessiner ci-dessous l'allure de la courbe :
\par\vspace{2pt}\fbox{\rule{0pt}{20mm}\rule{0.97\linewidth}{0pt}}
\etape{4}{Je calcule un seul chiffre}
\chiffre{Allongement = première mesure après la main $-$ référence\hfill = \champ{25mm} µm\hfill\ \par\smallskip\small Repère : l'acier s'allonge d'environ 11,5 µm par mètre et par degré (valeur usuelle, à confirmer chez le fabricant des cales). Pour 30 mm, cela fait environ 0,35 µm par degré.}
\etape{5}{Je décide}
Au poste, avant de mesurer une pièce que l'on vient de tenir en main, j'attends \champ{14mm} minutes.\par\smallskip
Une précaution à retenir :\par\vspace{1pt}\reponse[1]
\motnouveau{\textbf{Température de référence} : les cales et les pièces sont définies à 20 °C. Au millième, une pièce plus chaude est une pièce plus longue.}
'''))

TPS.append(dict(num='3', fichier='Trame_TP3_pied_a_coulisse', titre='Pied à coulisse contre micromètre',
 question='Deux instruments, une cale : lequel croire ?', duree='30 min',
 materiel='un pied à coulisse au 1/50, la cale de 10 mm, votre Cgk du TP 1, Ellistat.',
 corps=r'''
\etape{1}{Je prédis}
Les mesures les plus groupées viendront du :\quad \cb micromètre \quad \cb pied à coulisse \quad \cb pareil
\etape{2}{Je mesure}
Mesurer la cale de 10 mm \textbf{15 fois au pied à coulisse}. Retirer la cale à chaque mesure. Noter toutes les décimales lues (10,00 ou 10,02).
''' + grille(15, 8) + r'''
\etape{3}{Je saisis dans Ellistat}
\begin{enumerate}[label=\textbf{\alph*.},leftmargin=16pt,itemsep=1pt]
\item \menu{Gage R\&R}, onglet \menu{Justesse}, bouton \menu{ajouter une justesse}.
\item \textbf{Nom} = Pied à coulisse ; \textbf{Nombre de mesures} 15 ; \textbf{Valeur vraie} 10,000 ; \textbf{LSI} 9,925 ; \textbf{LSS} 10,075 ; \textbf{Valeur de k} 3. Valider.
\item Taper les 15 mesures dans la liste « Mesures », avec toutes les décimales lues.
\end{enumerate}
\etape{4}{Je lis un seul chiffre}
\chiffre{Dans le tableau « Résultats statistiques », ligne \textbf{Cgk} du pied à coulisse :\hfill Cgk = \champ{30mm}\hfill\ \par\smallskip\small Pour comparer : le Cgk de mon micromètre (TP 1) vaut \champ{25mm}. Repère du livret Bosch : capable au-dessus de \textbf{1,33}.}
\etape{5}{Je décide}
Pour 0,15 mm de tolérance, le pied à coulisse est\quad \cb capable \quad \cb pas capable.\par\smallskip
Règle simple du livret Bosch : la résolution de l'instrument ne doit pas dépasser \textbf{5 \%} de la tolérance. Pour le pied à coulisse (résolution 0,02 mm), la plus petite tolérance contrôlable est $0{,}02 / 0{,}05 =$ \champ{14mm} mm.
\par\vspace{2pt}
\motnouveau{\textbf{Résolution} : le plus petit pas que l'instrument sait lire (0,02 mm au pied à coulisse, 0,001 mm à votre micromètre). Un instrument n'est ni bon ni mauvais : il est capable ou non \emph{pour une tolérance donnée}.}
'''))

TPS.append(dict(num='2', fichier='Trame_TP2_jusqu_ou_peut_il_aller', titre='Jusqu\'où peut-il aller ?',
 question='Quelle est la plus petite tolérance que mon micromètre peut contrôler ?', duree='15 min',
 materiel='l\'étude « Justesse » du TP 1 dans Ellistat. Aucune nouvelle mesure.',
 corps=r'''
\etape{1}{Je prédis}
Mon micromètre est capable pour 0,15 mm de tolérance. Le sera-t-il encore pour :
\par\smallskip\renewcommand{\arraystretch}{1.5}\begin{tabular}{|c|c|c|}\hline \textbf{Tolérance} & \textbf{Ma prédiction} & \textbf{Résultat (étape 5)}\\\hline
0,05 mm & \cb oui \quad \cb non & \cb oui \quad \cb non\\\hline
0,02 mm & \cb oui \quad \cb non & \cb oui \quad \cb non\\\hline
0,01 mm & \cb oui \quad \cb non & \cb oui \quad \cb non\\\hline\end{tabular}
\etape{2}{Je mesure}
Rien à mesurer : on réutilise les 25 mesures du TP 1.
\etape{3}{J'ouvre mon étude dans Ellistat}
\menu{Gage R\&R}, onglet \menu{Justesse}. Choisir votre étude dans la liste en haut à gauche, puis lire le tableau « Résultats statistiques ».
\etape{4}{Je lis un seul chiffre}
\chiffre{Ligne \textbf{Tolerance min} :\hfill Tolerance min = \champ{30mm} mm\hfill\ \par\smallskip\small C'est la plus petite tolérance pour laquelle ce micromètre, avec ma façon de mesurer, reste capable.}
\etape{5}{Je décide}
Règle : une tolérance est contrôlable si elle est \textbf{supérieure ou égale} à la Tolerance min. Compléter la colonne « Résultat » du tableau de l'étape 1.
\par\bigskip
Avec ce micromètre, je peux contrôler une cote jusqu'à une tolérance de \champ{22mm} mm.\par\medskip
Ma prédiction était\quad \cb juste \quad \cb à corriger.\par\bigskip
Une cote de mon poste a une tolérance de \champ{18mm} mm : je la contrôle avec ce micromètre ?\quad \cb oui \quad \cb non
\par\vspace{4pt}
\motnouveau{\textbf{Tolerance min} : ce chiffre ne dépend que de la dispersion de vos mesures et de leur décalage avec la cale, pas de la tolérance que vous avez saisie. Un même instrument passe pour une cote et échoue pour une autre.}
'''))

FORMATEUR = r'''\documentclass[10pt,a4paper]{article}
\input{trame.tex}
\pied{Journée du 25/11/2026 · Trames terrain · repères du formateur}
\begin{document}
\thispagestyle{fancy}
\bandeau{Journée du 25/11/2026 · 4 stagiaires}{Trames terrain : repères du formateur}{Cinq TP d'une page, à imprimer en 4 exemplaires}
\titre{Ordre conseillé et durées}
\renewcommand{\arraystretch}{1.35}
\begin{tabularx}{\linewidth}{|c|>{\raggedright\arraybackslash}p{40mm}|c|>{\raggedright\arraybackslash}p{37mm}|>{\raggedright\arraybackslash}X|}\hline
\textbf{TP} & \textbf{Titre (fiche de la base)} & \textbf{Durée} & \textbf{Matériel} & \textbf{Chiffre lu, valeurs du jeu de secours}\\\hline
1 & Mon micromètre est-il juste ? (M3) & 45 min & micromètre 0-25 et cale 10 mm par binôme & Cgk. Secours : 6,02 pour $T = 0{,}15$ (formules du livret Bosch).\\\hline
2 & Jusqu'où peut-il aller ? (M7) & 15 min & aucun & Tolerance min. Secours : 0,036 mm, donc capable à 0,05 et pas à 0,02.\\\hline
3 & Pied à coulisse contre micromètre (M4) & 30 min & pied à coulisse au 1/50 & Cgk du pied à coulisse. Secours : 0,45 : pas capable à 0,15 ; résolution 0,02 permet $T \geq 0{,}4$ mm.\\\hline
4 & Avec ou sans cliquet (M5) & 30 min & mêmes micromètre et cale & Écart type. Secours : 0,0005 avec cliquet contre 0,0023 sans.\\\hline
5 & La cale dans la main (M6) & 25 min & cale longue, chronomètre & Allongement. Secours : environ +3 µm, retour en 3 minutes.\\\hline
\end{tabularx}
\par\smallskip
Le TP 2 vient juste après le TP 1 : il réutilise l'étude sans nouvelle mesure. L'ordre de la journée, les durées et les réserves sont dans la trame de 8 h 20.

\titre{Ce qui reste à vérifier sur ton compte avant la séance}
\begin{itemize}
\item \textbf{Saisie d'une justesse sur une cale de 10 mm} : Ellistat attend une valeur vraie, LSI et LSS. Nous centrons LSI et LSS sur la cale (largeur 0,15). Seule la largeur est confirmée par les formules ; l'effet de la position de LSI et LSS n'a pas été testé.
\item \textbf{Pied à coulisse} : vérifier que les valeurs 10,00 et 10,02 sont acceptées et ce que l'écran affiche. Non vu.
\item \textbf{Onglet Détail avec plusieurs colonnes} (TP 4 et 5) : vu sur une seule colonne. Le clic sur le nom d'une colonne dans la liste « Échantillons » est supposé.
\item \textbf{Seuil 1,33} : c'est celui du livret Bosch. Les seuils de couleur d'Ellistat n'ont pas été lus.
\item \textbf{Valeur des cales} : écart de la valeur vraie à lire sur le certificat des cales ; à défaut, la valeur nominale est utilisée et le dire.
\item \textbf{TP 5} : la dilatation de 11,5 µm par mètre et par degré est une valeur usuelle de l'acier, à confirmer sur la documentation de tes cales. Avec une cale de 20 mm, l'effet n'est que d'environ 0,23 µm par degré : la cale de 30 mm (micromètre 25-50, un seul) montre mieux, avec une rotation.
\item \textbf{Frappe de 25 valeurs} : prévoir un secrétaire par binôme. Le collage d'une liste dans la fenêtre « Justesse » n'a pas été testé.
\end{itemize}
\titre{Comment s'en servir}
Les trames sont des versions courtes de M3, M7, M4, M5 et M6. Les fiches complètes (questions, réponses, « pour aller plus loin ») restent dans le livret et le guide formateur. Chaque trame a une seule lecture dans Ellistat et au plus un mot nouveau. Faire annoncer la prédiction avant de mesurer, et faire dire la décision à voix haute en fin de TP.
\end{document}
'''

def build():
    for tp in TPS:
        src = HEAD % tp + tp['corps'] + '\n\\end{document}\n'
        open(os.path.join(T, tp['fichier'] + '.tex'), 'w', encoding='utf-8').write(src)
    open(os.path.join(T, 'Trame_formateur_reperes.tex'), 'w', encoding='utf-8').write(FORMATEUR)

if __name__ == '__main__':
    build()
    print('tex ok')
