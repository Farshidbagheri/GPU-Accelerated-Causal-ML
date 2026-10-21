# System design and validation

## The research question

At an eligible ED decision landmark, under a specified follow-up horizon, what causal contrast can be estimated between *starting antibiotic therapy within a defined grace period* and a *clinically constrained deferred strategy*? The treatment event must be **administration**, not an order or Pyxis dispense record. Target-trial assumptions and clinical domain input are prerequisites; this repository has **not** estimated this effect from patient data.

## Three interfaces

**Data interface:** structured encounters → timestamp ledger (event/chart/result/administration) → decision-time admissible history. Output: documented feature eligibility and a provenance record.

**Inference interface:** treatment-regime specification → g-method/DR comparators and time-aware candidates → cohort/overlap checks → estimates or explicit infeasibility. Output: effect/interval (if identifiable), scenario-stability and uncertainty.

**Systems interface:** fixed inputs, seeds and estimands → replicated workloads (landmark × timestamp scenario × fold × bootstrap) → matched CPU/CUDA benchmarking. Output: validated scenarios/hour, wall-clock time, peak memory and numerical agreement.

See the [overview architecture diagram](../figures/research-system-architecture.svg).

## Architecture-to-evidence traceability

| Component | Current implementation | Gate required before claiming success |
| --- | --- | --- |
| ED event ledger | **Implemented** on publicly released demo tables; charting audit | More complete availability semantics and encounter-window checks |
| Time-alignment sensitivity | **Reproduced** a published 2026 synthetic toy; separate clinical policy remains untested | Assess validity for antibiotic estimand and real timestamps |
| Counterfactual estimator | **Implemented** independent synthetic PyTorch baseline, 3 seeds | External baselines on same synthetic process; uncertainty over more seeds; clinical identification |
| Reliable reporting | **Partially implemented** through provenance and limited synthetic metrics | Prespecified rule for overlapping scenarios, identification and uncertainty |
| CUDA acceleration | **Scoped measurement completed** in user-executed Tesla T4 Colab: same trained weights, synthetic inference on 160,000 people × 5 options, 11.50× median CUDA/CPU ratio and 1.19×10⁻⁷ max numerical difference. [Provenance](../reports/colab-runs/2026-10-21-t4/README.md) | Full longitudinal causal resampling/cross-fitting pipeline, multi-session confidence intervals, reproducible memory profiling, and clinical inferential fidelity |

### Engineering metrics

- **Clinical/causal:** clearly defined eligibility, treatment regimes, follow-up, bias/positivity gates, support for each scenario.
- **Statistical:** synthetic PEHE-RMSE and ATE error; coverage and calibration where identifiable.
- **Compute:** end-to-end wall time, memory, validated scenarios/hour, CPU/CUDA numerical parity.
- **Reproducibility:** pinned upstream commits and package environments, random seeds, patient-disjoint split, immutable workflow logs.

GPU improvement for the **full planned causal pipeline** remains a falsifiable hypothesis. The measured small synthetic inference speedup does not establish better causal identification or a clinical benefit.
