# Off by a Beat: controlled reproduction of the authors' toy example

**Paper:** Tang, Yao, Wiens & Parbhoo. *Off by a beat: the effects of temporal misalignment in reinforcement learning for sepsis treatment*. npj Digital Medicine 9, 360 (2026). DOI [10.1038/s41746-026-02625-2](https://doi.org/10.1038/s41746-026-02625-2).

**Original authors' code:** https://github.com/shengpu-tang/RL-Off-by-a-Beat — MIT license. **Pinned commit:** \`2f3e58c8a9186f68b22b0ab5b82c6f9366968ac6\`.

The separate [reproduction workflow](../../.github/workflows/reproduce-offbyabeat-toy.yml) checks out the **actual original upstream notebook**, executes its specified, unmodified toy example cells (6, 7, 8, 11, 13, 16 and 17) and saves a JSON report of learned two-state policies under the two alignment schemes and their discounted value under the true simulation dynamics. This avoids copying external code into this repository and preserves the original authors' attribution.

### What counts as success?
- The selected notebook cells run without modification at the pinned source commit.
- The extracted action policies are finite and correctly normalized.
- Their estimated actions and values under the authors' simulator are recorded.

### What this is not
- NOT a reproduction of the article's headline 335/750 state disagreement result.
- NOT a T4 run; NOT a sepsis antibiotic timing model.
- NOT model evaluation on real clinical datasets.
- NOT a GPU benchmark.

The experiment needs only CPU. It uses 100 simulated trajectories of 10 steps and does not train a neural network. The other notebook and the MIMIC-III analysis must be tested separately before any claim about the paper's full results.
