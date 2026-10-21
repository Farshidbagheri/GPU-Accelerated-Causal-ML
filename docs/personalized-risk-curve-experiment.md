# Individualized simulated treatment-start risk curves

**Scope:** first controlled simulation of the dissertation's *risk from waiting* question—not a clinical estimator and not a reproduction of T4.

The [source](../src/personalized_delay_synthetic.py) generates 3,200 synthetic independent individuals with four sequential opportunities to begin simulated treatment, an option to remain untreated until the fourth time step, and time-varying confounding from evolving simulated severity. The estimator learns from **factual binary outcomes only** and never observes the simulation's potential outcomes during fitting. Counterfactual risk curves under five fixed initiation regimes are integrated by the *known synthetic generator*, used only for out-of-sample scoring. CPU PyTorch neural S-learners use unweighted factual loss and inverse-observational-path propensity weights. True propensities come from the simulator: they cannot be assumed known for clinical observational data.

**Local preliminary results, 3 seeds (41–43):** mean conditional risk-curve RMSE: raw factual group means **0.198942**, unweighted neural learner **0.035608**, IPW neural learner **0.044565**. Thus IPW did **not** outperform unweighted fitting here, a finding requiring further investigation rather than suppression. The model generates different curves by baseline simulated patient features, not validated personalized medical advice.

**Computing:** the standalone [profiling script](../scripts/benchmark_synthetic_cpu_cuda.py) runs matched work on CPU and CUDA *only if CUDA is present*. A CPU-only environment returns `NOT_RUN_NO_CUDA` and **no GPU speedup number**. A local median CPU run was around 0.6 seconds for this small problem; cross-machine timing claims are invalid. The independent [GitHub workflow](../.github/workflows/personalized-curve-benchmark.yml) records the machine and checks reproducibility.

## Limitations

- Inputs are invented physiologic proxies, not real antibiotics or sepsis patients.
- Output is a synthetic event risk, **not** mortality, ICU admission or antibiotic safety.
- No real treatment administration history is in the demo dataset; it cannot validate this learned counterfactual policy.
- Target clinical estimands require authorized encounter-level antibiotic administration, time-zero, confounder and outcome data.
- The simulation uses true treatment probabilities; their estimation, weighting diagnostics, policy positivity and uncertainty still need rigorous benchmarking.
- A realistic clinical policy must consider harm from deferral and clinician rescue. An artificial treatment response does not demonstrate any safe patient-specific delay.
- **A CPU-only proof of concept is not evidence of CUDA acceleration.**

Experimental status: algorithmic feasibility shown on synthetic data; clinical causal question and GPU performance hypothesis remain open.
