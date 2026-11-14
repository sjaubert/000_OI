import json
CAT=json.load(open('catalogue.json',encoding='utf-8'))
PARC=[["p25","Journée très pratique (7 h)",["E1","E2","E3","E4","M1","M2","M3","M4","M5","M7","M9","A1","A2","A3","A4","A6"]],
 ["pE","Découverte d'Ellistat",["E1","E2","E3","E4","E5","E6"]],
 ["pM","Moyen de mesure, une journée",["E1","E2","E3","M1","M2","M3","M4","M5","M6","M7","M8","M9","M10","M14"]],
 ["pA","Attributs, une demi-journée",["A1","A2","A3","A4","A5","A6","A8","A9"]],
 ["pC","Cartes et capabilité, une journée",["C1","C2","C3","E5","C4","C6","C7"]],
 ["pS","Groupe solide, synthèse",["C5","M8","M13","C8"]],
 ["pK","Étalons et cales de grade 0",["M10","M14","M16","M15","M17"]]]
codes={a['code'] for a in CAT}
for p in PARC: assert set(p[2])<=codes,p
HTML=r'''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Base d'activités SPC</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:wght@600;700&family=Source+Sans+3:wght@400;600;700&display=swap">
<style>
:root{--papier:#F6F8F7;--encre:#17324D;--trait:#5B6B7A;--grille:#D9E2E0;--fond:#E9EEED;--carte:#FFFFFF;--accent:#1F4E79;--accentfond:#DCE7F2;--ok:#2E7D32;--okfond:#E3F1E4;--ko:#B3261E;--kofond:#FBE4E2;--uimm:#005677;
--bE:#13A2DD;--bM:#005677;--bA:#C2610F;--bC:#7B1FA2;
--f-titre:"Barlow Semi Condensed","Arial Narrow",Arial,sans-serif;--f-texte:"Source Sans 3","Segoe UI",Arial,sans-serif;color-scheme:light}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--papier:#16201F;--encre:#DCE8F2;--trait:#9AABB8;--grille:#2C3A36;--fond:#0F1716;--carte:#1B2625;--accent:#8DB8E6;--accentfond:#1E3247;--ok:#7CC283;--okfond:#1D3322;--ko:#F2877E;--kofond:#3A1E1C;--uimm:#4FA3C7;--bE:#4FC3F7;--bM:#4FA3C7;--bA:#F0A257;--bC:#CE93D8;color-scheme:dark}}
:root[data-theme="dark"]{--papier:#16201F;--encre:#DCE8F2;--trait:#9AABB8;--grille:#2C3A36;--fond:#0F1716;--carte:#1B2625;--accent:#8DB8E6;--accentfond:#1E3247;--ok:#7CC283;--okfond:#1D3322;--ko:#F2877E;--kofond:#3A1E1C;--uimm:#4FA3C7;--bE:#4FC3F7;--bM:#4FA3C7;--bA:#F0A257;--bC:#CE93D8;color-scheme:dark}
*{box-sizing:border-box} body{margin:0;background:var(--fond);color:var(--encre);font-family:var(--f-texte);font-size:16px;line-height:1.45}
[hidden]{display:none!important}
.page{max-width:1180px;margin:0 auto;padding:22px max(16px,env(safe-area-inset-left,0px)) 48px max(16px,env(safe-area-inset-right,0px));display:grid;gap:16px}
.page>*{min-width:0}
header .sur{margin:0;font-family:var(--f-titre);font-weight:600;text-transform:uppercase;letter-spacing:.06em;font-size:.9rem;color:var(--trait)}
h1{font-family:var(--f-titre);font-size:clamp(1.9rem,4vw,2.6rem);margin:0;line-height:1.05} header p{margin:6px 0 0;color:var(--trait)}
.regle{background:var(--carte);border-left:4px solid var(--uimm);border-radius:0 8px 8px 0;padding:10px 16px} .regle p{margin:2px 0}
.panneau{background:var(--carte);border:1px solid var(--grille);border-radius:10px;padding:14px 16px;display:grid;gap:12px}
.panneau h2{font-family:var(--f-titre);font-size:1.35rem;margin:0}
.reglages{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px}
label{display:grid;gap:4px;font-size:.92rem;font-weight:600} label small{font-weight:400;color:var(--trait)}
input[type=number],select{font:inherit;color:var(--encre);background:var(--papier);border:1.5px solid var(--grille);border-radius:6px;padding:7px 9px;min-width:0;width:100%}
.puces{display:flex;flex-wrap:wrap;gap:6px}
button{font:inherit;cursor:pointer}
.puce{border:1.5px solid var(--grille);background:var(--papier);color:var(--encre);border-radius:999px;padding:5px 12px;font-size:.9rem}
.puce[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);color:var(--carte);font-weight:600}
.btn{border:none;border-radius:6px;padding:8px 14px;font-family:var(--f-titre);font-weight:600;font-size:1rem;background:var(--accent);color:var(--carte)}
.btn.second{background:transparent;color:var(--accent);border:1.5px solid var(--accent)}
.bilan{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:8px}
.chiffre{background:var(--papier);border:1px solid var(--grille);border-radius:6px;padding:7px 10px}
.chiffre span{display:block;font-size:.74rem;color:var(--trait);text-transform:uppercase;letter-spacing:.05em}
.chiffre b{font-family:var(--f-titre);font-size:1.35rem}
.chiffre.trop{border-color:var(--ko);background:var(--kofond)} .chiffre.bon{border-color:var(--ok);background:var(--okfond)}
.jauge{height:10px;border-radius:5px;background:var(--grille);overflow:hidden} .jauge i{display:block;height:100%;background:var(--ok)} .jauge i.trop{background:var(--ko)}
.materiel{font-size:.93rem;margin:0}
.bloc{display:grid;gap:10px}
.bloc>h2{font-family:var(--f-titre);font-size:1.5rem;margin:8px 0 0;display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
.bloc>h2 small{font-family:var(--f-texte);font-weight:400;font-size:.9rem;color:var(--trait)}
.cartes{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:12px}
.act{background:var(--carte);border:1px solid var(--grille);border-left:5px solid var(--b);border-radius:8px;padding:12px 14px;display:grid;gap:6px;align-content:start}
.act.choisie{box-shadow:0 0 0 2px var(--b)}
.act .tete{display:flex;gap:10px;align-items:flex-start}
.act .code{flex:none;font-family:var(--f-titre);font-weight:700;font-size:1.05rem;color:#fff;background:var(--b);border-radius:6px;padding:2px 8px}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]) .act .code{color:#10201F}}
.act h3{font-family:var(--f-titre);font-size:1.2rem;margin:0;line-height:1.15}
.act .q{margin:0;color:var(--trait);font-style:italic;font-size:.95rem}
.act p{margin:0;font-size:.95rem}
.meta{display:flex;flex-wrap:wrap;gap:6px;font-size:.8rem}
.meta span{background:var(--papier);border:1px solid var(--grille);border-radius:4px;padding:1px 7px;white-space:nowrap}
.meta span.e{border-color:var(--bE)} .meta span.m{border-color:var(--bM)}
.orga{font-size:.9rem;background:var(--accentfond);border-radius:6px;padding:5px 9px}
.liens{display:flex;flex-wrap:wrap;gap:6px}
.liens a{font-size:.88rem;text-decoration:none;color:var(--encre);background:var(--papier);border:1.5px solid var(--grille);border-radius:6px;padding:4px 9px;font-weight:600}
.liens a.fiche{border-color:var(--b)}
.choix{display:flex;gap:8px;align-items:center;font-weight:600;font-size:.92rem;cursor:pointer}
.choix input{width:18px;height:18px}
details.plus summary{cursor:pointer;font-size:.88rem;color:var(--accent)}
details.plus ul{margin:4px 0 0;padding-left:18px;font-size:.9rem}
.docs{display:flex;flex-wrap:wrap;gap:8px}
.docs a{text-decoration:none;color:var(--encre);background:var(--papier);border:1.5px solid var(--grille);border-radius:8px;padding:6px 11px;font-weight:600;font-size:.92rem}
details.form summary{cursor:pointer;font-family:var(--f-titre);font-weight:600;font-size:1.15rem}
a:focus-visible,button:focus-visible,summary:focus-visible,input:focus-visible,select:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.pied{font-size:.82rem;color:var(--trait)}
#seance ol{margin:0;padding-left:22px} #seance li{margin:2px 0}
@media print{body{background:#fff;font-size:11.5px}.sansimp,.bloc,.regle,header p{display:none!important}.panneau{border:none;padding:0}}
</style></head><body><div class="page">
<header><p class="sur">Pôle Formation UIMM Centre-Val de Loire · Maîtrise statistique des procédés</p><h1>Base d'activités SPC</h1>
<p>__NB__ activités pratiques, environ __H__ heures au total. On choisit selon le groupe, le temps et le matériel.</p></header>

<section class="regle"><p><b>Prédire, faire, comparer.</b> Chaque activité tient sur une fiche et pose une seule question. Les stagiaires mesurent ou comptent, Ellistat calcule, puis on décide.</p></section>

<section class="panneau sansimp" aria-label="Réglages">
  <h2>1. Mon groupe et mon temps</h2>
  <div class="reglages">
    <label for="inN"><span>Nombre de stagiaires</span><small>de 1 à 24</small><input id="inN" type="number" min="1" max="24" value="4"></label>
    <label for="inH"><span>Temps disponible (heures)</span><small>hors pauses</small><input id="inH" type="number" min="0.5" max="40" step="0.5" value="7"></label>
    <label for="inNiv"><span>Niveau maximal</span><small>1 : découverte, 3 : exigeant</small><select id="inNiv"><option value="1">1 seulement</option><option value="2">1 et 2</option><option value="3" selected>tous</option></select></label>
  </div>
  <div><b style="font-size:.92rem">Blocs affichés</b><div class="puces" id="fBlocs" style="margin-top:4px"></div></div>
  <div><b style="font-size:.92rem">Parcours tout prêts</b> <span style="font-size:.88rem;color:var(--trait)">(remplace la sélection)</span><div class="puces" id="fParc" style="margin-top:4px"></div></div>
</section>

<section class="panneau" id="seance" aria-live="polite">
  <h2>2. Ma séance</h2>
  <div class="bilan" id="bilan"></div>
  <div class="jauge sansimp"><i id="jauge" style="width:0"></i></div>
  <p class="materiel" id="materiel"></p>
  <ol id="liste"></ol>
  <div class="sansimp" style="display:flex;gap:8px;flex-wrap:wrap"><button class="btn" id="btnImp" type="button">Imprimer ma séance</button><button class="btn second" id="btnVide" type="button">Vider la sélection</button></div>
</section>

<div id="blocs"></div>

<section class="panneau sansimp">
  <h2>Outils communs</h2>
  <div class="docs">
    <a href="Pages/Donnees_a_copier.html">Données à copier dans Ellistat</a>
    <a href="Pages/Tirer_un_lot.html">Tirer un lot (attributs)</a>
    <a href="Pages/Comparer_deux_series.html">Comparer deux séries de mesures</a>
    <a href="Pages/L_instrument_est-il_capable.html">L'instrument est-il capable ?</a>
    <a href="Activites/Memo_cartes_attributs.pdf">Mémo : les cartes p, Np, c, u et Laney (PDF)</a>
    <a href="Activites/Memo_methode_Bosch_Cg_Cgk.pdf">Mémo : Cg et Cgk, méthode Bosch (PDF)</a>
    <a href="Activites/Livret_toutes_les_fiches.pdf">Toutes les fiches en un seul PDF</a>
  </div>
  <details class="form"><summary>Documents du formateur</summary>
    <div class="docs" style="margin-top:8px">
      <a href="Formateur/Guide_formateur_base_SPC.pdf">Guide formateur : organisation et corrigés des fiches</a>
      <a href="Formateur/Guide_RR_formateur.pdf">Guide de « L'opérateur compte-t-il ? »</a>
      <a href="Formateur/Guide_Trois_cales_formateur.pdf">Guide de « Trois cales, trois questions »</a>
      <a href="Formateur/Rappel_GRR_ANOVA_formateur.pdf">Rappel : GRR et analyse de variance</a>
      <a href="Formateur/Ellistat_tests_conventions.pdf">Ellistat : deux tests de conventions</a>
    </div>
  </details>
</section>
<p class="pied">Sources des méthodes : guide utilisateur d'Ellistat Data Analysis ; Robert Bosch GmbH, <i>Booklet 10 : Capability of Measurement and Test Processes</i>, édition novembre 2019. Base construite le 11 novembre 2026. Tout le contenu est dans ce dossier.</p>
</div>
<script>
(function(){
"use strict";
var CAT=__CAT__, PARC=__PARC__, CLE="baseSPC_v1";
var NOMS={E:"Prise en main d'Ellistat",M:"Le moyen de mesure",A:"Cartes aux attributs",C:"Cartes aux mesures et capabilité"};
var $=function(id){return document.getElementById(id);};
function esc(s){ return String(s).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c];}); }
var etat={n:4,h:7,niv:3,blocs:{E:true,M:true,A:true,C:true},sel:{}};
try{ var s=localStorage.getItem(CLE); if(s){ var o=JSON.parse(s); if(o&&o.blocs&&o.sel) etat=Object.assign(etat,o); } }catch(e){}
function sauver(){ try{ localStorage.setItem(CLE,JSON.stringify(etat)); }catch(e){} }
function duree(m){ var h=Math.floor(m/60), r=m%60; return h?(h+" h"+(r?" "+(r<10?"0":"")+r:"")):(r+" min"); }
function pl(n,mot){ return n+" "+mot+(n>1?"s":""); }
/* organisation pour n stagiaires : {texte, postes} */
function orga(a,n){
  var o=a.org;
  if(o.mode==="seul") return {t:"Chacun sur son poste : "+pl(n,"poste")+".",p:n};
  if(o.mode==="binome"){
    if(n===1) return {t:"Un seul stagiaire : il mesure, le formateur note.",p:1};
    if(n%2===0) return {t:pl(n/2,"binôme")+".",p:n/2};
    if(n===3) return {t:"Un trinôme.",p:1};
    return {t:pl((n-3)/2,"binôme")+" et un trinôme.",p:(n-3)/2+1};
  }
  if(o.mode==="rotation"){
    if(n<o.min) return {t:"Il faut au moins "+o.min+" personnes : le formateur complète.",p:Math.max(n,1)};
    if(n<=8) return {t:"Rotation sur 3 postes, "+n+" tours. Un micromètre par stagiaire.",p:n};
    return {t:"Deux groupes de "+Math.ceil(n/2)+" au plus, chacun sa rotation.",p:n};
  }
  if(n<o.min) return {t:"Il faut au moins "+o.min+" personnes : le formateur complète ("+pl(o.min-n,"personne")+").",p:1};
  var g=Math.max(1,Math.floor(n/o.taille)), t=Math.ceil(n/g);
  return {t:(g===1?"Un seul groupe de "+n:pl(g,"groupe")+" de "+t+" au plus")+({M11:" : 3 opérateurs mesurent, les autres notent.",M17:" : 3 opérateurs mesurent, les autres notent.",M15:" : un micromètre et une cale témoin pour tout le groupe, chacun passe à son tour."}[a.code]||"."),p:g};
}
function construire(){
  $("fBlocs").innerHTML=Object.keys(NOMS).map(function(b){ return '<button type="button" class="puce" data-b="'+b+'" aria-pressed="'+(etat.blocs[b]?"true":"false")+'">'+b+' · '+NOMS[b]+'</button>'; }).join("");
  $("fParc").innerHTML=PARC.map(function(p,i){ return '<button type="button" class="puce" data-p="'+i+'">'+esc(p[1])+'</button>'; }).join("");
  var h="";
  Object.keys(NOMS).forEach(function(b){
    var L=CAT.filter(function(a){return a.bloc===b;}), tot=L.reduce(function(s,a){return s+a.duree;},0);
    h+='<section class="bloc" data-bloc="'+b+'" style="--b:var(--b'+b+')"><h2>Bloc '+b+' · '+NOMS[b]+' <small>'+L.length+' activités, '+duree(tot)+'</small></h2><div class="cartes">';
    L.forEach(function(a){
      h+='<article class="act" id="act'+a.code+'" data-code="'+a.code+'"><div class="tete"><span class="code">'+a.code+'</span><div><h3>'+esc(a.titre)+'</h3><p class="q">'+esc(a.question)+'</p></div></div>'
        +'<div class="meta"><span>'+duree(a.duree)+'</span><span>niveau '+a.niveau+'</span>'+(a.ellistat?'<span class="e">Ellistat</span>':'')+(a.mesure?'<span class="m">on mesure</span>':'')+'</div>'
        +'<p>'+esc(a.but)+'</p><div class="orga" data-orga></div>'
        +'<details class="plus"><summary>Matériel</summary><ul>'+a.materiel.map(function(m){return '<li>'+esc(m)+'</li>';}).join("")+'</ul></details>'
        +'<div class="liens"><a class="fiche" href="'+a.fiche+'" target="_blank" rel="noopener">Fiche (PDF)</a>'+a.liens.map(function(l){ return '<a href="'+l[1]+'" target="_blank" rel="noopener">'+esc(l[0])+'</a>'; }).join("")+'</div>'
        +'<label class="choix"><input type="checkbox" data-sel="'+a.code+'"> Retenir pour ma séance</label></article>';
    });
    h+='</div></section>';
  });
  $("blocs").innerHTML=h;
  $("blocs").style.display="grid"; $("blocs").style.gap="16px";
}
function maj(){
  var n=etat.n, sel=CAT.filter(function(a){return etat.sel[a.code];}), tot=sel.reduce(function(s,a){return s+a.duree;},0), dispo=Math.round(etat.h*60);
  document.querySelectorAll(".bloc").forEach(function(s){ s.hidden=!etat.blocs[s.dataset.bloc]; });
  CAT.forEach(function(a){ var c=$("act"+a.code); c.hidden=a.niveau>etat.niv&&!etat.sel[a.code]; c.classList.toggle("choisie",!!etat.sel[a.code]);
    c.querySelector("[data-orga]").textContent="Pour "+pl(n,"stagiaire")+" : "+orga(a,n).t; c.querySelector("input").checked=!!etat.sel[a.code]; });
  document.querySelectorAll("#fBlocs .puce").forEach(function(b){ b.setAttribute("aria-pressed",etat.blocs[b.dataset.b]?"true":"false"); });
  var trop=tot>dispo;
  $("bilan").innerHTML='<div class="chiffre"><span>Stagiaires</span><b>'+n+'</b></div><div class="chiffre"><span>Activités retenues</span><b>'+sel.length+'</b></div>'
    +'<div class="chiffre '+(sel.length?(trop?"trop":"bon"):"")+'"><span>Durée retenue</span><b>'+duree(tot)+'</b></div><div class="chiffre"><span>Temps disponible</span><b>'+duree(dispo)+'</b></div>'
    +'<div class="chiffre"><span>'+(trop?"Dépassement":"Marge")+'</span><b>'+duree(Math.abs(dispo-tot))+'</b></div>';
  var j=$("jauge"); j.style.width=Math.min(100,dispo?100*tot/dispo:0)+"%"; j.className=trop?"trop":"";
  var bes={}; sel.forEach(function(a){ var p=orga(a,n).p; for(var k in a.besoin){ var q=a.besoin[k]*(k==="micromètre 25-50"?1:p); if(a.code==="M11"&&k==="butées") q=a.besoin[k]*p; bes[k]=Math.max(bes[k]||0,q); } });
  var cles=Object.keys(bes);
  $("materiel").innerHTML=sel.length?("<b>Matériel de mesure à prévoir</b> (au plus fort de la séance) : "+(cles.length?cles.map(function(k){ return bes[k]+" × "+esc(k); }).join(", "):"aucun")+(sel.some(function(a){return a.ellistat;})?". Ellistat : un compte par poste.":".")):"Cochez « Retenir pour ma séance » sur les activités voulues, ou choisissez un parcours tout prêt.";
  $("liste").innerHTML=sel.map(function(a){ return '<li><b>'+a.code+' · '+esc(a.titre)+'</b> ('+duree(a.duree)+') : '+esc(orga(a,n).t)+'</li>'; }).join("");
  sauver();
}
construire();
$("inN").value=etat.n; $("inH").value=etat.h; $("inNiv").value=String(etat.niv);
$("inN").addEventListener("input",function(){ var v=Math.round(Number(this.value)); if(v>=1&&v<=24){ etat.n=v; maj(); } });
$("inH").addEventListener("input",function(){ var v=Number(this.value); if(v>0&&v<=40){ etat.h=v; maj(); } });
$("inNiv").addEventListener("change",function(){ etat.niv=+this.value; maj(); });
$("fBlocs").addEventListener("click",function(e){ var b=e.target.closest(".puce"); if(!b) return; etat.blocs[b.dataset.b]=!etat.blocs[b.dataset.b]; maj(); });
$("fParc").addEventListener("click",function(e){ var b=e.target.closest(".puce"); if(!b) return; etat.sel={}; PARC[+b.dataset.p][2].forEach(function(c){ etat.sel[c]=true; }); etat.blocs={E:true,M:true,A:true,C:true}; maj(); $("seance").scrollIntoView({behavior:"smooth",block:"start"}); });
$("blocs").addEventListener("change",function(e){ var c=e.target.dataset&&e.target.dataset.sel; if(!c) return; if(e.target.checked) etat.sel[c]=true; else delete etat.sel[c]; maj(); });
$("btnVide").addEventListener("click",function(){ etat.sel={}; maj(); });
$("btnImp").addEventListener("click",function(){ window.print(); });
maj();
window.__base={etat:function(){return etat;},orga:function(c,n){ return orga(CAT.filter(function(a){return a.code===c;})[0],n); }};
})();
</script></body></html>'''
tot=sum(a['duree'] for a in CAT)
html=HTML.replace('__CAT__',json.dumps(CAT,ensure_ascii=False)).replace('__PARC__',json.dumps(PARC,ensure_ascii=False)).replace('__NB__',str(len(CAT))).replace('__H__',str(round(tot/60)))
open('SPC/index.html','w',encoding='utf-8').write(html); print('ok',len(html),tot)
