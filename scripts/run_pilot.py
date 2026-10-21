"""Aggregate-only audit of decision-time eligibility using public ED demo data.

Cutoffs are hypothetical. No clinical decision, treatment effect or antibiotic
administration is inferred.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from timing_audit import audit_vitals, pyxis_descriptive_audit


def analyze(data: Path, offsets: list[int]) -> dict:
    stays = pd.read_csv(data / "edstays.csv.gz")
    vitals = pd.read_csv(data / "vitalsign.csv.gz")
    report = {
        "dataset": "MIMIC-IV-ED Demo v2.2 (public, deidentified)",
        "scope": "descriptive documentation-timestamp eligibility",
        "decision_times": "hypothetical minutes after ED arrival",
        "n_stays": int(stays.stay_id.nunique()),
        "offsets": {},
        "limitations": [
            "Charttime is not verified information availability.",
            "No antibiotic administration or causal effects estimated.",
            "The 100-patient demo is not suitable for clinical inference."
        ]
    }
    for offset in sorted(set(offsets)):
        if offset < 0:
            raise ValueError("Offsets must be >= 0")
        _, stats = audit_vitals(stays, vitals, offset_minutes=offset)
        n = stats["n_vitals_events"]
        stats["post_decision_fraction_all_events"] = (
            round(stats["n_post_decision_events"] / n, 6) if n else None
        )
        report["offsets"][str(offset)] = stats
    if (data / "pyxis.csv.gz").exists():
        report["pyxis"] = pyxis_descriptive_audit(stays, pd.read_csv(data / "pyxis.csv.gz"))
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data")
    parser.add_argument("--out", default="results")
    parser.add_argument("--offsets", default="30,60,120")
    args = parser.parse_args()
    offsets = [int(x.strip()) for x in args.offsets.split(",") if x.strip()]
    if not offsets:
        parser.error("Provide at least one cutoff minute")
    report = analyze(Path(args.data), offsets)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "aggregate_audit.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
