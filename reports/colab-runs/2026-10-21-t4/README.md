# Measured CPU/CUDA benchmark — Google Colab Tesla T4

**Status:** USER-RUN ARTIFACT VERIFIED • 21 October 2026 • Google Colab • **publicly releasable aggregate synthetic results only**.

The Colab notebook and result ZIP were supplied following the actual execution. The exact source SHA-256 values in the hardware report were compared against source files in the ZIP and **matched**. No patient EHRs, clinical antibiotics or mortality outcomes were used.

## Hardware

- **NVIDIA Tesla T4 GPU**, 14.563 GiB usable VRAM; CUDA 13.0, driver 580.82.07
- Intel Xeon @ 2.00 GHz, 2 vCPU; 12.671 GiB system RAM
- Python 3.13.15 and PyTorch 2.11.0+cu130
- Machine: Google Colab; measured 2026-10-21 07:23:59 UTC

## Actual results

| Workload | Median CPU | Median CUDA | Reported ratio (CPU/GPU) | Numerical parity |
|---|---:|---:|---:|---|
| Full synthetic training and evaluation: 3 seeds; 3,200 simulated patients per seed | 1.59191 s | 1.19903 s | **1.3277×** | Not directly comparable: independently trained weights |
| Identical-weight inference: 3,200 synthetic people × 5 decision scenarios | 0.026820 s | 0.001259 s | **21.3026×** | Max absolute difference 1.19×10⁻⁷ |
| Identical-weight inference: 160,000 synthetic people × 5 decision scenarios | 0.237679 s | 0.020659 s | **11.5049×** | Max absolute difference 1.19×10⁻⁷ |

Inference device-copy and copy-back time are included; model transfer and warmup excluded. Each timing series contains 3 repetitions. The CPU end-to-end first run was 6.87 seconds, much longer than subsequent runs, so the measured training speedup is provisional.

**Scientific boundary:** This is genuine GPU evidence for a **simulated computational workload**, not evidence that CUDA improved causal identification or real antibiotic clinical outcomes. A single Colab T4 session is insufficient to claim platform-independent acceleration.

**Provenance:** The attached original Colab notebook and results archive were inspected before this report was created. The [structured aggregate JSON](colab-t4-2026-10-21.json) preserves per-run timing, environment and SHA-256 source fingerprints. The notebook is **not identical** to the earlier GitHub implementation; this benchmark reflects the separately supplied executed Colab code. For exact repeatability, archive that notebook/source alongside the report.
