import sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from longitudinal_synthetic_benchmark import simulate,split_by_patient,experiment

def test_dgp_reproducible():
    a=simulate(n_patients=25,seed=40);b=simulate(n_patients=25,seed=40)
    np.testing.assert_allclose(a["y"],b["y"])
    assert a["features"].shape==(150,5)
    assert np.isfinite(a["true_ite"]).all()

def test_patient_split():
    d=simulate(n_patients=100,seed=40)
    tr,val,te=split_by_patient(d,40)
    assert not (set(d["pid"][tr]) & set(d["pid"][te]))
    assert tr.sum()+val.sum()+te.sum()==600

def test_model_produces_estimates():
    d=experiment(seed=40,n_patients=90,epochs=8)
    assert d["test_patients"]>0
    assert len(d["independent_test_aipw_95pct_ci"])==2
    assert all(np.isfinite(m["pehe_rmse"]) for m in d["methods"].values())
    assert d["gpu_speedup_measured"] is False
