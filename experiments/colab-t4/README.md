# Executed Google Colab benchmark — Tesla T4, 21 October 2026

This folder preserves the **original executed notebook (with its recorded outputs)** and the **exact Python sources written by its two `%%writefile` cells** during the user-run Colab session. Files have been reviewed for high-risk credentials and restricted EHR data; the experiment used **synthetic subjects only**.

| Artifact | Description |
| --- | --- |
| [Executed notebook](NVIDIA_Causal_ML_CPU_CUDA_Benchmark.ipynb) | Full Colab cell inputs, execution outputs and charts, including recorded hardware |
| [Synthetic model used in Colab](antibiotic_timing_synthetic.py) | Actual source; SHA-256 83b0c9ff08c4f18cc3e40e05dd19ed9ce9ef10d283eca5bc359e4a71ba1b5a51 |
| [CPU/CUDA benchmark source](benchmark_cpu_cuda.py) | Actual source; SHA-256 e78cf8e69a384273adab45af18b49df8a1b3c3970ec1f916afd44780c2b1f173 |
| [Aggregate verified results](../../reports/colab-runs/2026-10-21-t4/README.md) | Summarized metrics, device details and limitations |

**Reproduce:** upload notebook to [Google Colab](https://colab.research.google.com/), choose a CUDA GPU (the original run used Tesla T4), and select Runtime → Run all. Hardware allocation and numerical timings may differ between sessions.

**Measured here:** median synthetic inference: 11.50× faster for 160,000 individuals × 5 options; numerical maximum deviation 1.19×10⁻⁷. Median end-to-end training speed ratio: 1.33× on a single Colab T4 session; includes warmup variability and independently trained weights.

**Does not demonstrate:** real clinical antibiotic administration effects, GPU-accelerated T4 reproduction or stable multi-platform throughput.

The original ZIP submitted by the experimenter is not required for the public audit because the executed notebook embeds plots and the machine-readable aggregate results are included separately. The ZIP remains available to the owner for archival provenance.

**Code rights:** No standalone open-source license has yet been granted for the original code. The public PhysioNet Demo license applies separately to the `data/` tables.
