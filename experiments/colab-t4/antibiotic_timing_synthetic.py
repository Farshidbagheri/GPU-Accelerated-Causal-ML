"""Factual-only learning of simulated individualized antibiotic initiation risk curves.

This is a controlled synthetic causal identification exercise, not a clinical or
antibiotic-safety result. Simulation ground truth is never used for model training.
With known observed time-varying propensity, unstabilized IPW addresses selection
into fixed initiation policies under simulated sequential exchangeability.
"""
from __future__ import annotations
import argparse
import json
import time
from pathlib import Path
import numpy as np
import torch
from torch import nn
import torch.nn.functional as F

HORIZON = 4  # interventions: first dose at 0,1,2,3, or no dose through time 3 (4)


def _sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -24, 24)))


def risk_process(x, severity_noise, start_time):
    """Known true event probability under fixed-dose time, given exogenous disturbances.

    x is (n,2), severity_noise (n,4), start_time (n,), where 4 means none.
    Risk is a *simulated adverse-event proxy*, NOT an actual clinical endpoint.
    """
    n = len(x)
    severity = 0.8*x[:, 0] + 0.2*x[:, 1]
    high = np.maximum(severity, 0)
    cum_untreated = np.zeros(n)
    for t in range(HORIZON):
        exposed = start_time <= t
        severity = (0.73*severity + 0.35*x[:, 0] + 0.20*x[:, 1]
                    + 0.19*(~exposed) - 0.42*exposed + 0.58*severity_noise[:, t])
        high = np.maximum(high, severity)
        cum_untreated += (~exposed)
    # Nonlinear heterogeneity means high baseline severity increases harms from deferral.
    log_odds = (-2.15 + 0.68*severity + 0.31*x[:, 0] + 0.21*x[:, 1]
                + 0.17*high + 0.115*cum_untreated
                + 0.060*cum_untreated*np.maximum(x[:, 0], 0))
    return _sigmoid(log_odds)


def simulate_factual(n, seed):
    rng = np.random.default_rng(seed)
    x = rng.normal(size=(n, 2))
    noises = rng.normal(size=(n, HORIZON))
    outcome_noise = rng.random(n)
    severity = 0.8*x[:, 0] + 0.2*x[:, 1]
    first_t = np.full(n, HORIZON, dtype=np.int64)
    prob_observed_path = np.ones(n)
    for t in range(HORIZON):
        untreated = first_t == HORIZON
        if not untreated.any():
            break
        idx = np.where(untreated)[0]
        severity[idx] = (0.73*severity[idx] + 0.35*x[idx, 0]
                         + 0.20*x[idx, 1] + 0.19 + 0.58*noises[idx, t])
        p = 0.23 + 0.37*_sigmoid(0.72*severity[idx]+0.20*x[idx, 0]+0.12*t)
        take = rng.random(len(idx)) < p
        prob_observed_path[idx] *= np.where(take, p, 1-p)
        first_t[idx[take]] = t
    factual_risk = risk_process(x, noises, first_t)
    y = (outcome_noise < factual_risk).astype(np.float32)
    return dict(x=x.astype(np.float32),
                k=first_t, y=y,
                propensity=prob_observed_path.astype(np.float32),
                noise=noises.astype(np.float32))


def oracle_personalized_risk(x, seed, draws=64):
    """MC oracle E[Y^k | baseline X=x] under a known *synthetic* DGP.

    Ground truth used for scoring ONLY. It never enters optimization.
    """
    rng = np.random.default_rng(seed)
    oracle = np.zeros((len(x), HORIZON+1))
    for _ in range(draws):
        noise = rng.normal(size=(len(x), HORIZON))
        for k in range(HORIZON+1):
            oracle[:, k] += risk_process(x, noise, np.full(len(x), k)) / draws
    return oracle


