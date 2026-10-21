# Publication-readiness assessment — 21 October 2026

**Repository:** `Farshidbagheri/GPU-Accelerated-Causal-ML` (private during this review)

## Decision

**Conditionally ready for the owner to make public**, after they personally review the repository, accept the public release of its complete Git history, and decide whether to license the independently authored code. This report does **not** change repository visibility.

## Evidence examined

1. Tracked HEAD tree: the only `data/` files are six gzip tables of **MIMIC-IV-ED Demo v2.2**, its `LICENSE.txt` and `SHA256SUMS.txt`. No full MIMIC, MetroHealth, AmsterdamUMCdb, or personal files were listed.
2. Public original distribution: PhysioNet confirms the Demo is **open to anyone under ODbL 1.0**; the full MIMIC-IV and MIMIC-IV-ED datasets are **credential restricted**.
3. Source integrity: [GitHub checksum workflow](https://github.com/Farshidbagheri/GPU-Accelerated-Causal-ML/actions/runs/39542809361) passed, verifying all 7 distributed license/data files against the stored distribution's `SHA256SUMS.txt`. **Independent fetch of official manifest hash not obtained**; this test validates the checked-in manifest.
4. Repository content: surveyed all 50+ current file/tree entries and early Git tree states containing only uploaded demo data, demo code, README and temporary placeholder files. No restricted dataset filename detected. Sample historical README also scanned.
5. Pattern screening: 24 current **text** files checked for common GitHub/API tokens, embedded private-key headers, and credential assignments, with no matching high-risk patterns; compressed CSV content and every Git commit blob were **not** exhaustively screened for private health data.
6. GitHub Actions: successful [ED data audit](https://github.com/Farshidbagheri/GPU-Accelerated-Causal-ML/actions/runs/39542809955) and successful [license data hash check](https://github.com/Farshidbagheri/GPU-Accelerated-Causal-ML/actions/runs/39542809361), plus separately verified [synthetic PyTorch model](https://github.com/Farshidbagheri/GPU-Accelerated-Causal-ML/actions/runs/39531676558).
7. Third-party source: external methods are referenced, not redistributed as source; original authors' notebooks are pulled on demand at pinned revisions during CI.

## Public-visibility risks

- **Entire Git history becomes public**, not just the current branch files. GitHub authorship/commit metadata becomes accessible; original upload/placeholder commits are retained. No sensitive file is currently apparent, but a regex screen is **not** a forensic or formal privacy certification.
- **Dataset license and code rights are different.** The public Demo's ODbL attribution/share-alike requirements apply to its database; Python code has no new license in this repo. Owner should choose whether to explicitly release the Python implementation under a separate OSS license.
- **Fellowship reviewers:** a private repository is *not accessible to an arbitrary NVIDIA reviewer*. Make it public only after approving the points above; then open it in a logged-out browser to confirm the exact proposal link resolves.
- Future **restricted MIMIC or MetroHealth** extracts and derivatives should remain in authorized environments, not committed—even to private GitHub—without permission.
- The title says GPU-Accelerated as a **future objective**. The results shown are CPU-only and not evidence of measured GPU speedup.

## Improvements made during this review

- Added automatic checksum and allowed-file-name gate for the original data distribution.
- Published a clear ODbL attribution and data-security policy.
- Published a scope table separating actual results from unreproduced methods.
- Reorganized the README to foreground evidence, controls, reproducibility and project limits.

## What remains before public toggle?

**One explicit owner decision:** make the repository public despite the disclosure of existing Commit history. Public visibility is not necessary for the code to run; it is necessary if an anonymous NVIDIA reviewer is expected to open the GitHub evidence link in the proposal.

After that decision, GitHub Settings → General → Danger Zone → Change repository visibility → Public; verify the target URL in a signed-out browser. Alternatively, the owner can authorize an in-chat connector action if one is available; none was used to alter visibility here.
