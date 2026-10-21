# External-method registry (no third-party source vendored)

This directory records **reproduction plans**, not claims of completed replications. Every model is evaluated separately, with the upstream implementation's license, commit, environment, expected data and appropriate metrics documented before any training.

| Method | Relevance | Stage |
| --- | --- | --- |
| [T4](t4/README.md) | Antibiotic timing: closest scientific comparator | Environment/license review |
| [Off by a Beat](off_by_a_beat/README.md) | Temporal misalignment sensitivity in sepsis RL | Synthetic experiment candidate |
| [VTDNet](vtdnet/README.md) | Time-varying confounding | Separate synthetic benchmark candidate |
| [G-Transformer](g_transformer/README.md) | Dynamic treatment counterfactual modeling | Code provenance review |
| [Precision Medication](precision_medication/README.md) | Future treatment-policy extension | Literature review only |

**Never** claim results from another project's paper as our results. Original MIMIC-III, MIMIC-IV, AmsterdamUMCdb or MetroHealth data must not be redistributed through this repository unless the *specific* source terms permit that exact release. Published authors' code and datasets may have different permissions.

### Experiment progression
1. Verify upstream repo identity, LICENSE, commit SHA and environment requirements.
2. Reproduce authors' synthetic experiment, using the same data-generating process and metrics.
3. Only with appropriate clinical inputs/permissions, construct a comparable real-data target-trial design.
4. Profile CPU/GPU performance on the same workload and estimation-quality checks.
5. Store reproducible aggregate results and full provenance.

Default GitHub Actions runs **CPU-based tests**, not GPU model training. Treat MIMIC-IV-ED Demo audit as distinct from a sepsis causal model.
