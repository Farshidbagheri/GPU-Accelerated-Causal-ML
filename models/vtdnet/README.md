# VTDNet (Dai et al., 2025): readiness assessment

**Paper:** Dai et al., *Journal of Biomedical Informatics* 169:104880 (2025). DOI [10.1016/j.jbi.2025.104880](https://doi.org/10.1016/j.jbi.2025.104880). **Original code:** https://github.com/Throwfox/VTDNet, SHA \`3770f32e0479dab16a97fc11849dfaa1fc717153\`. Upstream README describes MIT licensing but *there is no LICENSE file in the inspected tree*, so we do not vendor their source; their code is checked out afresh for runtime inspection.

## Static issues found in published implementation
1. Data generator writes \`outcomes\`, loader's splitting function expects \`factual_outcomes\`. The generated dictionary does not contain \`factual_outcomes\`.
2. Loader \`CustomDataset_syn.__getitem__\` returns \`cf1\` for \`cf2\` and \`cf3\`.
3. The custom dataset returns **eight** items but the original trainer unpacks **five**.
4. Trainer definition accepts \`test_loader\`, yet \`VTD_training.py\` invokes it without that positional argument.
5. Evaluation imports \`utils.data_loader\` but the repository contains \`utils/data_load.py\`.
6. Model/trainer/evaluation require \`.cuda()\` even for testing on CPU.
7. Simulation's counterfactual generator uses an unusual \`np.where(treatments_history[t] == i, ...)\` condition, not an unambiguous intervention on the i-th treatment.
8. Cross-sample attention: \`query @ key.transpose(-2,-1)\` operates on a [sequence,batch,batch] matrix, coupling patient outputs to other batch members. May be intended, but must be scrutinized for individualized-effect inference.
9. The released notebook uses Google Drive mounting and different training signature/parameters than the command-line script.

**Conclusion:** Full paper PEHE/eATE reproduction **blocked**, not simply a matter of installing PyTorch. Exact numerical comparisons to the published article would be misleading until synthetic target generation, training and scoring all agree. Keep independent reference benchmark separately labelled.

## Executable check
The [architecture compatibility workflow](../../.github/workflows/vtdnet-architecture.yml) checks out pinned author code without including it in this repo; substitutes dynamic CPU device placement for hard-coded CUDA just for a forward/loss/backward smoke test on random shaped tensors. No trained treatment-effect estimator or authors' PEHE results are claimed.

This is an assessment of a **published 2025** method, not proof that the method or scientific conclusions are invalid.
