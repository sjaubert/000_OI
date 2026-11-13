import numpy as np, json, openpyxl
from openpyxl.styles import Font
from scipy import stats
OLD=json.load(open('../ses/donnees.json'))
D='SPC/Donnees_Ellistat/'
J={}
def write(cle,name,sheet,head,data,dec=3):
    wb=openpyxl.Workbook(); ws=wb.active; ws.title=sheet; ws.append(head)
    for r in data: ws.append(r)
    for c in ws[1]: c.font=Font(name='Arial',bold=True)
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.font=Font(name='Arial')
            if isinstance(c.value,float): c.number_format='0.'+'0'*dec if dec else '0'
    for col in ws.columns: ws.column_dimensions[col[0].column_letter].width=14
    wb.save(D+name); J[cle]={'nom':name,'entete':head,'lignes':data,'dec':dec}
M={'butees6':('Butees_6x5.xlsx',2),'decoupage':('Butees_mauvais_decoupage.xlsx',2),'butees10':('Butees_10x5.xlsx',3),'pression':('Enquete_Pression.xlsx',0),'dimension':('Enquete_Dimension.xlsx',0),
   'liquide':('Enquete_Liquide.xlsx',0),'inspection':('Inspection_120_lots.xlsx',0),'justesse':('Justesse_Bosch_p11.xlsx',3),'rr':('RR_Bosch_p14.xlsx',3),'lin':('Linearite_5_cales_simule.xlsx',3),
   's5just':('Synthese_Justesse_cale12_simule.xlsx',3),'s5rr':('Synthese_RR_butees_simule.xlsx',3)}
for k,(n,dec) in M.items(): write(k,n,'Donnees',OLD[k]['entete'],OLD[k]['lignes'],dec)
b6=[r[1:] for r in OLD['butees6']['lignes']]
write('butees30','Butees_30_valeurs.xlsx','Donnees',['Diametre'],[[v] for r in b6 for v in r],2)
R={}
rng=np.random.default_rng(1125)
# lots 35 x 50
x=np.concatenate([rng.binomial(50,0.04,20),rng.binomial(50,0.10,15)]).tolist()
write('lots35','Lots_35x50_simule.xlsx','Donnees',['Lot','Taille_lot','Defectueuses'],[[i+1,50,int(v)] for i,v in enumerate(x)],0)
p=sum(x[:20])/1000; s=np.sqrt(p*(1-p)/50); R['lots35']=dict(x=x,tot20=sum(x[:20]),pbar=p,LCS=p+3*s,LCI=max(0,p-3*s),npLCS=50*(p+3*s),hors=[i+1 for i,v in enumerate(x) if v/50>p+3*s],
   pall=sum(x)/1750, LCSall=sum(x)/1750+3*np.sqrt(sum(x)/1750*(1-sum(x)/1750)/50), horsall=[i+1 for i,v in enumerate(x) if v/50>sum(x)/1750+3*np.sqrt(sum(x)/1750*(1-sum(x)/1750)/50)])
