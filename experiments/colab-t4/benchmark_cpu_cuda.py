"""Matched synthetic-risk-curve CPU/CUDA benchmarking.

Runs only devices actually present, never estimates GPU speedup from model names.
Same dataset, seeds, model parameters and training protocol per device. Supports
CPU as a valid result and records a NOT_RUN status for absent CUDA GPUs.
"""
import argparse, json, os, platform, sys, time
from pathlib import Path
import psutil
import torch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from antibiotic_timing_synthetic import evaluate_once


def execute(device, seeds, patients, epochs, oracle_draws):
    outputs=[]
    if device=='cuda' and not torch.cuda.is_available():
        return {'status':'NOT_RUN_NO_CUDA_DEVICE','device':'cuda','runs':[],
                'explanation':'No NVIDIA CUDA GPU exposed to this runtime; no GPU timings or speedup measured.'}
    for seed in seeds:
        if device=='cuda':torch.cuda.reset_peak_memory_stats();torch.cuda.synchronize()
        start=time.perf_counter()
        run=evaluate_once(seed,patients,epochs,device,oracle_draws)
        if device=='cuda':torch.cuda.synchronize()
        elapsed=time.perf_counter()-start
        outputs.append({'seed':seed,'end_to_end_seconds':round(elapsed,5),
                        'ipw_curve_rmse':run['metrics']['factual_ipw']['curve_rmse'],
                        'unweighted_curve_rmse':run['metrics']['factual_unweighted']['curve_rmse'],
                        'max_cuda_memory_bytes':int(torch.cuda.max_memory_allocated()) if device=='cuda' else None,
                        'rss_bytes_at_end':int(psutil.Process().memory_info().rss)})
    return {'status':'COMPLETED','device':device,'runs':outputs,
            'median_end_to_end_seconds':round(sorted(x['end_to_end_seconds'] for x in outputs)[len(outputs)//2],5)}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--devices',default='cpu,cuda')
    p.add_argument('--seeds',default='41,42,43')
    p.add_argument('--patients',type=int,default=3200)
    p.add_argument('--epochs',type=int,default=70)
    p.add_argument('--oracle-draws',type=int,default=64)
    p.add_argument('--output',type=Path,default=Path('results/compute-benchmark.json'))
    a=p.parse_args()
    devices=[s.strip() for s in a.devices.split(',') if s.strip()]
    seeds=[int(s) for s in a.seeds.split(',')]
    runs={device:execute(device,seeds,a.patients,a.epochs,a.oracle_draws) for device in devices}
    cpu=runs.get('cpu',{})
    cuda=runs.get('cuda',{})
    speedup=(cpu['median_end_to_end_seconds']/cuda['median_end_to_end_seconds']
             if cpu.get('status')=='COMPLETED' and cuda.get('status')=='COMPLETED' else None)
    data={'experiment':'End-to-end matched synthetic risk-curve execution benchmark',
          'inputs':{'seeds':seeds,'patients':a.patients,'epochs':a.epochs,'oracle_draws':a.oracle_draws},
          'runtime':{'python':platform.python_version(),'torch':torch.__version__,
                     'torch_cuda_compiled':torch.version.cuda,
                     'cuda_available':torch.cuda.is_available(),
                     'cuda_device_name':torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
                     'platform':platform.platform()},
          'devices':runs,'measured_cuda_speedup':round(speedup,4) if speedup is not None else None,
          'important_scope':'Only synthetic model training and curve evaluation; not clinical causal effect.'}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(data,indent=2)+'\n',encoding='utf8')
    print(json.dumps({'devices':{k:{'status':v['status'],'median':v.get('median_end_to_end_seconds')} for k,v in runs.items()},
                      'speedup':speedup},indent=2))

if __name__=='__main__':main()
