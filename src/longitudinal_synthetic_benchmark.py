"""Independent synthetic longitudinal causal benchmark; NOT a paper reproduction.

At each simulated decision time, L_t and patient history determine treatment
propensity and factual outcome; the individual current-action effect is known.
Train/validation/test split is by patient. No clinical inputs are used.
"""
from __future__ import annotations
import argparse, json, random, time
from pathlib import Path
import numpy as np
from sklearn.linear_model import LogisticRegression, Ridge

def sigmoid(x):
    return 1/(1+np.exp(-np.clip(x,-20,20)))

def simulate(n_patients=1200,horizon=6,seed=40):
    rng=np.random.default_rng(seed); rows=[]
    for pid in range(n_patients):
        x=rng.normal(); prev_l=rng.normal(); prev_a=0
        for t in range(horizon):
            l=0.72*prev_l+0.46*prev_a+0.34*x+rng.normal(scale=0.62)
            p=sigmoid(0.96*l+0.58*x+0.48*prev_a-0.22)
            a=int(rng.uniform()<p)
            y0=0.86*l+0.25*x+0.62*np.sin(l)+0.42*prev_a*l+0.07*t
            tau=1.0+0.96*np.sin(l)+0.30*x*np.tanh(l)-0.25*prev_a
            y=y0+a*tau+rng.normal(scale=0.48)
            rows.append((pid,x,l,prev_a,prev_l,t/horizon,a,y,tau,p))
            prev_l,prev_a=l,a
    z=np.asarray(rows,dtype=np.float64)
    return dict(pid=z[:,0].astype(int),features=z[:,1:6],a=z[:,6].astype(int),
                y=z[:,7],true_ite=z[:,8],true_propensity=z[:,9])

def split_by_patient(d,seed):
    ids=np.unique(d["pid"])
    order=np.random.default_rng(seed+840).permutation(ids);n=len(ids)
    masks=[np.isin(d["pid"], subset) for subset in
           [order[:int(.7*n)],order[int(.7*n):int(.85*n)],order[int(.85*n):]]]
    assert sum(m.sum() for m in masks)==len(d["pid"])
    assert not (masks[0]&masks[2]).any()
    return masks

def train_neural(xtr,atr,ytr,xval,aval,yval,seed,epochs,device):
    import torch
    from torch import nn
    random.seed(seed);np.random.seed(seed);torch.manual_seed(seed);torch.set_num_threads(2)
    if device=="cuda" and not torch.cuda.is_available():
        raise RuntimeError("GPU requested but no CUDA device available")
    dev=torch.device(device)
    model=nn.Sequential(nn.Linear(xtr.shape[1]+1,48),nn.ReLU(),
                        nn.Linear(48,32),nn.ReLU(),nn.Linear(32,1)).to(dev)
    def ts(v):return torch.tensor(v,dtype=torch.float32,device=dev)
    xx=ts(np.column_stack([xtr,atr]));yy=ts(ytr).reshape(-1,1)
    xv=ts(np.column_stack([xval,aval]));yv=ts(yval).reshape(-1,1)
    opt=torch.optim.AdamW(model.parameters(),lr=.004,weight_decay=.0001)
    best=float("inf");weights=None;best_epoch=0;stale=0
    for epoch in range(epochs):
        model.train()
        for ind in torch.randperm(len(xx),device=dev).split(256):
            loss=torch.mean((model(xx[ind])-yy[ind])**2)
            opt.zero_grad();loss.backward();opt.step()
        model.eval()
        with torch.no_grad():val=float(torch.mean((model(xv)-yv)**2).item())
        if val<best-.00005:
            best=val;best_epoch=epoch+1;stale=0
            weights={k:v.detach().clone() for k,v in model.state_dict().items()}
        else:stale+=1
        if stale>=12:break
    model.load_state_dict(weights);model.eval()
    def pred(x,treatment):
        with torch.no_grad():
            a=ts(np.column_stack([x,np.full(len(x),treatment)]))
            return model(a).cpu().numpy().reshape(-1).astype(np.float64)
    return pred,dict(best_epoch=best_epoch,epochs_attempted=epoch+1,
                     validation_mse=best,device=device)

