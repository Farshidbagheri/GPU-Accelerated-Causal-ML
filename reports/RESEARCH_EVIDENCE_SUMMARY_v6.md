# Completed verification cycle — NVIDIA research evidence package v6

**Date:** 21 October 2026  
**Scope:** End-to-end software experiment verification for a GPU-accelerated causal ML dissertation proposal.  
**Result:** One original authors' synthetic toy experiment successfully reproduced; one **new, independently designed and trained PyTorch counterfactual benchmark** completed with baselines on three seeds; one upstream VTDNet architecture compatibility test completed; public ED documentation audit preserved.

## Evidence dashboard

| Experiment | Verified result | GitHub Actions proof | Limits |
| --- | --- | --- | --- |
| ED Demo | 222 visits, 1,038 vital-sign records; 5 tests | [Audit](https://github.com/Farshidbagheri/GPU-Accelerated-Causal-ML/actions/runs/39530223244) | Documentation audit, no ITE |
| Off by a Beat (2026) | 100 original notebook sweeps: reward 3.34337 vs 9.87805, **exact authors' notebook match** | [Original-author toy reproduction](https://github.com/Farshidbagheri/GPU-Accelerated-Causal-ML/actions/runs/39530437176) | Toy simulation, no clinical reproduction |
| Independent longitudinal causal model | Three patient-disjoint seeds: **PEHE 2.912 naive; 0.641 Ridge; 0.287 PyTorch** | [Causal model](https://github.com/Farshidbagheri/GPU-Accelerated-Causal-ML/actions/runs/39531676558) | Fully synthetic, one-step effects, not original T4/VTDNet |
| VTDNet (2025) | Reduced upstream architecture forward/backward passed after CPU device patch; potential batch-dependence flagged | [VTDNet inspection](https://github.com/Farshidbagheri/GPU-Accelerated-Causal-ML/actions/runs/39532009883) | **No original VTDNet training, PEHE, or clinical claims** |
| T4 (2023) | Code/data-interface barriers documented | [Readiness assessment](../models/t4/README.md) | No author paper reproduction |

![Measured PEHE](../figures/synthetic_counterfactual_pehe.svg)

## Independent trained neural estimator: protocol and measured scores

**Synthetic data:** 1,200 patients per seed; six repeated, ordered decisions per patient. The current measured covariate is affected by previous treatment and confounds current treatment/outcome. The simulator supplies potential outcome effects as ground truth *only for evaluation*. Inputs to estimators are decision-time covariates and past treatment (no future features); models train using factual outcomes alone. Split is by **patient**, 70% training, 15% validation, 15% holdout.

| Method | PEHE-RMSE ↓, mean of three seeds | Absolute ATE error ↓, mean |
| --- | ---: | ---: |
| Naive treated-minus-untreated | 2.912222 | 2.844957 |
| Covariate-adjusted Ridge S-learner | 0.640825 | 0.152510 |
| PyTorch nonlinear S-learner | **0.287209** | **0.027648** |

Relative PEHE-RMSE reduction of neural versus linear baseline: **55.2%** on this specific *synthetic* data-generating process. Relative reductions are **not** general clinical performance claims. Three seeds alone do not provide publication-grade uncertainty for superiority; larger parameter sweeps and independent simulations are needed. An auxiliary AIPW score used independent test patients and patient-clustered standard errors; full JSON artifact is on the workflow.

### Why this is relevant to the dissertation

We now have verified code for a measurable causal-estimation outcome, tests, and a precedent demonstration that temporal indexing can alter learned policies. They support **feasibility and motivation**, not any claim that individualized antibiotic-start times can already be estimated safely from actual EHR data.

### Critical methodological constraints

- No real clinical causal effects, mortality benefit, antibiotic policy or dose recommendations were estimated.
- No GPU speedup has been measured. Both successful model experiments ran on GitHub-hosted **CPU**.
- PEHE values here refer to known synthetic counterfactuals; PEHE cannot ordinarily be validated directly on observational patient EHR.
- VTDNet upstream code contains broken interfaces and a patient-batch coupling to investigate; a compatibility smoke test is not a peer-reviewed reproduction.
- T4's synthetic generator does not feed its main training pipeline as written; do not call it reproduced.
- No restricted MIMIC, MetroHealth, or AmsterdamUMCdb data were uploaded or used.

### What we can honestly include in the NVIDIA proposal

A concise line is defensible: *"We implemented and validated a patient-disjoint, synthetic longitudinal causal-estimation benchmark with a PyTorch outcome model and baseline comparisons; a separate published 2026 toy experiment on timestamp alignment was exactly reproduced using the authors' released notebook."*

Do **not** quote a GPU gain, sepsis benefit or claim T4/VTDNet replications. Confirm that this work belongs within the proposed dissertation methodology before including it as established progress.

### Reproduce and inspect

- [Main independent benchmark script](../src/longitudinal_synthetic_benchmark.py)
- [Independent model CI](../.github/workflows/causal-benchmark.yml)
- [Authors' 2026 synthetic experiment](offbyabeat_toy_reproduction.md)
- [VTDNet original-code audit](../models/vtdnet/README.md)
- [ED Demo time audit](ed_demo_timing_audit_v1.md)

**Status:** Software/experimental feasibility loop completed for the scope above. The *full dissertation research problem* and clinical identification remain open and are not being represented as completed.