class CurveNet(nn.Module):
    def __init__(self, width=48):
        super().__init__()
        self.net=nn.Sequential(nn.Linear(2+HORIZON+1,width),nn.SiLU(),
                               nn.Linear(width,width//2),nn.SiLU(),
                               nn.Linear(width//2,1))
    def forward(self, x, k):
        return torch.sigmoid(self.net(torch.cat([x, F.one_hot(k,HORIZON+1).float()],1)).flatten())


def _tensor(a, device, dtype=torch.float32):
    return torch.as_tensor(a, device=device, dtype=dtype)


def train_curve_model(train, validation, device="cpu", seed=41, epochs=70,
                      ipw=True, width=48, batch_size=384):
    if device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA device unavailable: GPU benchmark not performed")
    dev=torch.device(device)
    torch.manual_seed(seed); np.random.seed(seed)
    if device=="cpu": torch.set_num_threads(2)
    model=CurveNet(width).to(dev)
    optimizer=torch.optim.AdamW(model.parameters(),lr=0.003,weight_decay=0.0004)
    xt=_tensor(train['x'],dev); yt=_tensor(train['y'],dev); kt=_tensor(train['k'],dev,torch.long)
    xv=_tensor(validation['x'],dev); yv=_tensor(validation['y'],dev)
    kv=_tensor(validation['k'],dev,torch.long)
    if ipw:
        raw=1/np.clip(train['propensity'],0.02,1.0)
        weights=np.minimum(raw,35)
        # Equal treatment-time normalization balances support across regimes.
        for k in range(HORIZON+1):
            rows=train['k']==k
            weights[rows]=weights[rows]/np.maximum(weights[rows].mean(),1e-6)
    else: weights=np.ones(len(xt))
    wt=_tensor(weights,dev)
    best=float('inf');best_state=None;bad=0;best_epoch=0
    start=time.perf_counter()
    for epoch in range(epochs):
        model.train()
        for indices in torch.randperm(len(xt),device=dev).split(batch_size):
            p=model(xt[indices],kt[indices]).clamp(1e-5,1-1e-5)
            loss=(F.binary_cross_entropy(p,yt[indices],reduction='none')*wt[indices]).mean()
            optimizer.zero_grad();loss.backward();optimizer.step()
        model.eval()
        with torch.no_grad():
            pv=model(xv,kv).clamp(1e-5,1-1e-5)
            val=float(F.binary_cross_entropy(pv,yv).item())
        if val < best-1e-4:
            best=val;bad=0;best_epoch=epoch+1
            best_state={name:w.detach().clone() for name,w in model.state_dict().items()}
        else:bad+=1
        if bad>=15:break
    model.load_state_dict(best_state)
    if dev.type=='cuda':torch.cuda.synchronize()
    elapsed=time.perf_counter()-start
    model.eval()
    return model,dict(training_seconds=round(elapsed,3),selected_epoch=best_epoch,
                      validation_log_loss=round(best,6),device=device,
                      ipw=ipw,n_training_rows=len(xt))


def score_curves(model,x,device="cpu", batch=1024):
    dev=torch.device(device)
    results=np.zeros((len(x),HORIZON+1),dtype=np.float64)
    with torch.no_grad():
        for i in range(0,len(x),batch):
            xx=_tensor(x[i:i+batch],dev)
            for k in range(HORIZON+1):
                results[i:i+len(xx),k]=model(xx,torch.full((len(xx),),k,dtype=torch.long,device=dev)).cpu().numpy()
    return results


def _metrics(est,ref):
    return dict(curve_rmse=float(np.sqrt(np.mean((est-ref)**2))),
                harm_from_waiting_rmse=float(np.sqrt(np.mean(((est[:,1:]-est[:,:1])-(ref[:,1:]-ref[:,:1]))**2))),
                mean_absolute_curve_error=float(np.mean(np.abs(est-ref))),
                urgency_at_3pct_agreement=float(np.mean(
                  ((est[:,1:]-est[:,:1])>=0.03).argmax(axis=1)==
                  ((ref[:,1:]-ref[:,:1])>=0.03).argmax(axis=1))))


def evaluate_once(seed=41,n=3200,epochs=70,device="cpu",oracle_draws=64):
    full=simulate_factual(n,seed)
    perm=np.random.default_rng(seed+600).permutation(n)
    ntrain=int(n*.70);nval=int(n*.15)
    train_ix=perm[:ntrain];val_ix=perm[ntrain:ntrain+nval];test_ix=perm[ntrain+nval:]
    subset=lambda ix:{key:v[ix] for key,v in full.items()}
    train=subset(train_ix);val=subset(val_ix);test=subset(test_ix)
    truth=oracle_personalized_risk(test['x'],seed+10000,draws=oracle_draws)
    learned={};meta={}
    for name,ipw in [('factual_unweighted',False),('factual_ipw',True)]:
        model,info=train_curve_model(train,val,device,seed,epochs,ipw=ipw)
        estimates=score_curves(model,test['x'],device)
        learned[name]=estimates;meta[name]=info
    naive=np.tile(np.asarray([train['y'][train['k']==k].mean() for k in range(HORIZON+1)]),(len(test_ix),1))
    result={
        'seed':seed,'n_people':n,'n_test_people':len(test_ix),
        'n_train':len(train_ix),'n_validation':len(val_ix),
        'observed_dose_time_counts':np.bincount(full['k'],minlength=HORIZON+1).tolist(),
        'interventions':'simulated first-dose t=0,1,2,3 or none through horizon',
        'oracle_population_risk_by_start_time':np.round(truth.mean(axis=0),6).tolist(),
        'unadjusted_group_risk_by_observed_treatment_time':np.round(naive.mean(axis=0),6).tolist(),
        'ipw_learned_population_risk':np.round(learned['factual_ipw'].mean(axis=0),6).tolist(),
        'mean_true_harm_of_delay_time3_vs_time0':float((truth[:,3]-truth[:,0]).mean()),
        'metrics':{**{key:_metrics(est,truth) for key,est in learned.items()},'naive_group_means':_metrics(naive,truth)},
        'training':meta,
        'sample_curve_x':np.round(test['x'][:3],3).tolist(),
        'sample_curve_truth':np.round(truth[:3],5).tolist(),
        'sample_curve_ipw':np.round(learned['factual_ipw'][:3],5).tolist(),
        'device':device,'source':'Independent synthetic DGP / factual-only learned estimator',
        'limitations':[
          'No real EHR patients or antibiotic administration are modeled',
          'Reported risk is a simulated event probability, not sepsis mortality',
          'Oracle conditional risk is available only because this is a simulation',
          'IPW uses known true treatment propensities from the synthetic generator',
          'This is not individualized clinical effect identification, and no safe delay is claimed',
          'GPU speedup requires matched independent CUDA experiment']
    }
    return result


def summarize(runs):
    keys=['factual_ipw','factual_unweighted','naive_group_means']
    return {key:{metric:round(float(np.mean([r['metrics'][key][metric] for r in runs])),6)
                  for metric in ['curve_rmse','harm_from_waiting_rmse','mean_absolute_curve_error']}
            for key in keys}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--seeds',default='41,42,43')
    p.add_argument('--patients',type=int,default=3200)
    p.add_argument('--epochs',type=int,default=70)
    p.add_argument('--oracle-draws',type=int,default=64)
    p.add_argument('--device',choices=['cpu','cuda'],default='cpu')
    p.add_argument('--out',type=Path,default=Path('results/personalized_timing_synthetic.json'))
    a=p.parse_args()
    if a.device=='cuda' and not torch.cuda.is_available():
        raise SystemExit('CUDA device unavailable: GPU benchmark NOT performed')
    runs=[evaluate_once(int(s),a.patients,a.epochs,a.device,a.oracle_draws)
          for s in a.seeds.split(',')]
    data=dict(experiment='Synthetic individualized first-dose-time risk curves',runs=runs,
              average_metrics=summarize(runs),gpu_speedup_measured=False,
              clinical_treatment_effect_estimated=False)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'average_metrics':data['average_metrics'],
                      'risk_oracle':runs[0]['oracle_population_risk_by_start_time'],
                      'risk_ipw':runs[0]['ipw_learned_population_risk'],
                      'training':runs[0]['training']},indent=2))

if __name__=='__main__':main()
