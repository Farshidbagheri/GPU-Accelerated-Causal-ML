# Individualized simulated treatment-start risk curves

**Scope:** first controlled simulation of the dissertation's *risk from waiting* question—not a clinical estimator and not a reproduction of T4.

The [source](../src/personalized_delay_synthetic.py) generates 3,200 synthetic independent individuals with four sequential opportunities to begin simulated treatment, an option to remain untreated until the fourth time step, and time-varying confounding from evolving simulated severity. The estimator learns from **factual binary outcomes only** and never observes the simulation's potential outcomes during fitting. Counterfactual risk curves under five fixed initiation regimes are integrated by the *known synthetic generator*, used only for out-of-sample scoring. CPU PyTorch neural S-learners use unweighted factual loss and inverse-observational-path propensity weights. True propensities come from the simulator: they cannot be assumed known for clinical observational data.

**Independently verified GitHub Actions results, 3 seeds (41–43), 3,200 simulated people each:** mean conditional risk-curve RMSE: raw factual group means **0.198853**, unweighted neural learner **0.041096**, inverse-path-propensity-weighted neural learner **0.038054**. The weighting method was slightly better on the reported mean here, but results must not be generalized beyond this synthetic simulator. [Verified workflow and raw JSON artifact](https://github.com/Farshidbagheri/GPU-Accelerated-Causal-ML/actions/runs/39556722065). The model generates different curves by baseline simulated patient features, not validated personalized medical advice.

**Computing:** the standalone [profiling script](../scripts/benchmark_synthetic_cpu_cuda.py) runs matched work on CPU and CUDA *only if CUDA is present*. A CPU-only environment returns `NOT_RUN_NO_CUDA` and **no GPU speedup number**. The independent GitHub run measured median CPU end-to-end time **0.76365 s**, while CUDA was **NOT_RUN_NO_CUDA**; cross-machine timing claims are invalid. The independent [GitHub workflow](../.github/workflows/personalized-curve-benchmark.yml) records the machine and checks reproducibility. **A separate, later, user-executed Google Colab Tesla T4 benchmark** archived an [original notebook and exact sources](../experiments/colab-t4/README.md), with 11.50× median CUDA/CPU speedup for same-weight synthetic inference on 160,000 people × five options and 1.19×10⁻⁷ maximum prediction difference. This does **not** retroactively make GitHub Actions a GPU run, and it does not benchmark the full proposed causal analysis pipeline.

## Limitations

- Inputs are invented physiologic proxies, not real antibiotics or sepsis patients.
- Output is a synthetic event risk, **not** mortality, ICU admission or antibiotic safety.
- No real treatment administration history is in the demo dataset; it cannot validate this learned counterfactual policy.
- Target clinical estimands require authorized encounter-level antibiotic administration, time-zero, confounder and outcome data.
- The simulation uses true treatment probabilities; their estimation, weighting diagnostics, policy positivity and uncertainty still need rigorous benchmarking.
- A realistic clinical policy must consider harm from deferral and clinician rescue. An artificial treatment response does not demonstrate any safe patient-specific delay.
- **The CPU-only GitHub run is not evidence of CUDA acceleration.** The distinct Colab T4 benchmark establishes only scoped synthetic inference performance, not real clinical treatment effects or full-pipeline speedup.

Experimental status: algorithmic feasibility shown on synthetic data; one scoped synthetic CUDA inference workload measured on Tesla T4; clinical causal question and GPU performance of the full planned pipeline remain open.
