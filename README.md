# Decision-time auditing for clinical EHR sequences

Reproducible **descriptive** audit of what recorded emergency-department vital signs would be available under a hypothetical decision-time cutoff, using the **real, openly released MIMIC-IV-ED Demo (100 deidentified patients)**.

**Research question:** What fraction of recorded EHR events would inadvertently leak into a model if a decision taken 60 minutes after ED arrival were modeled using whole-stay data?

**It does not estimate an antibiotic treatment effect, identify sepsis, verify drug administration, make treatment recommendations, or claim clinical validity.** `charttime` is documentation time and not proof of measurement/result availability; the 60-minute decision cutoff is illustrative and not an actual observed treatment decision. Medication Pyxis data represent charted dispensations, not verified first-IV-antibiotic administrations. The small demo has no power for clinical causal inference.

## Reproduce locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/download_demo.py --out data/raw
python scripts/run_pilot.py --data data/raw --out results --offset-minutes 60
pytest -q
```

Outputs: `results/per_stay_audit.csv` and `results/audit_metrics.json` (not committed). The repo includes **no patient-level data, identifiers, or generated patient outputs**.

## Source and license

MIMIC-IV-ED Demo v2.2, Johnson et al. (2023), doi: [10.13026/jzz5-vs76](https://doi.org/10.13026/jzz5-vs76), released under the Open Data Commons Open Database License 1.0. Download from PhysioNet directly, read its license, do not upload private MetroHealth or credentialed PhysioNet data to this repository.

## Relation to dissertation

This audit tests one necessary software invariant for later antibiotic-timing causal analyses: only information that predates a modeled action should reach its prediction/estimation stage. A full longitudinal causal study additionally needs validated time zero, antibiotic *administration* records, eligibility, follow-up outcomes, confounders, censoring, positivity checks and falsification/sensitivity analysis. That phase is **not implemented** here.

## External work (reference only, not vendored)

- T4: https://github.com/ruoqi-liu/T4
- VTDNet: https://github.com/Throwfox/VTDNet
- Off by a Beat: https://github.com/shengpu-tang/RL-Off-by-a-Beat
- Precision Medication: https://github.com/zizhendeng/Precision-Medication

Methods, licenses, and empirical claims from these projects remain their authors'. This repository does not represent a reproduction of their published benchmark results.
