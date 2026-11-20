import sys, json, math, numpy as np
from scipy import stats
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
D="/home/claude/tp_u/work/data"; F="/home/claude/tp_u/work/fig"
h1=np.load(f"{D}/s1_h.npy"); n1=np.load(f"{D}/s1_n.npy"); h2=np.load(f"{D}/s2_h.npy"); n2=np.load(f"{D}/s2_n.npy")
R=json.load(open(f"{D}/resultats.json")); NREF=52; W=60
ub=R['s1']['ubar']
out={}
out['lim']={int(h):(round(ub+3*math.sqrt(ub/h),5), round(max(0,ub-3*math.sqrt(ub/h)),5), int(math.floor(ub*h+3*math.sqrt(ub*h)))) for h in (40,56,80,120)}
cb=R['s1']['cbar']; ccl=cb+3*math.sqrt(cb)
out['c_alarms_all']=[i+1 for i in range(78) if n1[i]>ccl]
u=n1/h1; ucl=ub+3*np.sqrt(ub/h1)
out['u_alarms_all']=[i+1 for i in range(78) if u[i]>ucl[i]]
out['n_reference_weeks_120h']=int((h1[:52]==120).sum())
# Laney sur phase I série 1
z=(u[:52]-ub)/np.sqrt(ub/h1[:52]); sz=np.abs(np.diff(z)).mean()/1.128
out['laney_s1_ref_sz']=sz
X2=float(((n1[:52]-h1[:52]*ub)**2/(h1[:52]*ub)).sum()); out['s1_ref_X2']=X2; out['s1_ref_p']=float(stats.chi2.sf(X2,51))
# test exact de comparaison de deux taux de Poisson (conditionnel binomial)
N1,T1=R['pre']['N'],R['pre']['T']; N2,T2=R['post']['N'],R['post']['T']
p=stats.binomtest(N2,N1+N2,T2/(T1+T2),alternative='greater').pvalue
out['two_rate_p']=float(p); out['ratio']=(N2/T2)/(N1/T1)
# points hors limite avec 2 alarmes de suite etc
out['post_weeks_n']=int(len(h1)-(W-1)); out['post_after53']=dict(N=int(n1[52:].sum()),T=int(h1[52:].sum()))
# nb de pannes semaine 15
out['w15']=(int(h1[14]),int(n1[14]))
# S2
ub2=R['s2']['ubar']; u2=n2/h2
z2=(u2-ub2)/np.sqrt(ub2/h2); out['s2_sz']=float(np.abs(np.diff(z2)).mean()/1.128)
out['s2_hours_unique']=sorted(set(h2.tolist()))
out['s2_alarm_detail']=[(w,int(h2[w-1]),int(n2[w-1]),round(float(u2[w-1]),4)) for w in R['s2']['out_u']]
# alarme de Laney limites moyenne
sz2=R['s2']['sz']; out['s2_laney_ucl_480']=ub2+3*sz2*math.sqrt(ub2/480); out['s2_u_ucl_480']=ub2+3*math.sqrt(ub2/480)
print(json.dumps(out,indent=1,default=float))
json.dump(out,open(f"{D}/extra.json","w"),indent=1,default=float)
# ---- figures
blue="#005677"; cy="#13A2DD"; red="#B3261E"
def uchart(h,n,ub,ref=None,title="",ylab="pannes par heure de marche",shift=None,fn="",ylim=None):
    w=np.arange(1,len(h)+1); u=n/h; ucl=ub+3*np.sqrt(ub/h)
    fig,ax=plt.subplots(figsize=(8,3.0))
    ax.plot(w,u,color=blue,marker='o',ms=3,lw=1)
    ax.step(w,ucl,where='mid',color=red,lw=1)
    ax.axhline(ub,color='green',lw=1)
    bad=u>ucl; ax.plot(w[bad],u[bad],'o',color=red,ms=5)
    if ref: ax.axvline(ref+0.5,color='gray',ls='--',lw=0.8); ax.text(ref/2,ax.get_ylim()[1]*0.92,"Phase I",ha='center',fontsize=8,color='gray')
    ax.set_xlabel("Semaine"); ax.set_ylabel(ylab,fontsize=8); ax.set_title(title,fontsize=9)
    ax.tick_params(labelsize=8); 
    if ylim: ax.set_ylim(*ylim)
    fig.tight_layout(); fig.savefig(f"{F}/{fn}.pdf"); plt.close(fig)
uchart(h1,n1,ub,ref=52,title="Série 1 simulée : carte u, limites calculées sur les semaines 1 à 52",fn="u_s1")
# carte c
fig,ax=plt.subplots(figsize=(8,3.0)); w=np.arange(1,79)
ax.plot(w,n1,color=blue,marker='o',ms=3,lw=1); ax.axhline(cb,color='green',lw=1); ax.axhline(ccl,color=red,lw=1)
bad=n1>ccl; ax.plot(w[bad],n1[bad],'o',color=red,ms=5); ax.axvline(52.5,color='gray',ls='--',lw=0.8)
ax.set_xlabel("Semaine"); ax.set_ylabel("nombre de pannes",fontsize=8); ax.set_title("Série 1 simulée : carte c (exposition ignorée)",fontsize=9); ax.tick_params(labelsize=8)
fig.tight_layout(); fig.savefig(f"{F}/c_s1.pdf"); plt.close(fig)
# série 2 : u et Laney
w=np.arange(1,53); ucl=ub2+3*np.sqrt(ub2/h2); ucl2=ub2+3*sz2*np.sqrt(ub2/h2)
fig,ax=plt.subplots(figsize=(8,3.0))
ax.plot(w,u2,color=blue,marker='o',ms=3,lw=1); ax.step(w,ucl,where='mid',color=red,lw=1,label="carte u")
ax.step(w,ucl2,where='mid',color='darkorange',lw=1,label="U Laney"); ax.axhline(ub2,color='green',lw=1)
bad=u2>ucl; ax.plot(w[bad],u2[bad],'o',color=red,ms=5); ax.legend(fontsize=8)
ax.set_xlabel("Semaine"); ax.set_ylabel("pannes par heure de marche",fontsize=8); ax.set_title("Série 2 simulée (parc de 6 presses) : carte u et U Laney",fontsize=9); ax.tick_params(labelsize=8)
fig.tight_layout(); fig.savefig(f"{F}/u_s2.pdf"); plt.close(fig)
