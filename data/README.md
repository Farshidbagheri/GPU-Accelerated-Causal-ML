# MIMIC-IV-ED Demo (public, deidentified)

**Official source:** [MIMIC-IV-ED Demo 2.2, PhysioNet](https://physionet.org/content/mimic-iv-ed-demo/2.2/) · **DOI:** [10.13026/jzz5-vs76](https://doi.org/10.13026/jzz5-vs76) · **Database license:** [ODbL 1.0](LICENSE.txt).

This folder contains **only six original compressed CSV files from the public 100-patient demo**, plus its original `SHA256SUMS.txt` and `LICENSE.txt`. The files were moved from the original `ed/` prefix into the repository's `data/` folder **without changing their content**. It is *not* the credential-restricted full MIMIC-IV/MIMIC-IV-ED database, and it contains no MetroHealth or AmsterdamUMCdb data.

| Official demo table | Role in the data model |
| --- | --- |
| `edstays.csv.gz` | ED visit identifiers, arrival and departure times |
| `triage.csv.gz` | Triage measurements and presentation attributes |
| `vitalsign.csv.gz` | Time-stamped documented clinical vitals |
| `diagnosis.csv.gz` | Encounter-associated diagnostic coding |
| `pyxis.csv.gz` | Medication dispensation events, **not confirmed administrations** |
| `medrecon.csv.gz` | Medication reconciliation history; **not first IV-dose evidence** |

## Reproducibility and privacy

```bash
python scripts/verify_public_demo.py
python scripts/run_pilot.py --data data --out results --offsets 30,60,120
```

The verification script checks all seven original data/license file checksums against the included *unaltered* PhysioNet manifest and rejects unknown filenames. Derived experiment summaries belong under `reports/`, not `data/`. Do not upload identifying information, full credentialed MIMIC data, protected MetroHealth files, access tokens or patient-level extracts from restricted datasets.

**The ED demo is useful for the *data-timing audit*, not a valid standalone test of antibiotic delay effects.** There are 100 deidentified patients and multiple ED encounters, but not the complete controlled cohorts and treatment-administration information required for causal treatment-timing identification.

Attribution: Johnson A, Bulgarelli L, Pollard T, Celi LA, Horng S, Mark R (2023). *MIMIC-IV-ED Demo (version 2.2)*. PhysioNet. https://doi.org/10.13026/jzz5-vs76.
