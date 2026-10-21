"""Audit decision-time eligibility of ED chart events; not a treatment effect estimator.

Only public MIMIC-IV-ED Demo data should be processed. This module makes no
claims that charttime is the clinical time at which information became available.
"""
from __future__ import annotations
import pandas as pd

REQUIRED_STAYS = {'stay_id', 'intime', 'outtime'}
REQUIRED_EVENTS = {'stay_id', 'charttime'}
VITALS = ('heartrate', 'sbp', 'dbp', 'resprate', 'o2sat', 'temperature')


def _require(df: pd.DataFrame, cols: set, name: str) -> None:
    missing = cols.difference(df.columns)
    if missing:
        raise ValueError(f"{name}: missing required columns: {sorted(missing)}")


def audit_vitals(stays: pd.DataFrame, vitals: pd.DataFrame, offset_minutes: int = 60) -> tuple[pd.DataFrame, dict]:
    """One row per stay. Audit how many recorded vitals would leak across a hypothetical decision time.

    The decision time (ED arrival + offset_minutes) is a *methodological probe*, not an observed clinical action.
    Input charttime = documentation timestamp, NOT reliably measurement or clinical-availability time.
    """
    _require(stays, REQUIRED_STAYS, 'edstays')
    _require(vitals, REQUIRED_EVENTS, 'vitalsign')
    if offset_minutes < 0:
        raise ValueError('offset_minutes must be >= 0')
    s = stays[['stay_id','intime','outtime']].drop_duplicates('stay_id').copy()
    for t in ['intime','outtime']:
        s[t] = pd.to_datetime(s[t], errors='coerce')
    s['decision_probe'] = s['intime'] + pd.to_timedelta(offset_minutes, unit='m')
    v = vitals.copy()
    v['charttime'] = pd.to_datetime(v['charttime'], errors='coerce')
    m = v.merge(s,on='stay_id',how='inner',validate='many_to_one')
    m['pre_decision'] = m['charttime'].notna() & m['decision_probe'].notna() & (m['charttime'] <= m['decision_probe'])
    m['post_decision'] = m['charttime'].notna() & m['decision_probe'].notna() & (m['charttime'] > m['decision_probe'])
    m['outside_ed_window'] = m['charttime'].notna() & ((m['charttime'] < m['intime']) | (m['charttime'] > m['outtime']))
    per = m.groupby('stay_id',as_index=False).agg(
        vitals_events=('charttime','size'),
        pre_decision_events=('pre_decision','sum'),
        post_decision_events=('post_decision','sum'),
        outside_ed_window_events=('outside_ed_window','sum'),
    )
    out=s[['stay_id','decision_probe']].merge(per,how='left',on='stay_id')
    count_cols=['vitals_events','pre_decision_events','post_decision_events','outside_ed_window_events']
    out[count_cols]=out[count_cols].fillna(0).astype(int)
    out['post_decision_fraction']=out['post_decision_events'].div(out['vitals_events'].where(out['vitals_events'].ne(0))).round(4)
    metrics={
        'n_stays':int(len(s)),
        'n_stays_with_vitals':int((out.vitals_events > 0).sum()),
        'n_vitals_events':int(out.vitals_events.sum()),
        'n_pre_decision_events':int(out.pre_decision_events.sum()),
        'n_post_decision_events':int(out.post_decision_events.sum()),
        'n_outside_ed_window':int(out.outside_ed_window_events.sum()),
        'offset_minutes':int(offset_minutes),
        'clinical_causal_effects_estimated':False,
        'data_access': 'MIMIC-IV-ED Demo v2.2 (if real data loaded)',
        'caveat': 'charttime is documentation time; availability and treatment time are not established',
    }
    return out,metrics


def pyxis_descriptive_audit(stays: pd.DataFrame, pyxis: pd.DataFrame) -> dict:
    """Describe unique medication chart events, never equating Pyxis with antibiotic administration."""
    _require(stays, REQUIRED_STAYS,'edstays')
    _require(pyxis, {'stay_id','charttime','name','med_rn'},'pyxis')
    p=pyxis[['stay_id','charttime','name','med_rn']].drop_duplicates()
    p=p[p.stay_id.isin(stays.stay_id)]
    return {'n_unique_charted_dispense_rows':int(len(p)),
            'n_stays_with_charted_dispense':int(p.stay_id.nunique()),
            'warning':'Pyxis dispensations are not verified IV antibiotic administration events.'}
