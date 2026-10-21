# Reproducibility gates and resource policy

**Already demonstrated:** successful GitHub Actions run on 100-patient public MIMIC-IV-ED Demo v2.2, 222 ED stays, 1,038 recorded vital-sign events; 5 unit tests. At hypothetical arrival+30/60/120 min cutoffs, 868/815/693 events were charted after cutoff. This is a *documentation-time audit*; it estimates no treatment effect or GPU speedup.

**Not yet demonstrated:** external model reproductions, GPU experiments, clinical treatment comparisons.

## Phase gates
- Gate A: versioned input/source provenance and license.
- Gate B: deterministic tests and valid time leakage prevention.
- Gate C: synthetic paper reproduction with original metrics and pinned seeds.
- Gate D: permissioned clinical data, treatment administration timestamps, outcomes, confounders, censoring, overlap and target-trial assumptions.
- Gate E: matched CPU/GPU workload plus inferential fidelity before acceleration claims.

**Resource discipline:** keep CI limited to quick CPU tests and audit; do not run model training on every commit; use manual workflow dispatch for expensive tests, with short timeout and saved aggregate reports. Do not claim Github Actions offers GPU compute.

**Data safety:** public demo tables have ODbL v1.0 and attribution. Do not upload full credentialed MIMIC-IV, credentialed MIMIC-IV-ED, MetroHealth records, AmsterdamUMCdb or clinical credentials to GitHub even when repository is private.

Source: https://physionet.org/content/mimic-iv-ed-demo/2.2/
Restricted MIMIC: https://physionet.org/content/mimiciv/3.1/
NVIDIA deadline / application format: https://research.nvidia.com/graduate-fellowships
