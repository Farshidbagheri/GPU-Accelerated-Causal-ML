# GPU-Accelerated Causal Machine Learning — Research Benchmarks

**Scientific objective:** trustworthy, scalable longitudinal causal estimation for clinical treatment-timing decisions. **Current evidence:** carefully separated CPU-only synthetic-model experiments and a descriptive audit of an openly licensed ED dataset. GPU acceleration and patient-level antibiotic effects are **proposed research**, not completed outcomes.

## Verified experimental evidence

| Study | Scope | Independently executed results | Verification |
| --- | --- | --- | --- |
| **Temporal alignment** — *Off by a Beat*, 2026 | 100-run authors' **synthetic toy notebook** | Policy value **3.343** versus **9.878**, exactly matching original notebook outputs | [CI](https://github.com/Farshidbagheri/GPU-Accelerated-Causal-ML/actions/runs/39530437176) |
| **Longitudinal causal estimation** | Independently designed simulated patients with known individual treatment effects | Three-seed mean **PEHE-RMSE: 0.287** PyTorch nonlinear, **0.641** adjusted Ridge, **2.912** naive | [CI](https://github.com/Farshidbagheri/GPU-Accelerated-Causal-ML/actions/runs/39531676558) |
| **Emergency-department documentation timing** | Open *MIMIC-IV-ED Demo* v2.2, 100 deidentified patients / **222 stays** | Audit of **1,038** vital-sign entries at three hypothetical ED decision cutoffs | [CI](https://github.com/Farshidbagheri/GPU-Accelerated-Causal-ML/actions/runs/39532311022) |
| **VTDNet** (2025) | Authors' original code, reduced CPU test | Forward and backward pass successful with CPU-placement patch | [CI](https://github.com/Farshidbagheri/GPU-Accelerated-Causal-ML/actions/runs/39532009883) |
| **T4** (2023) | Source/data interface assessment | Full paper reproducibility **blocked** by missing/incompatible preprocessing inputs | [Assessment](models/t4/README.md) |

![Independent simulated counterfactual benchmark](figures/synthetic_counterfactual_pehe.svg)

## How the scientific program fits together

1. **Define the decision-time question:** eligibility, outcome horizon, treatment administration, and what information was available before a decision.
2. **Stress-test timestamps:** repeat identical estimands under alternative defensible clinical-data availability assumptions; distinguish descriptive documentation audits from fitted-model information leakage.
3. **Validate causal estimation:** use simulated known counterfactuals to score PEHE and ATE error; only evaluate observational clinical effects when data access and identification assumptions support them.
4. **Investigate accelerated computing:** profile end-to-end reference CPU workloads, then compare matched CUDA workloads (wall-clock time, memory, valid-scenario throughput and numerical parity). **No GPU benchmark has yet been run.**

The goal is not to turn a synthetic test into a clinical prescribing recommendation. The dissertation investigates **optimal timing of antibiotics in sepsis**, but no effect of antibiotic timing has been estimated from patient data in this repository.

## Reproduce the verified work

| Experiment | Entry point |
| --- | --- |
| ED public demo audit | `python scripts/run_pilot.py --data data --out results --offsets 30,60,120` |
| Verify public demo checksum manifest | `python scripts/verify_public_demo.py` |
| Synthetic neural model, baselines, three seeds | [Benchmark source](src/longitudinal_synthetic_benchmark.py) / [independent workflow](.github/workflows/causal-benchmark.yml) |
| Author notebook reproduction | [Pinned-source workflow](.github/workflows/reproduce-offbyabeat-toy.yml) |
| VTDNet inspection | [Pinned-source workflow](.github/workflows/vtdnet-architecture.yml) |

Quick setup for the **ED demo** (Python 3.11):

```bash
python -m pip install -r requirements.txt
python scripts/verify_public_demo.py
python -m pytest -q tests/test_timing_audit.py tests/test_run_pilot.py
python scripts/run_pilot.py --data data --out results --offsets 30,60,120
```

GPU is **not required** for the completed experiments. Neural-model dependencies are installed by their dedicated GitHub Actions job, not by the ED demo `requirements.txt`.

## Provenance, permissions, detailed reports

- [Evidence ledger and provenance](reports/RESEARCH_EVIDENCE_SUMMARY_v6.md) · [Experiment scope/status](docs/EXPERIMENT_STATUS.md)
- [Data license, attribution, checksum verification, and privacy restrictions](docs/PUBLIC_DATA_AND_LICENSING.md)
- [Original MIMIC-IV-ED Demo v2.2](https://doi.org/10.13026/jzz5-vs76) — **ODbL 1.0**, not the credentialed full MIMIC-IV-ED database
- [2026 authors' toy reproduction report](reports/offbyabeat_toy_reproduction.md)
- [ED documentation audit report](reports/ed_demo_timing_audit_v1.md)
- [VTDNet reproducibility assessment](models/vtdnet/README.md) · [T4 assessment](models/t4/README.md)

**Publication safeguards:** No credential-restricted clinical data should be uploaded to GitHub. No passwords or API tokens belong in this repository. The **ODbL data license does not grant a software license for the independently written Python code**; a code license may be selected separately by the owner.

**Research contact:** Farshid Bagheri Saravi, Department of Electrical, Computer and Systems Engineering, Case Western Reserve University.
