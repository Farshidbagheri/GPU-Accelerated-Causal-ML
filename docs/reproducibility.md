# Reproducibility gates and resource policy

**Already demonstrated:** successful GitHub Actions run on 100-patient public MIMIC-IV-ED Demo v2.2, 222 ED stays, 1,038 recorded vital-sign events; 5 unit tests. At hypothetical arrival+30/60/120 min cutoffs, 868/815/693 events were charted after cutoff. This is a *documentation-time audit*; it estimates no treatment effect or GPU speedup.

**Also demonstrated (separate Google Colab run, 21 October 2026):** an executed Tesla T4 benchmark on a **synthetic inference workload** with identical trained weights. For 160,000 synthetic individuals × 5 options, median CPU inference was 237.679 ms and CUDA inference 20.659 ms (11.50×); maximum prediction difference was 1.19×10⁻⁷. The single-session notebook, exact sources, and measurement provenance are archived in [experiments/colab-t4](../experiments/colab-t4/README.md) and [reports/colab-runs](../reports/colab-runs/2026-10-21-t4/README.md).

**Not yet demonstrated:** full paper-level T4/VTDNet reproductions, a GPU-accelerated **end-to-end clinical causal pipeline**, real-patient antibiotic treatment effects, or clinical treatment comparisons.

## Phase gates
- Gate A: versioned input/source provenance and license.
- Gate B: deterministic tests and valid time leakage prevention.
- Gate C: synthetic paper reproduction with original metrics and pinned seeds.
- Gate D: permissioned clinical data, treatment administration timestamps, outcomes, confounders, censoring, overlap and target-trial assumptions.
- Gate E: matched CPU/GPU workload, numeric parity and inferential fidelity. A small synthetic same-weight inference benchmark has passed a scoped Tesla T4 timing/parity check; end-to-end causal model validation and cross-platform acceleration claims remain open.

**Resource discipline:** keep CI limited to quick CPU tests and audit; do not run model training on every commit; use manual workflow dispatch for expensive tests, with short timeout and saved aggregate reports. Do not claim Github Actions offers GPU compute.

**Data safety:** public demo tables have ODbL v1.0 and attribution. Do not upload full credentialed MIMIC-IV, credentialed MIMIC-IV-ED, MetroHealth records, AmsterdamUMCdb or clinical credentials to GitHub even when repository is private.

Source: https://physionet.org/content/mimic-iv-ed-demo/2.2/
Restricted MIMIC: https://physionet.org/content/mimiciv/3.1/
NVIDIA deadline / application format: https://research.nvidia.com/graduate-fellowships
