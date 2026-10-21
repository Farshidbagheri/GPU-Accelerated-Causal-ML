"""Re-execute selected original toy-notebook cells from Tang et al. (2026).

This script DOES NOT reconstruct the authors' model. Instead it loads their
unmodified upstream notebook at a pinned revision and executes exact code
cells 6, 7, 8, 11, 13, 16, 17 from the 100-episode illustrative example.
It does not reproduce the MIMIC-III result, a causal antibiotic estimator,
a GPU experiment, or the full figure/tables of the paper.
"""
import argparse
import json
from pathlib import Path
import numpy as np

UPSTREAM_SHA = "2f3e58c8a9186f68b22b0ab5b82c6f9366968ac6"
CELLS = [6, 7, 8, 11, 13, 16, 17]


def reproduce(notebook_path: Path) -> dict:
    nb = json.loads(notebook_path.read_text(encoding="utf8"))
    namespace = {"__name__": "__original_notebook_subset__"}
    for cell_index in CELLS:
        cell = nb["cells"][cell_index]
        assert cell["cell_type"] == "code", cell_index
        code = "".join(cell["source"])
        exec(compile(code, str(notebook_path) + "#cell_" + str(cell_index), "exec"), namespace)
    orig = namespace["π_orig"]
    shifted = namespace["π_shifted"]
    assert orig.shape == (2, 2) and shifted.shape == (2, 2)
    assert np.isfinite(orig).all() and np.isfinite(shifted).all()
    np.testing.assert_allclose(orig.sum(axis=1), 1.0)
    np.testing.assert_allclose(shifted.sum(axis=1), 1.0)
    actions_orig = orig.argmax(axis=1)
    actions_shifted = shifted.argmax(axis=1)
    disagreed = int((actions_orig != actions_shifted).sum())
    true_env = namespace["env"].env
    true_original_v = namespace["policy_evaluation"](true_env.P, orig)
    true_shifted_v = namespace["policy_evaluation"](true_env.P, shifted)
    result = {
        "paper": "Tang et al., npj Digital Medicine (2026)",
        "doi": "10.1038/s41746-026-02625-2",
        "upstream_repository": "shengpu-tang/RL-Off-by-a-Beat",
        "upstream_commit": UPSTREAM_SHA,
        "notebook": "synthetic/Toy_Problem.ipynb",
        "executed_original_notebook_cell_indices": CELLS,
        "experiment": "authors' illustrative 100-episode toy example",
        "n_episodes": len(namespace["episode_data"]),
        "n_time_steps_per_episode": 10,
        "behavior_policy": namespace["π_b"].tolist(),
        "learned_policy_original_alignment": orig.tolist(),
        "learned_policy_shifted_alignment": shifted.tolist(),
        "statewise_policy_disagreement_count": disagreed,
        "n_states": 2,
        "true_environment_value_original": true_original_v.tolist(),
        "true_environment_value_shifted": true_shifted_v.tolist(),
        "mean_true_value_original": float(np.mean(true_original_v)),
        "mean_true_value_shifted": float(np.mean(true_shifted_v)),
        "paper_main_table_reproduced": False,
        "clinical_data_used": False,
        "gpu_used": False,
        "interpretation": "One run of selected original toy-notebook cells, not paper-wide reproduction."
    }
    return result


def reproduce_full_toy_sweep(notebook_path: Path) -> dict:
    """Execute the authors' unmodified 'All Experiments' toy code cells."""
    nb = json.loads(notebook_path.read_text(encoding="utf8"))
    original_cells = [6, 7, 8, 29, 38, 39, 40, 41, 43, 45, 46, 48]
    namespace = {"__name__": "__original_toy_sweep__"}
    for i in original_cells:
        c = nb["cells"][i]
        assert c["cell_type"] == "code"
        exec(compile("".join(c["source"]), str(notebook_path) + "#cell_" + str(i), "exec"), namespace)

    orig = namespace["avg_π_orig"]
    shifted = namespace["avg_π_shifted"]
    v_orig = namespace["G_orig"]
    v_shifted = namespace["G_shifted"]
    assert len(namespace["all_results"]) == 100
    assert np.isfinite(v_orig).all() and np.isfinite(v_shifted).all()
    np.testing.assert_allclose(orig.sum(axis=1), 1)
    np.testing.assert_allclose(shifted.sum(axis=1), 1)
    per_run_disagreements = [
        int((r["orig"]["π"].argmax(axis=1) != r["shifted"]["π"].argmax(axis=1)).sum())
        for r in namespace["all_results"]
    ]
    return {
        "paper": "Tang et al., npj Digital Medicine (2026)",
        "doi": "10.1038/s41746-026-02625-2",
        "experiment": "authors' 100-run synthetic all-experiments toy sweep",
        "notebook": "synthetic/Toy_Problem.ipynb",
        "upstream_commit": UPSTREAM_SHA,
        "executed_unmodified_original_cell_indices": original_cells,
        "n_runs": 100,
        "n_episodes_per_run": 100,
        "n_steps_per_episode": 100,
        "average_policy_original": orig.tolist(),
        "average_policy_shifted": shifted.tolist(),
        "mean_true_environment_discounted_value_original": float(np.mean(v_orig)),
        "mean_true_environment_discounted_value_shifted": float(np.mean(v_shifted)),
        "true_environment_value_original_by_state": v_orig.tolist(),
        "true_environment_value_shifted_by_state": v_shifted.tolist(),
        "runs_with_at_least_one_different_state_action": int(sum(x > 0 for x in per_run_disagreements)),
        "mean_different_actions_per_run_among_two_states": float(np.mean(per_run_disagreements)),
        "full_clinical_paper_reproduced": False,
        "gpu_used": False,
        "real_clinical_data_used": False,
        "warning": "Unmodified toy subset of paper only. Not the 750-state MIMIC-III benchmark."
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--notebook", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--mode", choices=["illustration", "full-toy-sweep"], default="illustration")
    args = parser.parse_args()
    result = reproduce(args.notebook) if args.mode == "illustration" else reproduce_full_toy_sweep(args.notebook)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
