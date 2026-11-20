import numpy as np
from scipy import stats
def cg_stats(x, T, x0):
    x=np.asarray(x,float); n=len(x); m=x.mean(); s=x.std(ddof=1); b=m-x0
    cg=0.2*T/(6*s) if s>0 else float('inf'); cgk=(0.1*T-abs(b))/(3*s) if s>0 else float('inf')
    tmin=39.9*s+10*abs(b)
    return dict(n=n,mean=m,s=s,bias=b,cg=cg,cgk=cgk,tmin=tmin,distinct=len(set(np.round(x,6).tolist())))
def rr_anova(data, T=None):
    """data[piece, operateur, repetition]. ANOVA croisée, interaction regroupée si non significative (risque 5 %)."""
    d=np.asarray(data,float); p,o,r=d.shape
    gm=d.mean(); mp=d.mean(axis=(1,2)); mo=d.mean(axis=(0,2)); mpo=d.mean(axis=2)
    ssp=o*r*((mp-gm)**2).sum(); sso=p*r*((mo-gm)**2).sum()
    ssi=r*((mpo-mp[:,None]-mo[None,:]+gm)**2).sum(); sse=((d-mpo[:,:,None])**2).sum()
    dfp,dfo,dfi,dfe=p-1,o-1,(p-1)*(o-1),p*o*(r-1)
    msp,mso,msi,mse=ssp/dfp,sso/dfo,ssi/dfi,sse/dfe
    Fi=msi/mse; pi=stats.f.sf(Fi,dfi,dfe)
    pooled = pi>0.05
    if pooled:
        mse2=(ssi+sse)/(dfi+dfe); s_e=mse2; s_i=0.0
        s_o=max(0.0,(mso-mse2)/(p*r)); s_p=max(0.0,(msp-mse2)/(o*r)); Fo=mso/mse2; po=stats.f.sf(Fo,dfo,dfi+dfe)
    else:
        s_e=mse; s_i=max(0.0,(msi-mse)/r); s_o=max(0.0,(mso-msi)/(p*r)); s_p=max(0.0,(msp-msi)/(o*r)); Fo=mso/msi; po=stats.f.sf(Fo,dfo,dfi)
    EV=np.sqrt(s_e); AV=np.sqrt(s_o); INT=np.sqrt(s_i); GRR=np.sqrt(s_e+s_o+s_i); PV=np.sqrt(s_p)
    out=dict(EV=EV,AV=AV,INT=INT,GRR=GRR,PV=PV,ndc=np.sqrt(2)*PV/GRR if GRR>0 else float('inf'),
             F_int=Fi,p_int=pi,pooled=bool(pooled),F_op=Fo,p_op=po,TV=np.sqrt(GRR**2+PV**2),
             pct_GRR_proc=100*GRR/np.sqrt(GRR**2+PV**2))
    if T: out.update(pct_GRR_T=100*6*GRR/T, Cpc=T/(6*GRR), Tmin=60*GRR)
    return out
def read_rr(path):
    import openpyxl
    ws=openpyxl.load_workbook(path).active; rows=list(ws.iter_rows(values_only=True))[1:]
    a=np.array([[float(v) for v in r[1:]] for r in rows]); p=a.shape[0]
    return a.reshape(p,-1,2)
