from pathlib import Path
import sys
import pandas as pd
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from run_pilot import analyze


def test_multi_offset_monotonicity(tmp_path):
    pd.DataFrame({
        "stay_id": [1], "intime": ["2026-01-01 10:00"],
        "outtime": ["2026-01-01 13:00"]
    }).to_csv(tmp_path / "edstays.csv.gz", index=False, compression="gzip")
    pd.DataFrame({
        "stay_id": [1, 1, 1],
        "charttime": ["2026-01-01 10:15", "2026-01-01 10:45", "2026-01-01 11:30"],
        "heartrate": [90, 91, 92]
    }).to_csv(tmp_path / "vitalsign.csv.gz", index=False, compression="gzip")
    r = analyze(tmp_path, [120, 30, 60])
    assert list(r["offsets"]) == ["30", "60", "120"]
    assert [r["offsets"][k]["n_pre_decision_events"] for k in r["offsets"]] == [1, 2, 3]
    assert r["offsets"]["30"]["n_post_decision_events"] == 2
    assert "clinical inference" in r["limitations"][2]


def test_negative_offset_rejected(tmp_path):
    pd.DataFrame({
        "stay_id": [1], "intime": ["2026-01-01"], "outtime": ["2026-01-02"]
    }).to_csv(tmp_path / "edstays.csv.gz", index=False, compression="gzip")
    pd.DataFrame({
        "stay_id": [1], "charttime": ["2026-01-01"]
    }).to_csv(tmp_path / "vitalsign.csv.gz", index=False, compression="gzip")
    with pytest.raises(ValueError):
        analyze(tmp_path, [-1])
