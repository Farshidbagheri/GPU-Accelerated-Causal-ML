# GPU-Accelerated Causal Machine Learning

**Decision-time reliability and computational scalability for longitudinal treatment-effect research**

This repository supports doctoral research on the causal effects of antibiotic initiation timing in sepsis. Its engineering goal is to make repeated counterfactual analyses **auditable, statistically credible, and eventually more computationally efficient**, rather than to automate antibiotic prescribing.

![Research system architecture](figures/research-system-architecture.svg)


**Research-to-code traceability:** [Which elements of the antibiotic-timing dissertation are implemented, simulated, or still proposed](docs/research-traceability.md).

## Research architecture

1. **Clinical decision contract** — define eligible patients, landmark time, available history, treatment strategies, outcome horizon, and identification assumptions.
2. **Temporal evidence audit** — distinguish event, charting, result-availability and administration timestamps before building predictors.
3. **Causal modeling** — evaluate factual outcomes and counterfactual estimators with controlled simulations and transparent comparators.
4. **Reliability gates** — test overlap, temporal sensitivity, known-truth error, uncertainty and failure conditions.
5. **Computational profiling** — benchmark the same validated workload on CPU and CUDA, accounting for training, memory, data transfer and numerical agreement.

Partial scientific experiments are described below. **A small synthetic CPU/CUDA performance benchmark has now been measured**; full GPU acceleration of the proposed longitudinal causal validation pipeline is still a research objective. See [technical architecture](docs/architecture.md).

## New: simulated individualized risk-from-waiting curves

A completed [factual-only synthetic treatment-start experiment](docs/personalized-risk-curve-experiment.md) learns patient-dependent risk curves across five simulated intervention times. On three GitHub-tested seeds, mean curve RMSE was **0.0381** for an IPW neural learner, **0.0411** for an unweighted neural learner and **0.1989** for unadjusted group means, against *known simulator* counterfactual truth. These are not effects of actual antibiotics. The initial GitHub-hosted profiler ran on CPU only; a **subsequent user-executed Google Colab Tesla T4 run measured CUDA inference** on the same family of synthetic timing-response experiments.

![Known synthetic timing-response and estimated curve](figures/personalized-risk-curves.svg)

## Real Tesla T4 benchmark (Colab, 21 October 2026)

Using **identical trained model weights** for CPU and CUDA synthetic inference, a Google Colab Tesla T4 run measured:

| Workload | CPU median | CUDA median | Observed ratio | Numerical check |
| --- | ---: | ---: | ---: | --- |
| 3,200 synthetic individuals × 5 timing options | 26.820 ms | 1.259 ms | 21.30× | Max difference 1.19×10⁻⁷ |
| **160,000 synthetic individuals × 5 options** | **237.679 ms** | **20.659 ms** | **11.50×** | Max difference 1.19×10⁻⁷ |
| End-to-end training + evaluation (three seeds) | 1.592 s | 1.199 s | 1.33× | Independently trained; no weight parity |

These are **three-repeat, single-session synthetic measurements**, not multi-platform performance guarantees. The CPU and GPU training results use independently fitted models; their 1.33× result is exploratory. There is **no measured causal effect in sepsis patients**.

[Executed original Colab notebook and exact sources](experiments/colab-t4/README.md) · [Full measured benchmark provenance](reports/colab-runs/2026-10-21-t4/README.md)

## Results supported by executed code