# taille variable
n=rng.choice([80,120,160,200,250,300,400],25).tolist(); d=[int(rng.binomial(k,0.03)) for k in n]; d[17]=int(round(n[17]*0.09))
write('lotsvar','Lots_taille_variable_simule.xlsx','Donnees',['Lot','Taille_lot','Defectueuses'],[[i+1,n[i],d[i]] for i in range(25)],0)
p=sum(d)/sum(n); R['lotsvar']=dict(n=n,d=d,pbar=p,tot=(sum(d),sum(n)),lim=[(i+1,n[i],d[i]/n[i],p+3*np.sqrt(p*(1-p)/n[i]),max(0,p-3*np.sqrt(p*(1-p)/n[i]))) for i in range(25)])
R['lotsvar']['hors']=[t[0] for t in R['lotsvar']['lim'] if t[2]>t[3] or t[2]<t[4]]
# défauts par panneau (carte c)
c=np.concatenate([rng.poisson(4,20),rng.poisson(8,10)]).tolist()
write('panneaux','Defauts_panneaux_simule.xlsx','Donnees',['Panneau','Defauts'],[[i+1,int(v)] for i,v in enumerate(c)],0)
cb=sum(c[:20])/20; R['panneaux']=dict(c=c,tot20=sum(c[:20]),cbar=cb,LCS=cb+3*np.sqrt(cb),LCI=max(0,cb-3*np.sqrt(cb)),hors=[i+1 for i,v in enumerate(c) if v>cb+3*np.sqrt(cb)],cball=sum(c)/30,LCSall=sum(c)/30+3*np.sqrt(sum(c)/30))
# défauts par rouleau (carte u)
L=rng.choice([40,50,60,80,100,120],25).tolist(); u=[int(rng.poisson(0.05*l)) for l in L]; u[13]=int(round(0.16*L[13]))
write('rouleaux','Defauts_rouleaux_simule.xlsx','Donnees',['Rouleau','Longueur_m','Defauts'],[[i+1,L[i],u[i]] for i in range(25)],0)
ub=sum(u)/sum(L); R['rouleaux']=dict(L=L,u=u,tot=(sum(u),sum(L)),ubar=ub,lim=[(i+1,L[i],u[i]/L[i],ub+3*np.sqrt(ub/L[i]),max(0,ub-3*np.sqrt(ub/L[i]))) for i in range(25)])
R['rouleaux']['hors']=[t[0] for t in R['rouleaux']['lim'] if t[2]>t[3] or t[2]<t[4]]
# secours mesures
def mes(n,b,s,res,xm=10.0): return np.round((xm+b+s*rng.standard_normal(n))/res)*res
mic=mes(25,0.0006,0.0007,0.001); pac=mes(25,0.004,0.012,0.02)
write('instr','Secours_deux_instruments_simule.xlsx','Donnees',['Micrometre','Pied_a_coulisse'],[[round(float(a),3),round(float(b),2)] for a,b in zip(mic,pac)],3)
av=mes(15,0.0004,0.0006,0.001); sa=mes(15,-0.0030,0.0022,0.001)
write('cliquet','Secours_cliquet_simule.xlsx','Donnees',['Avec_cliquet','Sans_cliquet'],[[round(float(a),3),round(float(b),3)] for a,b in zip(av,sa)],3)
oa=mes(15,0.0,0.0007,0.001); ob=mes(15,0.0012,0.0007,0.001)
write('operateurs','Secours_deux_operateurs_simule.xlsx','Donnees',['Operateur_A','Operateur_B'],[[round(float(a),3),round(float(b),3)] for a,b in zip(oa,ob)],3)
t=np.arange(0,331,30); ch=np.round((25.0+0.0004+0.0024*np.exp(-t/110)+0.0004*rng.standard_normal(len(t)))/0.001)*0.001
write('chauffe','Secours_cale_chauffee_simule.xlsx','Donnees',['Temps_s','Mesure'],[[int(a),round(float(b),3)] for a,b in zip(t,ch)],3)
def t1(x,xm,T):
    x=np.array(x); m=x.mean(); s=x.std(ddof=1); b=m-xm
    return dict(n=len(x),m=m,s=s,b=b,Cg=0.2*T/(6*s) if s>0 else np.inf,Cgk=(0.1*T-abs(b))/(3*s) if s>0 else np.inf,Tmin=10*abs(b)+39.9*s,res_pct=None)
for k,x in [('mic',mic),('pac',pac),('av',av),('sa',sa),('oa',oa),('ob',ob)]:
    R[k]={kk:float(v) if v is not None else None for kk,v in t1(x,10,0.15).items()}
    R[k]['T']={T:(0.2*T/(6*R[k]['s']),(0.1*T-abs(R[k]['b']))/(3*R[k]['s'])) for T in (0.15,0.05,0.02,0.01)}
def cmp(a,b):
    r=stats.ttest_ind(b,a,equal_var=False); F=max(np.var(a,ddof=1),np.var(b,ddof=1))/min(np.var(a,ddof=1),np.var(b,ddof=1))
    return dict(d=float(np.mean(b)-np.mean(a)),t=float(abs(r.statistic)),tc=float(stats.t.ppf(.975,r.df)),F=float(F),Fc=float(stats.f.ppf(.975,len(a)-1,len(b)-1)))
R['cmp_instr']=cmp(mic,pac); R['cmp_cliquet']=cmp(av,sa); R['cmp_op']=cmp(oa,ob); R['chauffe']=ch.tolist()
# M14 : trois etalons composes (11,850 ; 11,925 ; 12,000), 10 mesures chacun, graine 3011 (voir m14/calc.py)
write('etalons','Secours_trois_etalons_simule.xlsx','Donnees',['Etalon_11_850','Etalon_11_925','Etalon_12_000'],[[11.851, 11.925, 12.0], [11.851, 11.925, 12.0], [11.85, 11.926, 12.001], [11.85, 11.925, 12.0], [11.849, 11.927, 12.001], [11.851, 11.925, 12.0], [11.851, 11.925, 12.001], [11.85, 11.926, 12.001], [11.851, 11.926, 12.001], [11.852, 11.925, 12.002]],3)
json.dump(J,open('donnees_base.json','w'),ensure_ascii=False)
def show(o,ind=0):
    for k,v in o.items():
        if isinstance(v,dict): print(' '*ind+str(k)+':'); show(v,ind+2)
        elif isinstance(v,float): print(' '*ind+f'{k}: {v:.6g}')
        else: print(' '*ind+f'{k}: {v}')
show(R)
