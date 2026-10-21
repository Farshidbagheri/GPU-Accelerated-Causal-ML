# Release and DOI plan — evidence-preserving publication

This repository is research software supporting a **doctoral sepsis antibiotic timing project**, but none of the open benchmark outputs establish a treatment effect in real patients. The published source currently includes the **public PhysioNet MIMIC-IV-ED Demo v2.2** under its own **ODbL 1.0** license, and original software with **no separate permissive license**.

## Release gate: before making public

- Confirm publication of **all Git commit history**, which GitHub exposes when repository visibility becomes public.
- Confirm the executed Colab [notebook](../experiments/colab-t4/NVIDIA_Causal_ML_CPU_CUDA_Benchmark.ipynb) contains only simulated data and runtime outputs; check its exact source files match the recorded SHA-256.
- Verify [source license and public demo](data-and-licensing.md); do not upload credential-restricted MIMIC or MetroHealth data.
- Ensure paper-level replication is never claimed for T4/VTDNet, and that GPU speedups are labeled **single Colab session and synthetic workload**.
- Check project lab/university software ownership, any collaborators' IP claims, and possible patent/paper timing before intentionally granting code reuse rights.

## Software license (owner decision)

**Not required to view a public repo or to publish a DOI.** With no LICENSE for our independently authored Python code, default copyright remains in effect. If the owner wants an open collaboration ecosystem, MIT or BSD-3-Clause is an option **only after confirming rights and accepting broad reuse including commercial usage**. This does not alter the data's ODbL obligations.

No license for third-party paper code is granted by this repository. The publicly accessible **data's** license is provided separately in `data/LICENSE.txt`.

## Stable DOI citation, after public visibility

1. Visit [Zenodo](https://zenodo.org), log in with GitHub, and connect the repository using [Zenodo's GitHub integration](https://help.zenodo.org/docs/github/enable-repository/).
2. Validate `CITATION.cff`: author name, title, institution and link. Avoid adding an imaginary DOI before registration.
3. Create a GitHub **Release** (suggested initial research software tag `v0.1.0` rather than claiming the dissertation is completed).
4. Zenodo archives the tagged release and registers a **version-specific DOI** and a record for the software; verify the DOI on Zenodo and cite it on GitHub and in the paper after it actually exists.
5. Keep versions immutable and publish a **new release/DOI** for scientifically substantial changes. Archive full data only as allowed by dataset license and publication policy.

See [GitHub's DOI instructions](https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content) and [Zenodo's archived-release steps](https://help.zenodo.org/docs/github/archive-software/github-upload/).

**Scope:** a DOI identifies and credits a citable research-software version; it does **not** certify model accuracy, clinical readiness, patent ownership, or exclusive invention rights.

## What a NVIDIA reviewer should see

- A concise [research question and traceability table](research-traceability.md)
- An [executed original Tesla T4 notebook](../experiments/colab-t4/README.md) with exact sources and hardware metrics
- A [synthetic causal curve benchmark](personalized-risk-curve-experiment.md) and a [real but descriptive ED demo audit](../reports/ed-timing-audit.md)
- Transparent boundaries distinguishing work **already measured** from the proposed clinically authorized sepsis causal inference work.
