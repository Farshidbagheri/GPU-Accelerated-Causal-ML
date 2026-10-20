"""Run ED decision-time descriptive audit after downloading the demo."""
import argparse,json,sys
from pathlib import Path
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from timing_audit import audit_vitals,pyxis_descriptive_audit

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--data',default='data/raw');ap.add_argument('--out',default='results');ap.add_argument('--offset-minutes',type=int,default=60);args=ap.parse_args()
    d=Path(args.data); out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    stays=pd.read_csv(d/'edstays.csv.gz'); vitals=pd.read_csv(d/'vitalsign.csv.gz')
    per,metrics=audit_vitals(stays,vitals,args.offset_minutes)
    per.to_csv(out/'per_stay_audit.csv',index=False)
    if (d/'pyxis.csv.gz').exists():metrics['pyxis_audit']=pyxis_descriptive_audit(stays,pd.read_csv(d/'pyxis.csv.gz'))
    (out/'audit_metrics.json').write_text(json.dumps(metrics,indent=2),encoding='utf-8')
    print(json.dumps(metrics,indent=2))

if __name__=='__main__':main()
