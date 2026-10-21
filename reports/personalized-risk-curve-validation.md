# Synthetic timing-curve benchmark — verified run

**GitHub Actions:** https://github.com/Farshidbagheri/GPU-Accelerated-Causal-ML/actions/runs/39556722065

* Source: `src/personalized_delay_synthetic.py`
* Evaluated: 3 randomized seeds (41, 42, 43); 3,200 simulated subjects per seed, with disjoint train/validation/test indices
* Intervention times: initiation at t=0, 1, 2, 3 or no simulated treatment through t=3
* Estimators trained on factual outcomes only; the simulator's true counterfactual risk was hidden until scoring
* All three unit tests passed on hosted CPU

| Method | Mean risk-curve RMSE, three seeds ↓ | Mean risk-from-waiting RMSE ↓ |
| --- | ---: | ---: |
| Unadjusted factual group risk | 0.198853 | 0.120867 |
| Unweighted PyTorch learner | 0.041096 | 0.051880 |
| Inverse-path-propensity-weighted PyTorch learner | **0.038054** | **0.041121** |

Known oracle risk, first seed, for t=0..none: 0.103508, 0.134285, 0.176009, 0.233797, 0.314982.
Estimated IPW neural risk, first seed: 0.096414, 0.141463, 0.164137, 0.223987, 0.295103.

The weighted learner reduced average curve error relative to a naive observational group-mean estimator on this **synthetic** data-generating process. Neither method has been validated on real antibiotic administration histories. The simulator supplies propensity probabilities, which are **unknown in clinical EHR data**.

## Compute check

In the same GitHub run, the median **CPU end-to-end** experiment time was **0.76365 seconds**. CUDA state: `NOT_RUN_NO_CUDA`. **There is no measured CPU-to-GPU speedup.** Even a future benchmark requires identical hardware/software, model settings, explicit GPU synchronization, and end-to-end fidelity checks.

These findings do not establish clinical effectiveness, mortality changes or a safe antibiotic-delay policy. A clinical target trial remains future work.
