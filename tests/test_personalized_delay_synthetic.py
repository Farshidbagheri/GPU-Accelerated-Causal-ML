import sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from personalized_delay_synthetic import simulate,oracle,run
def test_factual_simulator_has_support():
    d=simulate(100,123);assert np.bincount(d['k'],minlength=5).sum()==100
    assert (d['propensity']>0).all()
def test_counterfactual_risk_curve_exists():
    d=simulate(40,200);r=oracle(d['x'],300,draws=20)
    assert r.shape==(40,5) and np.isfinite(r).all()
    assert (r[:,-1]-r[:,0]).mean()>0
def test_factual_only_trained_risk_curves():
    r=run(seed=41,n=180,epochs=8,draws=5)
    assert len(r['oracle_risk_by_start_time'])==5
    assert np.isfinite(r['scores']['ipw']['curve_rmse'])
    assert r['clinical_effect'] is False
