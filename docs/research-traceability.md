# Research-to-implementation traceability

The [doctoral research proposal](https://github.com/Farshidbagheri/GPU-Accelerated-Causal-ML) and NVIDIA fellowship proposal share one primary scientific target:

> For a patient with suspected sepsis at a defined ED decision time, how does the **causal harm from additional delay** in first IV antibiotic administration vary with patient history, and what uncertainty-qualified initiation window can the data support?

**Critical distinction:** this is the research objective, **not a result already achieved by this code**. So far the repository holds a data-quality audit and two simulation-level experimental components; its clinical causal decision engine and matched GPU benchmarks remain research milestones.

## Scientific components mapped to actual evidence

| Dissertation/fellowship component | Current implementation | Evidence level | Next verification gate |
| --- | --- | --- | --- |
| **A. ED event and available-information history** | `src/timing_audit.py`, `scripts/run_pilot.py` on 100-person public ED demo | Completed descriptive audit of **charttime** (222 ED stays, 1,038 vital-sign rows); no true clinician availability or administration timestamp validation | Authorized longitudinal records with separate order/result/administration times; clinically reviewed cohort/time-zero |
| **B. Impact of temporal alignment** | `scripts/reproduce_offbyabeat_toy.py`, pinned upstream notebook | Reproduced authors' 100-run **toy simulation**; policy values agree with published notebook outputs | Evaluate temporal availability assumptions in an antibiotic-target-trial design |
| **C. Causal inference and heterogeneous effects** | `src/longitudinal_synthetic_benchmark.py`, patient-disjoint synthetic baseline | **Trained** a PyTorch nonlinear **one-step S-learner**; mean PEHE-RMSE 0.287 vs linear 0.641 on three controlled seeds | Implement dynamic initiation-regime estimands and robust g-method comparators; verify sequential identification and uncertainty |
| **D. Risk-from-waiting curves and personalized urgency windows** | Formal target defined in the dissertation/fellowship proposal; **no implemented patient-specific antibiotic-delay estimator** | Not yet experimentally demonstrated | Estimate multiple clinically feasible administration-time interventions and validate overlap, censoring, sensitivity and subgroup effects |
| **E. GPU scientific throughput** | Training script has `--device cuda` option; GitHub tests to date run on CPU | **No actual CUDA training or speedup measurement** | Execute matched CPU/CUDA workload with identical seeds/input, explicit device synchronization and estimation-fidelity checks |
| **F. Clinical outcomes and physician-facing interpretation** | Research plan only; Pyxis data in public demo measure **dispensation**, not first IV administration | No clinical treatment effect, mortality benefit or prescribing recommendation | Appropriate data-use authorization and clinician review of event, treatment, outcome and causal definitions |

### Provenance boundaries

The ED dataset is **real, public and deidentified**, but provides only the documentation-audit pilot. The learned causal model and *Off by a Beat* replication use **synthetic data**. Their numerical results do not estimate sepsis outcomes, optimal antibiotic initiation times or an NVIDIA GPU improvement. Only published authors' synthetic source is replayed; T4/G-Transformer/VTDNet full paper-level results are **not** claimed reproduced.

## Target research flow

```text
Authorized longitudinal ED data (planned)
  -> first-dose + result-availability timing definitions (planned)
  -> eligible cohorts & well-defined strategy windows (planned)
  -> counterfactual timing curves / risk-from-waiting (planned)
  -> diagnostics, sensitivity, clinical plausibility (planned)
  -> matched CPU/CUDA resampling + numerical parity (planned)
```

Reusable research components already established are: public demo documentation audit, **independent synthetic** treatment-effect estimation and an external **synthetic** temporal-alignment reproduction. They are scaffolding for this target flow; they are **not** its successful end-to-end clinical execution.

## Evidence pointers

- [Executed evidence and run IDs](../reports/research-evidence.md)
- [Experiment-by-experiment acceptance states](experiment-matrix.md)
- [Engineering architecture and metrics](architecture.md)
- [Public data origin, scope and licensing](data-and-licensing.md)

This distinction is intentional so that researchers and reviewers can verify reproducible progress without confusing a *proposed scientific contribution* with a *completed clinical result*.
