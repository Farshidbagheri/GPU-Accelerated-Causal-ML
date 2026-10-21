# Longitudinal causal-method evaluation

This directory is a **method registry with reproducibility states**. It is not a collection of copied third-party models. Each model's source remains with its authors; where an experiment is executed, its GitHub Actions job checks out the author's code at a fixed commit and records output provenance. Third-party source and clinical datasets are not mixed with our independent implementation.

| Method | Why included | Verified here | Not yet verified |
| --- | --- | --- | --- |
| [T4](t4/README.md) | Antibiotic timing comparator most directly relevant to the dissertation | Static source and dataset compatibility review | Full reproduction/training blocked by preprocessing interface |
| [Off by a Beat](off_by_a_beat/README.md) | Timestamp misalignment in sequential sepsis treatment modeling | **Original authors' 100-run synthetic toy reproduced**; value metrics matched | Sepsis clinical-policy experiment, antibiotic-specific inference |
| [VTDNet](vtdnet/README.md) | Time-varying deconfounding representation | Reduced forward/backward CPU compatibility check | Full clinical training and paper PEHE not reproduced |
| [G-Transformer](g_transformer/README.md) | Counterfactual trajectories under sequential treatment | Literature and code provenance reviewed | Original benchmark and code authorship confirmation |
| [Precision Medication](precision_medication/README.md) | Future joint-medication temporal causal modeling | Literature and upstream link documented | Training and medication-policy benchmark |
| [Our nonlinear S-learner](temporal_neural_baseline/README.md) | Fully runnable, transparent known-truth baseline | **Three synthetic seeds** with patient-level train/test split and PEHE comparison | Multi-step clinical treatment policy and GPU validation |

**Engineering rule:** a published model can be *listed*, *run*, *reproduced*, or *externally validated*; these are distinct states. See [evidence summary](../reports/research-evidence.md) and [experiment matrix](../docs/experiment-matrix.md). Original source should be fetched with a pinned commit and used according to its license rather than silently presented as work authored here.

The public ED demo alone does not permit a fair head-to-head clinical test of T4, G-Transformer, VTDNet and the other methodologies. Their outcomes, counterfactual targets, simulated truth, and data access requirements differ.
