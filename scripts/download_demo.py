"""Download the small, explicitly open PhysioNet ED demo; do not redistribute patient tables."""
from __future__ import annotations
import argparse,hashlib,json,datetime
from pathlib import Path
from urllib.request import urlopen

BASE = 'https://physionet.org/files/mimic-iv-ed-demo/2.2/'
FILES = ['ed/edstays.csv.gz','ed/vitalsign.csv.gz','ed/pyxis.csv.gz','LICENSE.txt']

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--out',default='data/raw')
    args=p.parse_args()
    root=Path(args.out);root.mkdir(parents=True,exist_ok=True)
    manifest={'source':BASE,'doi':'10.13026/jzz5-vs76','accessed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':[]}
    for item in FILES:
        dst=root/Path(item).name
        with urlopen(BASE+item,timeout=45) as resp: data=resp.read()
        dst.write_bytes(data)
        manifest['files'].append({'name':dst.name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
        print(dst, len(data),'bytes')
    (root/'provenance.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')

if __name__=='__main__': main()
