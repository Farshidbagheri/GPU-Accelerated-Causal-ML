# Rights, licenses, and scientific-use boundaries

This repository combines independently developed research code and figures, an independently archived public demonstration dataset, and **references** to other researchers' implementations. These materials do not all share one license.

## 1. Public data: MIMIC-IV-ED Demo v2.2

**Source:** Alistair Johnson, Lucas Bulgarelli, Tom Pollard, Leo Anthony Celi, Steven Horng, and Roger Mark (2023), *MIMIC-IV-ED Demo v2.2*, PhysioNet. https://doi.org/10.13026/jzz5-vs76

**Applicable license:** [Open Data Commons Open Database License v1.0 (ODbL)](data/LICENSE.txt), also [specified on the official dataset record](https://physionet.org/content/mimic-iv-ed-demo/2.2/). ODbL is **not** the MIT software license. The six compressed CSV files in `data/` are unchanged copies of the public demo distribution. The original distribution's `LICENSE.txt` and `SHA256SUMS.txt` are preserved. The CSV files were moved from the source's `ed/` directory to `data/`; their compressed bytes have not been modified.

The license permits reuse and redistribution subject to its conditions. Redistributors must retain license notices and attribution, and share adapted **databases** according to the ODbL when those obligations apply. No permission to disclose the credentialed MIMIC-IV or full MIMIC-IV-ED database is provided by the public demo's license.

The source is [PhysioNet's public 100-person ED Demo](https://physionet.org/content/mimic-iv-ed-demo/2.2/). It is **not** the credential-restricted [full ED database](https://physionet.org/content/mimic-iv-ed/2.2/). Its timestamps support descriptive documentation-time checks only; medication dispensation is not a verified first intravenous antibiotic administration.

**Attribution notice:** Contains information from MIMIC-IV-ED Demo v2.2, made available on PhysioNet under the Open Database License (ODbL) 1.0. Cite the original dataset independently of any software DOI.

## 2. Independently written code, figures and documentation

The repository author has selected the **[MIT License](LICENSE)** for their original source code, corresponding scripts, original diagrams, and accompanying original software documentation, copyright © 2026 Farshid Bagheri Saravi. The MIT grant permits modification, redistribution and commercial use **of that original software**, subject to preservation of the license and copyright notice.

**Scope is important:** the MIT grant does **not** relicense the third-party *MIMIC-IV-ED Demo* database, its license text and source archives under `data/`, nor does it relicense unbundled upstream research code, papers, clinical records or other third-party material. The public demo keeps its **ODbL 1.0** terms. If you redistribute this mixed repository, preserve **both** the MIT notice for its original software and ODbL attribution/license for the public dataset.

The author has indicated the software is their own independent prototype, rather than MetroHealth-provided or university-funded collaborator code. The MIT grant concerns materials the author can lawfully license; it does not itself decide title to any material subject to a separate third-party agreement.

## 3. Third-party research software

T4, G-Transformer, VTDNet, *Off by a Beat*, and other comparator methods are independently authored projects. Their linked repositories retain their own rights. The GitHub Actions workflows check out specified upstream commits during testing; no blanket relicense of those authors' source code is implied, and no third-party source distribution is provided in this repository's release tree.

The **MIMIC Code Repository** maintained by MIT-LCP is also different from **MIMIC clinical data**. A software license applied to MIMIC Code does not change PhysioNet's database license.

## 4. Zenodo release metadata gate

A GitHub–Zenodo release archive may include files under different rights. Zenodo's [license guide](https://help.zenodo.org/docs/deposit/describe-records/licenses/) allows describing mixed-license records, but the author's choice must be reviewed before publication. The software metadata is **MIT** (declared in `CITATION.cff`); Zenodo's general CC BY 4.0 default must **not** be used in place of MIT or as a relicense of the ODbL public demonstration dataset.

Before the first release: confirm ownership/permission for code and figures; verify source dataset files and notices using `python scripts/verify_public_demo.py`; confirm no secrets or restricted patient data are in current files **or prior Git history and workflow logs**; and confirm the final Zenodo record accurately identifies the applicable rights. [Publication procedure](docs/zenodo-publication-guide.md).

This file documents sources and publication checks; it is **not** a substitute for advice from a qualified legal or university research/IP adviser.
