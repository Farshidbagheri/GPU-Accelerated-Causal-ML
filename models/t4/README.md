# T4 — reproduction readiness assessment

**Article:** Liu et al., *Nature Machine Intelligence* 5, 421–431 (2023), [DOI](https://doi.org/10.1038/s42256-023-00638-0).  
**Author code:** https://github.com/ruoqi-liu/T4 (MIT license).  
**Status:** **NOT REPRODUCED.** The code is publicly available but the repository does not provide a fully ready-to-run, synthetic-end-to-end training pipeline.

## Confirmed obstacles in author's repository

1. The README's `simulation/gen_synthetic.py` writes `data/synthetic_full.pkl` with keys `x`, `x_static`, `y`, `a` per patient.
2. `model/dataset.py` instead loads `data/mimic3.pkl` and `header.pkl` and expects keys such as `treatment`, `outcome`, `death` and named clinical covariates.
3. `run.sh` calls `pre_train.py` and `main.py` without changing to the `model/` folder where those scripts actually reside.
4. README pins an obsolete Ubuntu 16.04 / Python 3.6 / PyTorch 1.4 environment; a current environment would need compatibility testing.
5. Raw clinical MIMIC-III or AmsterdamUMCdb files cannot be used as the missing intermediate preprocessing output automatically. Credential and data-use conditions apply.

**Implication:** Successfully generating a synthetic pickle is not reproducing T4 training, ITE estimates or the paper's reported numbers. Before benchmarking, one must implement and verify a documented adapter/preprocessing pipeline (with authors' consent or as explicitly labeled local adaptation), establish proper treatment/outcome labels and run correct controls. The current 100-patient MIMIC-IV-ED Demo does not supply what the original model expects.

The experimental success under `models/off_by_a_beat` is **another paper**, not evidence that T4 has been reproduced.
