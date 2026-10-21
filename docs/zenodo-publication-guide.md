# Zenodo DOI publication and research-software release checklist

**Status: RELEASED.** Public GitHub release [`v0.1.0`](https://github.com/Farshidbagheri/GPU-Accelerated-Causal-ML/releases/tag/v0.1.0), published **2026-10-21**; DOI for this version: **[10.5281/zenodo.23530462](https://doi.org/10.5281/zenodo.23530462)**; all-versions concept DOI / README badge target: **[10.5281/zenodo.23530461](https://doi.org/10.5281/zenodo.23530461)**. The badge is now installed in README, and GitHub `CITATION.cff` points to the version-specific DOI.

## Scientific object and attribution
- Resource type: **Software**
- Title: GPU-Accelerated Causal Machine Learning: Reproducible Benchmarks for Decision-Time Reliability and Synthetic Antibiotic-Timing Research
- Creator: **Farshid Bagheri Saravi**
- Affiliation: **Case Western Reserve University**
- Keywords: causal machine learning; sepsis; clinical treatment timing; longitudinal EHR; CUDA; GPU benchmarking; synthetic potential outcomes; reproducibility
- Full description: This is a research-software repository for a Ph.D. investigation of clinically credible antibiotic timing in sepsis. It contains a publicly licensed, deidentified MIMIC-IV-ED Demo timestamp audit; independent synthetic causal and individualized delay-risk experiments; a reproduced authors' temporal-alignment toy experiment; and source code and original notebook for a *single-session, synthetic* Tesla T4 CPU/CUDA benchmark. Observed 160,000 synthetic people × 5 scenarios: 237.679 ms CPU and 20.659 ms CUDA (11.50×) under identical inference weights, with max numerical deviation 1.19e-7. It does **not** establish any clinical antibiotic-treatment effect, safe delay, a fully reproduced T4 or VTDNet paper, or GPU acceleration of the full causal research pipeline.
- Primary source repository: https://github.com/Farshidbagheri/GPU-Accelerated-Causal-ML
- Related **source dataset**, independently citable: MIMIC-IV-ED Demo v2.2, Johnson et al., PhysioNet DOI: 10.13026/jzz5-vs76
- If/when the author has an ORCID, add it to CITATION.cff or Zenodo; **do not invent** an identifier.

## Legal and publication gate
- The repository is **already public**; its full Git commit history is publicly visible.
- **Verified against the official PhysioNet dataset page and ODbL 1.0:** `data/` contains the freely distributed **MIMIC-IV-ED Demo v2.2** (100 public demo patients), not the credential-restricted full MIMIC-IV-ED dataset. Redistribution of the unchanged demo is permitted with ODbL notices and attribution. The six CSV archives, original LICENSE.txt, and SHA256SUMS.txt may remain bundled when those terms are preserved. It is **not MIT-licensed clinical data**. Official sources: https://physionet.org/content/mimic-iv-ed-demo/2.2/ and https://opendatacommons.org/licenses/odbl/1-0/ . For the file-by-file rights map, see [RIGHTS_AND_LICENSES.md](../RIGHTS_AND_LICENSES.md).
- The author has approved the **[MIT software license](../LICENSE)** for their original code, related original software diagrams and documentation. This does not override the **ODbL 1.0** applied to public MIMIC-IV-ED Demo data in `data/`.
- The Zenodo **software-record license should be MIT**, explicitly present as `license: MIT` in `CITATION.cff`. Zenodo's CC BY 4.0 default must not be accepted for this software. The bundled public demo separately retains **ODbL 1.0** with its source license and attribution, as detailed in [RIGHTS_AND_LICENSES.md](../RIGHTS_AND_LICENSES.md). Verify the imported record's license metadata and description reflect this distinction.
- **Specific university-policy gate:** CWRU's Intellectual Property Policy, sections 1 and 4, includes some software produced with university support, employees or equipment and addresses students as well as staff and faculty. Ownership of this exact prototype cannot be determined solely by reading the code. If university resources, employment obligations or clinical-collaboration contracts contributed to the work, confirm release permission before making its history public. Official: https://case.edu/research/sites/default/files/2024-03/Intellectual-Property-Policy.pdf .
- **Automated Zenodo metadata:** `CITATION.cff` includes `license: MIT` and version DOI `10.5281/zenodo.23530462`. The README and rights map make the bundled public Demo's **ODbL 1.0** explicit. The DOI values come from the author's Zenodo badge/DOI screen; Zenodo's detailed record license fields have not been independently read through this integration. Review those fields in the account UI and correct metadata there if it omits or contradicts the data's independent ODbL license.
- Public release and a Zenodo DOI are **permanent disclosures** relevant to patentability and institutional/collaborator ownership. Coordinate any confidential invention plans before clicking Publish.
- There is no need to claim a novel patented algorithm to make software citable. This code is an early computational feasibility study.

## GitHub → Zenodo path (completed for v0.1.0)
1. **Already completed:** repository set to **Public**, with original software MIT license and public Demo ODbL notices. Check the latest README in a logged-out browser if desired.
2. Sign in at https://zenodo.org with the user's **own** account. Under **Linked accounts**, connect GitHub if not connected.
3. Profile → **GitHub** → **Sync now**; find `Farshidbagheri/GPU-Accelerated-Causal-ML` and enable it. Official: https://help.zenodo.org/docs/github/enable-repository/
4. **Ready:** `CITATION.cff` declares `version: 0.1.0` and `license: MIT`; the bundled public demo separately declares ODbL in `data/LICENSE.txt`. No `.zenodo.json` is used (adding one would supersede CITATION.cff). Confirm Zenodo has imported MIT as the **software** license without implying a change to the database rights.
5. **Completed:** the Zenodo toggle was enabled and GitHub Release `v0.1.0` was published on `main`. Zenodo generated version DOI `10.5281/zenodo.23530462`. For a future version, publish a **new** GitHub Release/tag; enabling the toggle alone does not issue another DOI.
6. **DOI confirmed from the author's Zenodo badge screen:** version DOI `10.5281/zenodo.23530462`; concept DOI `10.5281/zenodo.23530461`. Separately, check the Zenodo record's creator, license and related-data rights fields in the browser. Do **not** publish a duplicate manual upload.
7. **Completed on GitHub `main`:** DOI badge at the top of README links to the **concept DOI**; the `CITATION.cff` DOI identifies the specific archived **v0.1.0 release**. These post-release metadata edits do **not** retroactively modify the frozen `v0.1.0` Zenodo snapshot. Cite the version DOI for reproducibility.

### Published first release
**Tag:** `v0.1.0`  
**Title:** Initial Research Prototype - GPU-Accelerated Causal ML

Description:
- Auditable public MIMIC-IV-ED Demo data-timing integrity checks (not clinical effects)
- 2026 published synthetic temporal-alignment experiment reproduced from authors' source
- Patient-disjoint synthetic PyTorch treatment-effect experiments and timing-response curves
- Executed Colab Tesla T4 notebook and identical-weight CUDA/CPU synthetic inference benchmark
- Exact code, documented numerical settings, provenance and limitations
- Early research software; **not** validated for clinical decision making

### References
- https://help.zenodo.org/docs/github/enable-repository/
- https://help.zenodo.org/docs/github/archive-software/github-upload/
- https://help.zenodo.org/docs/github/describe-software/citation-file/
- https://help.zenodo.org/docs/deposit/describe-records/licenses/
- https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content

**Important:** This repository has one verified GitHub Release `v0.1.0` and the author's supplied Zenodo DOI pair. These identifiers are **software** DOIs; the independently sourced **MIMIC-IV-ED Demo** dataset must still be cited under its own DOI `10.13026/jzz5-vs76`.
