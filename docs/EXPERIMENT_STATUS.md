# What is implemented — 21 October 2026

| Component | Source/data | What actually ran | Claim allowed |
| --- | --- | --- | --- |
| EHR timing audit | Open 100-person MIMIC-IV-ED Demo | Documentation-time cutoffs for **222 visits**, 1,038 vital-sign entries; 5 tests | Descriptive data-timing audit; **not** detected leakage from a trained model |
| Off by a Beat | Pinned 2026 authors' synthetic notebook | **100-run original toy experiment**, matching saved author outputs (3.343/9.878) | Reproduction of *toy simulation only* |
| Neural causal baseline | **Independent synthetic** longitudinal patients | Train a PyTorch nonlinear S-learner and two comparators, three seeds; PEHE 0.287 neural / 0.641 Ridge / 2.912 naive | Synthetic one-step inference; **not** T4 or VTDNet |
| VTDNet | Authors' pinned source | Reduced-size forward/backward test with CPU device compatibility edit | Architecture compatibility only, *not* paper PEHE |
| T4 | Authors' source and README | Data/interface review | Incompatible missing preprocessing; **not reproduced** |
| GPU training/speedup | — | **None** | Planned, not a finding |
| Antibiotic-timing causal effects | — | **None on patients** | Dissertation objective, not a finding |

Full evidence: [research report](../reports/RESEARCH_EVIDENCE_SUMMARY_v6.md). Tests are run on bounded CPU-only GitHub Actions with downloadable aggregates; do not equate passing tests with clinical or statistical validation.

## Reproducibility

- [Demo data integrity](../scripts/verify_public_demo.py), [CI](../.github/workflows/public-release.yml)
- [ED audit](../scripts/run_pilot.py), [CI](../.github/workflows/test.yml)
- [Authors' synthetic reproduction](../scripts/reproduce_offbyabeat_toy.py), [CI](../.github/workflows/reproduce-offbyabeat-toy.yml)
- [Neural simulation](../src/longitudinal_synthetic_benchmark.py), [CI](../.github/workflows/causal-benchmark.yml)
- [VTDNet inspection](../scripts/vtdnet_upstream_smoke.py), [CI](../.github/workflows/vtdnet-architecture.yml)

The first two run on real **public demo** files; the neural and toy experiments use **synthetic** data only.
