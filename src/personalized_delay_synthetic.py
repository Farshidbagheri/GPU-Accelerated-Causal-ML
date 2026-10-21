"""Synthetic individualized first-dose timing curves, trained on factual data only.

Simulated observational trajectories with time-varying confounding. All
counterfactual risk curves used as ground truth are generated *only* for
holdout scoring, never for model fitting. NOT a clinical effect estimate.
"""
import argparse, json, time
from pathlib import Path
import numpy as np
import torch
from torch import nn
import torch.nn.functional as F
HORIZON=4

def sigmoid(z):return 1/(1+np.exp(-np.clip(z,-24,24)))

def risk_process(x,noise,k):
    n=len(x); sev=.8*x[:,0]+.2*x[:,1]
    highest=np.maximum(sev,0); untreated=np.zeros(n)
    for t in range(HORIZON):
        exposed=k<=t
        sev=.73*sev+.35*x[:,0]+.2*x[:,1]+.19*(~exposed)-.42*exposed+.58*noise[:,t]
        highest=np.maximum(highest,sev);untreated+=(~exposed)
    logits=(-2.15+.68*sev+.31*x[:,0]+.21*x[:,1]+.17*highest
            +.115*untreated+.060*untreated*np.maximum(x[:,0],0))
    return sigmoid(logits)

def simulate(n,seed):
    rng=np.random.default_rng(seed)
    x=rng.normal(size=(n,2));noise=rng.normal(size=(n,HORIZON))
    sev=.8*x[:,0]+.2*x[:,1]; k=np.full(n,HORIZON,dtype=np.int64)
    pathprob=np.ones(n)
    for t in range(HORIZON):
        idx=np.where(k==HORIZON)[0]
        if not len(idx):break
        sev[idx]=.73*sev[idx]+.35*x[idx,0]+.20*x[idx,1]+.19+.58*noise[idx,t]
        p=.23+.37*sigmoid(.72*sev[idx]+.20*x[idx,0]+.12*t)
        treated=rng.random(len(idx))<p
        pathprob[idx]*=np.where(treated,p,1-p)
        k[idx[treated]]=t
    prob=risk_process(x,noise,k)
    y=(rng.random(n)<prob).astype(np.float32)
    return dict(x=x.astype(np.float32),k=k,y=y,
                propensity=pathprob.astype(np.float32))

def oracle(x,seed,draws=64):
    rng=np.random.default_rng(seed);out=np.zeros((len(x),HORIZON+1))
    for _ in range(draws):
        noise=rng.normal(size=(len(x),HORIZON))
        for k in range(HORIZON+1):
            out[:,k]+=risk_process(x,noise,np.full(len(x),k))/draws
    return out

class RiskNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.net=nn.Sequential(nn.Linear(7,48),nn.SiLU(),nn.Linear(48,24),
                               nn.SiLU(),nn.Linear(24,1))
    def forward(self,x,k):
        return torch.sigmoid(self.net(torch.cat([x,F.one_hot(k,5).float()],1)).flatten())

def train(tr,val,device,seed,epochs,weighted):
    torch.manual_seed(seed);np.random.seed(seed)
    dev=torch.device(device)
    if device=='cpu':torch.set_num_threads(2)
    model=RiskNet().to(dev)
    T=lambda x,dtype=torch.float32:torch.as_tensor(x,device=dev,dtype=dtype)
    x=T(tr['x']); k=T(tr['k'],torch.long);y=T(tr['y'])
    xv=T(val['x']);kv=T(val['k'],torch.long);yv=T(val['y'])
    weight=np.minimum(1/np.clip(tr['propensity'],.02,1),35) if weighted else np.ones(len(x))
    if weighted:
        for ki in range(5):
            m=tr['k']==ki
            weight[m]/=np.maximum(weight[m].mean(),1e-6)
    w=T(weight)
    opt=torch.optim.AdamW(model.parameters(),lr=.003,weight_decay=.0004)
    best=float('inf');weights=None;stale=0;epoch_best=0
    start=time.perf_counter()
    for ep in range(epochs):
        model.train()
        for inds in torch.randperm(len(x),device=dev).split(384):
            p=model(x[inds],k[inds]).clamp(1e-5,1-1e-5)
            loss=(F.binary_cross_entropy(p,y[inds],reduction='none')*w[inds]).mean()
            opt.zero_grad();loss.backward();opt.step()
        model.eval()
        with torch.no_grad():
            val_loss=float(F.binary_cross_entropy(model(xv,kv).clamp(1e-5,1-1e-5),yv))
        if val_loss<best-1e-4:
            best=val_loss;stale=0;epoch_best=ep+1
            weights={name:param.detach().clone() for name,param in model.state_dict().items()}
        else:stale+=1
        if stale>=15:break
    model.load_state_dict(weights)
    if device=='cuda':torch.cuda.synchronize()
    return model,{'seconds':round(time.perf_counter()-start,4),
                  'validation_bce':round(best,6),'best_epoch':epoch_best}

