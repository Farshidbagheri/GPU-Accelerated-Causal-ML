import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import pandas as pd
import pytest
from timing_audit import audit_vitals,pyxis_descriptive_audit

def test_decision_probe_excludes_future_documentation():
    stays=pd.DataFrame({'stay_id':[1,2],'intime':['2026-01-01 10:00','2026-01-01 10:00'],'outtime':['2026-01-01 14:00','2026-01-01 14:00']})
    vs=pd.DataFrame({'stay_id':[1,1,1],'charttime':['2026-01-01 10:10','2026-01-01 11:01','2026-01-01 15:00'],'heartrate':[95,101,100]})
    by,stats=audit_vitals(stays,vs,offset_minutes=60)
    row=by.loc[by.stay_id==1].iloc[0]
    assert row.pre_decision_events==1
    assert row.post_decision_events==2
    assert row.outside_ed_window_events==1
    assert stats['n_stays_with_vitals']==1
    assert stats['clinical_causal_effects_estimated'] is False

def test_missing_columns_rejected():
    with pytest.raises(ValueError): audit_vitals(pd.DataFrame({'stay_id':[1]}),pd.DataFrame({'stay_id':[1],'charttime':['2026-01-01']}))

def test_pyxis_not_admin_exposure():
    s=pd.DataFrame({'stay_id':[5],'intime':['2026-01-01'],'outtime':['2026-01-02']})
    p=pd.DataFrame({'stay_id':[5,5],'charttime':['2026-01-01','2026-01-01'],'name':['A','A'],'med_rn':[1,1]})
    m=pyxis_descriptive_audit(s,p)
    assert m['n_unique_charted_dispense_rows']==1
    assert 'not verified' in m['warning']
