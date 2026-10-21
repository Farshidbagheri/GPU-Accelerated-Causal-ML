"""Matched CPU/CUDA test of synthetic risk-curve training, never fake CUDA."""
import argparse,json,time,platform,sys
from pathlib import Path
import torch,psutil
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from personalized_delay_synthetic import run
def execute(device,seeds,n,epochs,draws):
    if device=='cuda' and not torch.cuda.is_available():
        return {'status':'NOT_RUN_NO_CUDA','runs':[]}
    observations=[]
    for seed in seeds:
        if device=='cuda':torch.cuda.reset_peak_memory_stats();torch.cuda.synchronize()
        t=time.perf_counter()
        result=run(seed,n,epochs,device,draws)
        if device=='cuda':torch.cuda.synchronize()
        observations.append({'seed':seed,'elapsed_seconds':round(time.perf_counter()-t,5),
                             'ipw_curve_rmse':round(result['scores']['ipw']['curve_rmse'],6),
                             'rss_bytes':psutil.Process().memory_info().rss,
                             'cuda_peak_allocated_bytes':torch.cuda.max_memory_allocated() if device=='cuda' else None})
    measurements=sorted(x['elapsed_seconds'] for x in observations)
    return {'status':'COMPLETED','runs':observations,'median_seconds':measurements[len(measurements)//2]}
def main():
    p=argparse.ArgumentParser()
    p.add_argument('--seeds',default='41,42,43')
    p.add_argument('--patients',type=int,default=3200)
    p.add_argument('--epochs',type=int,default=70)
    p.add_argument('--oracle-draws',type=int,default=64)
    p.add_argument('--out',type=Path,default=Path('results/compute-profiling.json'))
    a=p.parse_args()
    seed_list=[int(s) for s in a.seeds.split(',')]
    cpu=execute('cpu',seed_list,a.patients,a.epochs,a.oracle_draws)
    gpu=execute('cuda',seed_list,a.patients,a.epochs,a.oracle_draws)
    speedup=round(cpu['median_seconds']/gpu['median_seconds'],4) if gpu['status']=='COMPLETED' else None
    out={'experiment':'Matched end-to-end synthetic policy curve benchmarking',
         'machine':{'platform':platform.platform(),'torch':torch.__version__,
                    'cuda_available':torch.cuda.is_available(),
                    'cuda_device':torch.cuda.get_device_name(0) if torch.cuda.is_available() else None},
         'protocol':{'seeds':seed_list,'n':a.patients,'epochs':a.epochs,'oracle_draws':a.oracle_draws},
         'cpu':cpu,'cuda':gpu,'measured_gpu_speedup':speedup,
         'no_clinical_treatment_effect_claim':True}
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'CPU_median_sec':cpu['median_seconds'],'CUDA_status':gpu['status'],
                      'measured_GPU_speedup':speedup},indent=2))
if __name__=='__main__':main()