def predict(model,x,device):
    dev=torch.device(device);out=np.zeros((len(x),5))
    model.eval()
    with torch.no_grad():
        for i in range(0,len(x),1024):
            xx=torch.as_tensor(x[i:i+1024],device=dev,dtype=torch.float32)
            for k in range(5):
                out[i:i+len(xx),k]=model(xx,torch.full((len(xx),),k,device=dev)).cpu().numpy()
    return out

def score(y,truth):
    return {'curve_rmse':float(np.sqrt(np.mean((y-truth)**2))),
            'waiting_harm_rmse':float(np.sqrt(np.mean(((y[:,1:]-y[:,:1])-(truth[:,1:]-truth[:,:1]))**2))),
            'mean_absolute_curve_error':float(np.mean(np.abs(y-truth)))}

def run(seed=41,n=3200,epochs=70,device='cpu',draws=64):
    if device=='cuda' and not torch.cuda.is_available():
        raise RuntimeError('No CUDA device available; GPU benchmark not performed')
    data=simulate(n,seed);ids=np.random.default_rng(seed+600).permutation(n)
    a=int(.7*n);b=int(.85*n)
    subset=lambda ix:{key:v[ix] for key,v in data.items()}
    tr=subset(ids[:a]);val=subset(ids[a:b]);test=subset(ids[b:])
    truth=oracle(test['x'],seed+10000,draws)
    scores={};curves={};timings={}
    for name,weighted in [('unweighted',False),('ipw',True)]:
        model,info=train(tr,val,device,seed,epochs,weighted)
        p=predict(model,test['x'],device)
        scores[name]=score(p,truth);curves[name]=p.mean(axis=0).tolist();timings[name]=info
    naive=np.tile([tr['y'][tr['k']==k].mean() for k in range(5)],(len(test['k']),1))
    scores['naive']=score(naive,truth)
    return {'seed':seed,'train_people':len(tr['k']),'test_people':len(test['k']),
            'observed_start_time_counts':np.bincount(data['k'],minlength=5).tolist(),
            'oracle_risk_by_start_time':truth.mean(axis=0).tolist(),
            'ipw_learned_risk_by_start_time':curves['ipw'],
            'unweighted_learned_risk_by_start_time':curves['unweighted'],
            'scores':scores,'train_details':timings,'device':device,
            'source':'Entirely synthetic, factual-only training; synthetic oracle used only for scoring',
            'clinical_effect':False,'gpu_speedup':False}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--seeds',default='41,42,43')
    p.add_argument('--patients',type=int,default=3200)
    p.add_argument('--epochs',type=int,default=70)
    p.add_argument('--oracle-draws',type=int,default=64)
    p.add_argument('--device',choices=['cpu','cuda'],default='cpu')
    p.add_argument('--out',type=Path,default=Path('results/individualized-risk-curves.json'))
    a=p.parse_args()
    if a.device=='cuda' and not torch.cuda.is_available():
        raise SystemExit('CUDA unavailable; no GPU benchmark was performed')
    runs=[run(int(s),a.patients,a.epochs,a.device,a.oracle_draws) for s in a.seeds.split(',')]
    avg={key:{m:round(float(np.mean([r['scores'][key][m] for r in runs])),6)
              for m in ['curve_rmse','waiting_harm_rmse','mean_absolute_curve_error']}
         for key in ['naive','unweighted','ipw']}
    out={'experiment':'Synthetic personalized first-dose-time risk curves',
         'runs':runs,'mean_scores':avg,'clinical_effect_estimated':False,
         'gpu_benchmark_performed':a.device=='cuda'}
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'mean_scores':avg,'first_seed_oracle_risk':runs[0]['oracle_risk_by_start_time'],
                      'first_seed_ipw_risk':runs[0]['ipw_learned_risk_by_start_time']},indent=2))
if __name__=='__main__':main()