def experiment(seed=40,n_patients=1200,epochs=45,device="cpu"):
    start=time.perf_counter()
    d=simulate(n_patients=n_patients,seed=seed)
    train,val,test=split_by_patient(d,seed)
    f=d["features"];mean=f[train].mean(0);sd=np.maximum(f[train].std(0),1e-8)
    x=(f-mean)/sd
    a=d["a"];y=d["y"];true=d["true_ite"][test]
    naive=float(y[train&(a==1)].mean()-y[train&(a==0)].mean())
    ridge=Ridge(alpha=4).fit(np.column_stack([x[train],a[train]]),y[train])
    linear=float(ridge.coef_[-1])
    predictor,training=train_neural(x[train],a[train],y[train],x[val],a[val],y[val],seed,epochs,device)
    y0=predictor(x[test],0);y1=predictor(x[test],1);estimated=y1-y0
    def stats(pred):
        return dict(pehe_rmse=round(float(np.sqrt(np.mean((pred-true)**2))),6),
                    estimated_ate=round(float(np.mean(pred)),6),
                    ate_abs_error=round(abs(float(np.mean(pred-true))),6))
    methods={
      "naive_unadjusted_difference":stats(np.full(len(true),naive)),
      "ridge_adjusted_constant_effect":stats(np.full(len(true),linear)),
      "pytorch_nonlinear_s_learner":stats(estimated)
    }
    propensity=LogisticRegression(max_iter=400).fit(x[train],a[train])
    p=np.clip(propensity.predict_proba(x[test])[:,1],.05,.95)
    aipw=estimated+a[test]*(y[test]-y1)/p-(1-a[test])*(y[test]-y0)/(1-p)
    test_ids=d["pid"][test];patient_ate=np.asarray([aipw[test_ids==i].mean() for i in np.unique(test_ids)])
    estimate=float(patient_ate.mean());se=float(patient_ate.std(ddof=1)/np.sqrt(len(patient_ate)))
    return dict(seed=seed,n_patients=n_patients,time_steps_per_patient=6,
                train_patients=int(np.unique(d["pid"][train]).size),
                validation_patients=int(np.unique(d["pid"][val]).size),
                test_patients=int(np.unique(test_ids).size),
                test_decisions=int(test.sum()),
                true_ate_test=round(float(true.mean()),6),
                treatment_prevalence_test=round(float(a[test].mean()),6),
                methods=methods,
                independent_test_aipw_ate=round(estimate,6),
                independent_test_aipw_patient_cluster_se=round(se,6),
                independent_test_aipw_95pct_ci=[round(estimate-1.96*se,6),round(estimate+1.96*se,6)],
                neural_training=training,runtime_seconds=round(time.perf_counter()-start,3),
                gpu_speedup_measured=False,
                limitations=[
                  "Fully synthetic; no antibiotic or sepsis inference.",
                  "Immediate one-step treatment effect, not a multi-step regime effect.",
                  "This is NOT a reproduction of the T4, VTDNet or G-Transformer papers.",
                  "Known PEHE reference comes from simulated potential outcomes.",
                  "Patient-independent holdout; cluster SE over held-out patient trajectories."
                ])

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--seeds",default="40,41,42")
    p.add_argument("--patients",type=int,default=1200)
    p.add_argument("--epochs",type=int,default=45)
    p.add_argument("--device",choices=["cpu","cuda"],default="cpu")
    p.add_argument("--out",type=Path,default=Path("results/causal_benchmark.json"))
    args=p.parse_args()
    seeds=[int(s) for s in args.seeds.split(",") if s.strip()]
    runs=[experiment(s,args.patients,args.epochs,args.device) for s in seeds]
    names=list(runs[0]["methods"])
    avg={name:{metric:round(float(np.mean([r["methods"][name][metric] for r in runs])),6)
               for metric in ["pehe_rmse","ate_abs_error"]} for name in names}
    result=dict(protocol="Independent one-step longitudinal causal simulation v1",
                n_repeats=len(runs),seeds=seeds,aggregate_mean_metrics=avg,runs=runs,
                clinical_effect_estimated=False,published_paper_benchmark_reproduced=False)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2)+"\n",encoding="utf8")
    print(json.dumps(dict(aggregate=avg,runs_summary=[
        dict(seed=r["seed"],true_ate=r["true_ate_test"],
             aipw=r["independent_test_aipw_ate"],
             training=r["neural_training"],runtime=r["runtime_seconds"])
        for r in runs]),indent=2))

if __name__=="__main__": main()
