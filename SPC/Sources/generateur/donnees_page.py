import json, html
J=json.load(open('donnees_base.json'))
GR=[("Butées : cartes aux mesures et capabilité",[('butees30','30 butées en une colonne, dans l\'ordre de fabrication'),('butees6','30 butées, 6 sous-groupes de 5'),('decoupage','Les mêmes 30 butées, mal regroupées'),('butees10','50 butées, 10 sous-groupes de 5')]),
 ("Trois enquêtes sur cartes",[('pression','Pression du réservoir (24 jours × 5)'),('dimension','Dimension usinée (27 × 5, valeurs codées)'),('liquide','Liquide par lots (17 valeurs)')]),
 ("Moyen de mesure",[('justesse','Justesse : cale 6,002 mm, 50 mesures (livret Bosch p. 11)'),('rr','R&R : 10 pièces, 3 opérateurs, 2 séries (livret Bosch p. 14)'),('lin','Linéarité : 5 cales × 10 mesures (simulé)'),
   ('instr','Secours : micromètre et pied à coulisse sur une cale de 10 mm (simulé)'),('cliquet','Secours : avec et sans cliquet, cale de 10 mm (simulé)'),('operateurs','Secours : deux opérateurs, cale de 10 mm (simulé)'),('chauffe','Secours : cale de 25 mm réchauffée dans la main (simulé)'),
   ('etalons','Secours : trois étalons 11,850 ; 11,925 ; 12,000 mm, 10 mesures chacun (simulé)'),('derive','Dérive : cale témoin de 10 mm, 8 passages de 5 mesures (simulé)'),('grades','Secours : cale céramique grade 0 et cale acier grade 1, 15 mesures chacune (simulé)'),('rrcotes','R&R : 10 cales de cotes connues 1,01 à 1,10 mm, 3 opérateurs, 2 séries (simulé)'),('s5just','Synthèse : justesse sur cale de 12,000 mm (simulé)'),('s5rr','Synthèse : R&R sur 10 butées (simulé)')]),
 ("Cartes aux attributs",[('lots35','35 lots de 50 pièces (simulé)'),('lotsvar','25 lots de taille variable (simulé)'),('inspection','120 lots de 150 pièces'),('panneaux','Défauts d\'aspect sur 30 panneaux (simulé)'),('rouleaux','Défauts sur 25 rouleaux de longueur variable (simulé)')])]
DECS={'instr':[3,2],'chauffe':[0,3]}
def fmt(v,dec):
    return ('%.*f'%(dec,v)).replace('.',',') if isinstance(v,float) else str(v)
def ligne(k,r):
    d=DECS.get(k); return [fmt(x,d[i] if d else J[k]['dec']) for i,x in enumerate(r)]
def tableau(k):
    d=J[k]; h='<table><thead><tr>'+''.join(f'<th>{html.escape(x)}</th>' for x in d['entete'])+('<th></th>' if k=='lin' else '')+'</tr></thead><tbody>'
    for i,r in enumerate(d['lignes']):
        h+='<tr>'+''.join(f'<td>{v}</td>' for v in ligne(k,r))+(f'<td><button class="mini" data-k="{k}" data-ligne="{i}">Copier les 10 mesures</button></td>' if k=='lin' else '')+'</tr>'
    return h+'</tbody></table>'
corps=''
for titre,jeux in GR:
    corps+=f'<section class="groupe"><h2>{html.escape(titre)}</h2>'
    for k,lib in jeux:
        corps+=f'''<details class="jeu" id="{k}"><summary>{html.escape(lib)}</summary><div class="outils"><a class="dl" href="../Donnees_Ellistat/{J[k]['nom']}" download>Télécharger {J[k]['nom']}</a><button class="copier" data-k="{k}">Copier le tableau</button><span class="ok" aria-live="polite"></span></div><div class="defile">{tableau(k)}</div></details>'''
    corps+='</section>'
