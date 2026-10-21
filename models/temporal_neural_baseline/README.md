# Independent longitudinal causal benchmark

**Aim:** train a genuine neural treatment-response model and evaluate current-step potential-outcome estimation against two transparent baselines on controlled **synthetic trajectories with known treatment effects**.

- 1,200 synthetic patients, 6 sequential treatment decisions each, 3 seeds.
- Time-varying covariate L_t depends on previous A_(t-1) and history; the treatment propensity depends on current L_t and baseline X. This creates observed time-varying confounding.
- Current outcome depends on L_t, observed history, treatment A_t, and a nonlinear effect tau(X,L_t,A_(t-1)). The simulator exposes tau only for scoring, never training.
- All learners train using **factual outcomes only** and split by patients (70% train, 15% validation, 15% held-out testing). No patient overlap.
- Baseline 1: naive average observed outcome difference; baseline 2: covariate-adjusted Ridge constant-effect S-learner; model: nonlinear PyTorch S-learner with train-time outcome loss and val-based checkpoint.
- Metrics: PEHE-RMSE against synthetic ground truth, absolute ATE error; auxiliary held-out AIPW estimate with patient-clustered approximate standard error (nuisance models trained on a disjoint training set).

**Limitations:** These are **not** T4, VTDNet or G-Transformer replications. They do not establish performance for real clinical data, dynamic antibiotic timing, multi-step regimes, or causal identification under hidden confounding. CPU numbers are not evidence of GPU acceleration.

### Reproduce
\`\`\`bash
pip install numpy scikit-learn torch pytest
python -m pytest -q tests/test_causal_benchmark.py
python src/longitudinal_synthetic_benchmark.py --seeds 40,41,42 --patients 1200 --epochs 45
\`\`\`

The [GitHub Actions benchmark](../../.github/workflows/causal-benchmark.yml) runs only when its files change or manually. Use an actual CUDA runner for future CPU/GPU speed comparisons (same data, seeds, batch size and model settings).
