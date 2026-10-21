# GPU-Accelerated Causal ML — Reproducible Research Benchmarks

A reproducible **documentation-time quality** pilot using the public, deidentified [MIMIC-IV-ED Demo v2.2](https://physionet.org/content/mimic-iv-ed-demo/2.2/). It quantifies how retrospective clinical features could include documentation recorded after a hypothetical decision cutoff. This is **not** a sepsis treatment-effect estimator or clinical decision system.

## Verified research milestones

See the [**research evidence summary**](reports/RESEARCH_EVIDENCE_SUMMARY_v6.md) for independently verified results and study limitations.

- **Published 2026 simulation reproduced:** original Off by a Beat toy notebook; 100 runs; values 3.34337 vs 9.87805 exactly matched.
- **Independent PyTorch causal model trained:** 3 synthetic patient-disjoint seeds; PEHE 0.287 vs Ridge 0.641 and naive 2.912. Not a paper reproduction.
- **VTDNet upstream architecture:** CPU smoke forward/backward passed with limited device patch; full reported PEHE remains unreproduced.
- **Public real-data audit:** MIMIC-IV-ED Demo; 222 ED stays; 1,038 documentation events; not causal inference.
- **No CUDA benchmark or clinical antibiotic-treatment benefit has been established.**

![Independent model comparison](figures/synthetic_counterfactual_pehe.svg)

## Repository layout

| Path | Purpose |
| --- | --- |
| `src/timing_audit.py` | Timing validation and Pyxis event counts |
| `scripts/run_pilot.py` | Multi-cutoff aggregate summary |
| `scripts/download_demo.py` | Optional official data downloader |
| `tests/` | Constructed-data unit tests |
| `data/` | Public demo tables already uploaded by repository owner and source license |
| `.github/workflows/test.yml` | Test + actual demo-data audit |

## Reproduce

```bash
python -m pip install -r requirements.txt
python -m pytest -q tests/test_timing_audit.py tests/test_run_pilot.py
python scripts/run_pilot.py --data data --out results --offsets 30,60,120
```

The runner creates `results/aggregate_audit.json` (git-ignored). GitHub Actions retains only aggregate counts as a short-lived artifact. No restricted data, identities or per-stay reports should be published.

## Interpretation boundaries

- Cutoffs at 30, 60, and 120 minutes after ED arrival are **hypothetical probes**, not observed decisions.
- `charttime` is a documentation timestamp, not proof that a measurement or result was available to a clinician.
- Pyxis entries are dispensations, **not confirmed antibiotic administrations**.
- The 100-patient demo cannot establish causal effects of antibiotic timing, mortality, safe delays, or prescribing recommendations.
- Longitudinal causal inference requires validated treatment and outcome definitions, confounders, censoring, overlap, and sensitivity checks; these are **future research**, not implemented here.
- This project makes **no CPU-vs-GPU performance claim**.

## Data provenance and rights

The owner already uploaded the publicly released demo tables to `data/`; they are not confidential MetroHealth data. Retain `data/LICENSE.txt` and `data/SHA256SUMS.txt` when redistributing the demo. Citation: MIMIC-IV-ED Demo v2.2, PhysioNet, DOI [10.13026/jzz5-vs76](https://doi.org/10.13026/jzz5-vs76). Never add credential-restricted PhysioNet tables, MetroHealth records, secrets, or personal health information.

## External method references — not vendored or reproduced

- [T4](https://github.com/ruoqi-liu/T4)
- [VTDNet](https://github.com/Throwfox/VTDNet)
- [Off by a Beat](https://github.com/shengpu-tang/RL-Off-by-a-Beat)
- [Precision Medication](https://github.com/zizhendeng/Precision-Medication)

Check licenses, versions and input-data requirements before attempting replications; published benchmark claims belong to the respective authors.
