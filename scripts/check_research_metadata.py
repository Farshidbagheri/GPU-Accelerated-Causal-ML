#!/usr/bin/env python3
"""Fast, offline consistency gates for this research-software repository.

This checker tests referential integrity and the recorded scope of evidence.
It does not establish causal identification, clinical validity, IP ownership,
security of the full Git history, or public-release authorization.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "research-evidence.json"
COLAB = ROOT / "reports" / "colab-runs" / "2026-10-21-t4" / "colab-t4-2026-10-21.json"

def check_markdown_links() -> tuple[int, int]:
    errors = []
    checked = 0
    files = 0
    for md in sorted(ROOT.rglob("*.md")):
        if ".git" in md.parts or ".venv" in md.parts:
            continue
        files += 1
        for n, line in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
            for match in re.finditer(r"\]\(([^)]+)\)", line):
                raw = match.group(1).strip().split(" \"", 1)[0]
                if re.match(r"^(?:https?://|mailto:|ftp://|data:|#)", raw, re.I):
                    continue
                relative = unquote(raw.split("#", 1)[0].split("?", 1)[0])
                if not relative:
                    continue
                checked += 1
                resolved = (md.parent / relative).resolve()
                if not resolved.is_relative_to(ROOT) or not resolved.exists():
                    errors.append(f"{md.relative_to(ROOT)}:{n}: missing local link {raw}")
    if errors:
        raise AssertionError("Broken relative Markdown links:\n" + "\n".join(errors))
    return files, checked

def check_evidence() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    colab = json.loads(COLAB.read_text(encoding="utf-8"))
    assert report["clinical_effect_estimated"] is False
    assert report["nvidia_gpu_benchmark_performed"] is True
    tasks = {task["id"]: task for task in report["tasks"]}
    assert {"ed_demo", "off_by_a_beat", "independent_causal_benchmark",
            "vtdnet", "t4", "synthetic_personalized_risk_curves",
            "colab_tesla_t4_synthetic_inference"} <= set(tasks)
    t4 = tasks["colab_tesla_t4_synthetic_inference"]
    assert t4["weights_identical_for_inference"] is True
    assert t4["reported_repetitions"] == 3
    assert colab["environment"]["gpu"] == "Tesla T4"
    full = next(x for x in colab["inference"] if x["n_people"] == 160000)
    assert t4["n_synthetic_people"] == full["n_people"]
    assert t4["n_timing_alternatives"] == full["n_timing_regimes"]
    for attr, reference in (
        ("cpu_median_ms", full["cpu_median_seconds"] * 1000),
        ("cuda_median_ms", full["cuda_median_seconds"] * 1000),
        ("reported_speedup", full["reported_speedup"]),
        ("max_output_difference", full["maximum_prediction_difference"]),
    ):
        assert abs(t4[attr] - reference) < 1e-5, attr
    assert abs(t4["cpu_median_ms"] / t4["cuda_median_ms"] - t4["reported_speedup"]) < 0.01
    assert tasks["synthetic_personalized_risk_curves"]["clinical_effect_estimated"] is False
    assert tasks["off_by_a_beat"]["full_clinical_paper_reproduced"] is False if "full_clinical_paper_reproduced" in tasks["off_by_a_beat"] else True

def check_publication_integrity() -> None:
    citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    assert "cff-version: 1.2.0" in citation
    assert "type: software" in citation
    assert "license: MIT" in citation
    assert "version: 0.1.0" in citation
    software_license = (ROOT / "LICENSE").read_text(encoding="utf-8")
    assert "MIT License" in software_license
    assert "Farshid Bagheri Saravi" in software_license
    assert "Farshid" in citation and "Bagheri Saravi" in citation
    assert not (ROOT / ".zenodo.json").exists(), "A .zenodo.json file would override CITATION.cff"
    assert (ROOT / "data" / "LICENSE.txt").exists()
    assert (ROOT / "docs" / "zenodo-publication-guide.md").exists()
    notebook = json.loads((ROOT / "experiments" / "colab-t4" / "NVIDIA_Causal_ML_CPU_CUDA_Benchmark.ipynb").read_text(encoding="utf-8"))
    assert notebook["cells"] and any(c.get("cell_type") == "code" for c in notebook["cells"])

def main() -> None:
    files, links = check_markdown_links()
    check_evidence()
    check_publication_integrity()
    print(f"Research metadata integrity PASS: {files} Markdown files, {links} local links, "
          "synthetic-result metadata, citation and preserved notebook.")

if __name__ == "__main__":
    main()
