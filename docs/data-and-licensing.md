# Public-data provenance and rights

## Included data

This repository currently carries **only** the openly released **MIMIC-IV-ED Demo v2.2**, 100 deidentified patients (multiple ED visits per patient). Its six compressed tables and the original distribution's `LICENSE.txt` and `SHA256SUMS.txt` are in [`data/`](../data/).

- **Official dataset / citation:** Johnson A, Bulgarelli L, Pollard T, Celi LA, Horng S, Mark R (2023). *MIMIC-IV-ED Demo v2.2*. PhysioNet. DOI: [10.13026/jzz5-vs76](https://doi.org/10.13026/jzz5-vs76).
- **Download source:** https://physionet.org/content/mimic-iv-ed-demo/2.2/
- **Data license:** [Open Data Commons Open Database License 1.0 (ODbL)](../data/LICENSE.txt). Re-users must follow its attribution and share-alike obligations where applicable.
- `SHA256SUMS.txt` originally lists paths under `ed/`; in this repository the `ed/` CSVs are flattened under `data/`. [The release verification script](../scripts/verify_public_demo.py) adjusts paths **without editing the source hashes**.
- A scheduled/manual GitHub Action validates the 7 original distribution files against their unaltered manifest and disallows additional tracked files in `data/`.

**Distribution integrity:** The checked-in `SHA256SUMS.txt` was compared against the [official PhysioNet manifest](https://physionet.org/files/mimic-iv-ed-demo/2.2/SHA256SUMS.txt) on October 21, 2026; all seven listed checksums agree. The GitHub integrity workflow also verifies those hashes against the bundled data and license files.

**Important distinction:** unrestricted public **Demo** is not the full MIMIC-IV or MIMIC-IV-ED database. The full databases require PhysioNet credentialed access and a DUA. Never commit full database extracts, even to a private GitHub repository, without independent written authorization. Never add MetroHealth, AmsterdamUMCdb, identifiable records or clinical credentials.

The code's experimental findings do **not** report patient-level treatment effects. All published reports in this repository are aggregate descriptive counts or **simulated** counterfactual outcomes.

## Publishing controls

1. Keep official public demo tables **only after** automated hashes pass.
2. Do not add patient-level derived data outside the published Demo.
3. Public GitHub visibility will expose the *Git commit history*, not only current files. Anyone making earlier mistakes must assess past commits before publishing; deleting sensitive files in a new commit would not remove their history.
4. **Original code and accompanying original software documents use [MIT](../LICENSE)**, as approved by their author; the **bundled source database retains [ODbL 1.0](../data/LICENSE.txt)**. The MIT grant is not an override of the original database's licensing terms. Details: [RIGHTS_AND_LICENSES.md](../RIGHTS_AND_LICENSES.md).
5. Models from others are linked to their original repositories; the author notebook is checked out at a pinned SHA during GitHub Actions. No third-party source is bundled here.
6. Results are explicitly limited to synthetic toy policies, synthetic one-step and individualized timing-response estimators, descriptive EHR documentation timing, and a **single-session Tesla T4 CUDA/CPU inference benchmark on synthetic inputs**. The latter measured an 11.50× CUDA inference speedup for 160,000 simulated people × five options, **not** full causal-pipeline throughput or clinical antibiotic efficacy. See the [measured Colab provenance](../reports/colab-runs/2026-10-21-t4/README.md).

**Privacy review performed:** tracked file listing and accessible history filenames checked; selected repository text was scanned for high-risk credential patterns. This does **not** substitute for GitHub's secret scanning or a full binary forensic audit. Publish only after the account owner approves making code and history public.
