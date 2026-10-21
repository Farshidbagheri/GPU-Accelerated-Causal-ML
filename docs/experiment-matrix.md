# Experimental status and acceptance criteria

| Experiment | Evidence category | Completed | Not yet established |
| --- | --- | --- | --- |
| Open MIMIC-IV-ED Demo timing audit | Descriptive **real, deidentified demo** data | 222 stays; 1,038 vital-sign chart records; 5 tests | Real antibiotic effect, true decision-time availability, trained-model leakage |
| 2026 temporal-misalignment toy | Published authors' **synthetic** notebook | 100 original simulation runs; reproducible values 3.343 and 9.878 | 750-state clinical result, antibiotic inference |
| Our nonlinear S-learner benchmark | **Independent synthetic** simulation | Three independent patient-disjoint seeds; neural PEHE-RMSE 0.287 vs Ridge 0.641 | Multi-step regime effects, clinical generalizability, GPU advantage |
| VTDNet reduced architecture | Upstream source inspection and smoke test | CPU forward/backward and finite loss after device patch | Published PEHE, causal parameter recovery |
| T4 code audit | Static integration review | Interface and missing-data blockers documented | Published time-to-treatment results |
| Future CUDA benchmarking | Planned | CPU training baseline exists; CUDA option in PyTorch code | GPU runtime, speedup, fidelity validation |

See [results and exact provenance](../reports/research-evidence.md). This classification prevents method readiness from being mistaken for empirical validation.

## Priorities before claiming experimental novelty

1. Preserve code, seeds, data provenance and a demonstrably equivalent baseline.
2. Specify a unique methodological contribution *beyond* recombining existing estimators; benchmark against timely prior art.
3. Define allowable clinical decision-time information and admissible observational assumptions.
4. Report negative findings and compute-bound bottlenecks, including a null or negative CUDA speedup.

The longer-term dissertation question remains open: safe and causally credible individualized antibiotic timing in patients with suspected sepsis.