| Evidence | Experiment and interpretation | Verification |
| --- | --- | --- |
| **Reproduced prior work** | Re-ran 100 synthetic experiments from the authors' *Off by a Beat* notebook (2026). Simulated policy values **3.343 vs 9.878** match its stored outputs. This is **not** the paper's clinical experiment. | [Workflow](https://github.com/Farshidbagheri/GPU-Accelerated-Causal-ML/actions/runs/39530437176) |
| **Independent causal-learning baseline** | PyTorch outcome model trained on three synthetic, patient-disjoint longitudinal datasets; mean **PEHE-RMSE 0.287** versus **0.641** for adjusted Ridge and **2.912** for a naive comparator. These are synthetic one-step treatment effects, **not** clinical antibiotic effects. | [Workflow](https://github.com/Farshidbagheri/GPU-Accelerated-Causal-ML/actions/runs/39531676558) |
| **Real-data documentation audit** | Open MIMIC-IV-ED Demo (100 deidentified patients, **222 ED stays**, **1,038** vital-sign records). Analyzed documentation timing against hypothetical decision cutoffs, **not** trained-model leakage or efficacy. | [Workflow](https://github.com/Farshidbagheri/GPU-Accelerated-Causal-ML/actions/runs/39542809955) |
| **Model integration assessments** | VTDNet upstream architecture: reduced CPU forward/backward smoke check only. T4: paper-level reproduction blocked by missing/incompatible original preprocessing inputs. | [Model registry](models/README.md) |

![Synthetic known-truth error comparison](figures/synthetic_counterfactual_pehe.svg)

**Important boundary:** A CUDA speedup was measured only for a synthetic inference workload; no CUDA throughput or clinically identified effect of delayed antibiotic administration in real EHR has been established. Full T4 and VTDNet paper metrics have **not** been reproduced.

## Repository layout

```text
.github/workflows/     Continuous integration and separately scoped experiments
data/                  Open MIMIC-IV-ED Demo tables + original license/checksums
experiments/           Executed Colab notebook with exact benchmark sources and outputs
docs/                  Architecture, reproducibility, experiment matrix, data governance
figures/               Editable research diagrams and result summaries
models/                External-method registry and scope of reproduction
reports/               Auditable aggregate results, protocols and machine-readable summaries
scripts/               Data integrity, timestamp audit and paper-integration checks
src/                   Temporal data validation and longitudinal causal benchmark
tests/                 Patient-split, timing and implementation unit tests
```

### Quickstart: verified open-data audit

Requires Python 3.11; does not need a GPU.

```bash
python -m pip install -r requirements.txt
python scripts/verify_public_demo.py
python -m pytest -q tests/test_timing_audit.py tests/test_run_pilot.py
python scripts/run_pilot.py --data data --out results --offsets 30,60,120
```

### Run model benchmarks

- [Causal estimator code](src/longitudinal_synthetic_benchmark.py) · [CPU-run CI](.github/workflows/causal-benchmark.yml)
- [Published temporal-alignment toy reproduction](scripts/reproduce_offbyabeat_toy.py) · [CI](.github/workflows/reproduce-offbyabeat-toy.yml)
- [Upstream VTDNet architecture smoke](scripts/vtdnet_upstream_smoke.py) · [CI](.github/workflows/vtdnet-architecture.yml)
- [Experiment evidence](reports/research-evidence.md) · [Experimental scope matrix](docs/experiment-matrix.md)

Separate model jobs install their own dependencies. Standard hosted GitHub Actions runners here provide CPU; they are **not** evidence of GPU execution.

## Data, licenses and attribution

The checked-in ED data are the **public MIMIC-IV-ED Demo v2.2**, not the credential-restricted full dataset. Source: Johnson et al. (2023), PhysioNet, [DOI 10.13026/jzz5-vs76](https://doi.org/10.13026/jzz5-vs76), **Open Data Commons Open Database License 1.0**. Source files and hashes are preserved; [CI checks the distribution hashes](https://github.com/Farshidbagheri/GPU-Accelerated-Causal-ML/actions/runs/39542809361).

[Data and licensing](docs/data-and-licensing.md) · [Reproducibility protocol](docs/reproducibility.md)

**Data folder:** [source, table descriptions and usage boundaries](data/README.md). **External models:** [source links and exact validation status](models/README.md).

**Code license:** No open-source software license has been assigned to the original Python code. The data's ODbL license does not automatically license that code. Do not upload credential-restricted data, identifiable records, secrets, or unapproved institutional data here.

**Research:** Farshid Bagheri Saravi, Case Western Reserve University.