assert set(k for _,j in GR for k,_ in j)==set(J), set(J)-set(k for _,j in GR for k,_ in j)
data=json.dumps({k:{'entete':v['entete'],'lignes':[ligne(k,r) for r in v['lignes']]} for k,v in J.items()},ensure_ascii=False)
page='''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Données à copier</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:wght@600;700&family=Source+Sans+3:wght@400;600;700&family=IBM+Plex+Mono:wght@400&display=swap">
<style>
:root{--papier:#F6F8F7;--encre:#17324D;--trait:#5B6B7A;--grille:#D9E2E0;--fond:#E9EEED;--carte:#FFFFFF;--accent:#1F4E79;--ok:#2E7D32;--uimm:#005677;
--f-titre:"Barlow Semi Condensed","Arial Narrow",Arial,sans-serif;--f-texte:"Source Sans 3","Segoe UI",Arial,sans-serif;--f-chiffre:"IBM Plex Mono",Consolas,monospace;color-scheme:light}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--papier:#16201F;--encre:#DCE8F2;--trait:#9AABB8;--grille:#2C3A36;--fond:#0F1716;--carte:#1B2625;--accent:#8DB8E6;--ok:#7CC283;--uimm:#4FA3C7;color-scheme:dark}}
:root[data-theme="dark"]{--papier:#16201F;--encre:#DCE8F2;--trait:#9AABB8;--grille:#2C3A36;--fond:#0F1716;--carte:#1B2625;--accent:#8DB8E6;--ok:#7CC283;--uimm:#4FA3C7;color-scheme:dark}
*{box-sizing:border-box} body{margin:0;background:var(--fond);color:var(--encre);font-family:var(--f-texte);font-size:16px;line-height:1.5}
.page{max-width:980px;margin:0 auto;padding:22px max(16px,env(safe-area-inset-left,0px)) 48px max(16px,env(safe-area-inset-right,0px));display:grid;gap:16px}
h1{font-family:var(--f-titre);font-size:clamp(1.8rem,4vw,2.4rem);margin:0;line-height:1.05} header p{margin:6px 0 0;color:var(--trait)}
.aide{background:var(--carte);border-left:4px solid var(--uimm);border-radius:0 8px 8px 0;padding:10px 16px} .aide p{margin:2px 0}
.groupe{background:var(--carte);border:1px solid var(--grille);border-radius:10px;padding:14px 16px;display:grid;gap:8px}
.groupe h2{font-family:var(--f-titre);font-size:1.35rem;margin:0}
details.jeu{border:1px solid var(--grille);border-radius:8px;background:var(--papier);scroll-margin-top:10px} details.jeu summary{cursor:pointer;padding:8px 12px;font-weight:600}
.outils{display:flex;flex-wrap:wrap;gap:8px;align-items:center;padding:0 12px 8px}
a.dl{text-decoration:none;color:var(--encre);background:var(--carte);border:1.5px solid var(--grille);border-radius:8px;padding:5px 10px;font-weight:600;font-size:.88rem}
button{font:inherit;cursor:pointer;border-radius:8px} button.copier{background:var(--uimm);color:#fff;border:none;padding:6px 12px;font-weight:600;font-size:.88rem}
button.mini{background:transparent;color:var(--accent);border:1.5px solid var(--accent);padding:2px 8px;font-size:.8rem}
.ok{color:var(--ok);font-size:.88rem} .defile{overflow-x:auto;padding:0 12px 12px}
table{border-collapse:collapse;font-family:var(--f-chiffre);font-size:.85rem} th,td{border-bottom:1px solid var(--grille);padding:3px 8px;text-align:right;white-space:nowrap} th{font-family:var(--f-texte);color:var(--trait)}
label.sep{display:inline-flex;gap:6px;align-items:center;font-size:.92rem} select{font:inherit;color:var(--encre);background:var(--carte);border:1.5px solid var(--grille);border-radius:6px;padding:4px 6px}
a:focus-visible,button:focus-visible,summary:focus-visible,select:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.retour{color:var(--accent)}
</style></head><body><div class="page">
<header><p style="margin:0"><a class="retour" href="../index.html">Retour au catalogue des activités</a></p><h1>Données à copier</h1>
<p>Tous les jeux de données de la base, prêts pour Ellistat. Aucun passage par Excel.</p></header>
<section class="aide"><p><b>Deux façons de faire.</b> Télécharger le fichier, puis dans Ellistat : menu en haut à droite de la grille, « Importer depuis Excel ». Ou cliquer sur « Copier le tableau », puis coller dans la grille d'Ellistat.</p>
<p><label class="sep" for="sep">Séparateur décimal pour la copie : <select id="sep"><option value=",">virgule (11,87)</option><option value=".">point (11.87)</option></select></label></p></section>
'''+corps+'''
<p style="font-size:.82rem;color:var(--trait)">Sources : exemples p. 11 et p. 14 de Robert Bosch GmbH, <i>Booklet 10 : Capability of Measurement and Test Processes</i>, édition novembre 2019. Les jeux marqués « simulé » sont fictifs, tirés avec une graine fixe.</p>
</div>
<script>
(function(){"use strict";var D='''+data+''';
function tsv(k,ligne){var d=D[k],sep=document.getElementById("sep").value,f=function(x){return sep==="."?String(x).replace(",","."):x;};if(ligne!==undefined)return d.lignes[ligne].slice(1).map(f).join("\\t");return [d.entete.join("\\t")].concat(d.lignes.map(function(r){return r.map(f).join("\\t");})).join("\\n");}
function copier(t,el){function fini(m){if(el){el.textContent=m;setTimeout(function(){el.textContent="";},2500);}}
 function secours(){var a=document.createElement("textarea");a.value=t;a.setAttribute("readonly","");a.style.position="fixed";a.style.opacity="0";document.body.appendChild(a);a.select();try{document.execCommand("copy");fini("Copié.");}catch(e){fini("Copie impossible : sélectionnez le tableau.");}document.body.removeChild(a);}
 if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(t).then(function(){fini("Copié.");},secours);}else secours();}
document.querySelectorAll("button.copier").forEach(function(b){b.addEventListener("click",function(){copier(tsv(b.dataset.k),b.parentNode.querySelector(".ok"));});});
document.querySelectorAll("button.mini").forEach(function(b){b.addEventListener("click",function(){copier(tsv(b.dataset.k,+b.dataset.ligne),b.closest("details").querySelector(".ok"));});});
if(location.hash){var c=document.getElementById(location.hash.slice(1));if(c&&c.tagName==="DETAILS")c.open=true;}
window.__donnees={tsv:tsv};
})();
</script></body></html>'''
open('SPC/Pages/Donnees_a_copier.html','w',encoding='utf-8').write(page); print('ok',len(page))
