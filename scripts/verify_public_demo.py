"""Release gate for the *public* MIMIC-IV-ED Demo v2.2 only.

Verify the official distribution's SHA256 manifest against all tracked demo
tables and license; detect accidental additions to data/. No patient rows
are emitted to logs. This cannot audit private Git history.
"""
from __future__ import annotations
import hashlib
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
DATA=BASE/"data"
EXPECTED={
    "diagnosis.csv.gz","edstays.csv.gz","medrecon.csv.gz",
    "pyxis.csv.gz","triage.csv.gz","vitalsign.csv.gz",
    "LICENSE.txt","SHA256SUMS.txt","README.md"
}
def verify(root:Path=DATA)->dict:
    actual={p.name for p in root.iterdir() if p.is_file()}
    assert actual==EXPECTED, f"Unexpected/missing data filenames: {sorted(actual^EXPECTED)}"
    sums=(root/"SHA256SUMS.txt").read_text(encoding="utf-8").splitlines()
    names=set()
    for line in sums:
        digest,relative=line.split(maxsplit=1)
        assert relative=="LICENSE.txt" or relative.startswith("ed/")
        name=Path(relative).name
        assert name not in names
        names.add(name)
        observed=hashlib.sha256((root/name).read_bytes()).hexdigest()
        if digest.lower()!=observed:
            raise AssertionError(f"SHA256 mismatch for {name}")
    assert names==EXPECTED-{"SHA256SUMS.txt","README.md"}
    return {"verified_demo_files":len(names),"all_manifest_hashes_match":True,
            "source":"MIMIC-IV-ED Demo v2.2, PhysioNet",
            "doi":"10.13026/jzz5-vs76",
            "license":"Open Data Commons Open Database License v1.0"}

if __name__=="__main__":
    print(verify())
