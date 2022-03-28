import pandas as pd
from TimeSeries.debut import Debuts
from Share.portion import Portions
from Share.share import Shares
from fitting import taubeta_rep
from Fitting.data_preparation import get_dbdt, get_bt, t2y
from Fitting.fit_sum import Chi1s, DBDTs, BTs


def get_fig2a():
    """Identical to <{base_dir}/plots/raw_data/fig2a.csv>"""
    return pd.Series({k: v for k, v in Debuts('any', n=1).counts.items() if 1990 <= k <= 2018})


def get_fig2b(mtype):
    """Identical to <{base_dir}/plots/raw_data/fig2b.csv>"""
    assert mtype in ['paper', 'patent_gon']
    return pd.DataFrame(Portions(mtype)).loc[:, 1990:].fillna(0)


def get_fig2c():
    """Identical to <{base_dir}/plots/raw_data/fig2c.csv>"""
    return pd.Series({k: v for k, v in Debuts('any', n=2).counts.items() if 1990 <= k <= 2018})


def get_fig2d():
    """Identical to <{base_dir}/plots/raw_data/fig2d.csv>"""
    return pd.DataFrame(Shares('any', window_len=1).kings).fillna(0)


def get_fig2e_chi1_matrix():
    """Identical to <{base_dir}/plots/raw_data/fig2e_chi1_matrix.csv>"""
    return pd.DataFrame(Chi1s())


def get_fig2e_fitting_results():
    """Identical to <{base_dir}/plots/raw_data/fig2e_fitting_results.csv>"""
    res = {'target_b': {t: b for t, b in get_bt().items() if 1990 <= t <= 2018},
           'target_db': {t: db for t, db in get_dbdt().items() if 1990 <= t <= 2018}}
    taubetas = [(9, 0.8), (12, 0.7), (19, 1.0)]
    for tau, beta in taubetas:
        key = taubeta_rep(tau, beta)
        res[f'{key}_db'] = dict(zip(range(1997, 2019), DBDTs()[tau][beta]))
        res[f'{key}_b'] = dict(zip(range(1997, 2019), BTs()[tau][beta]))
        res[f'{key}_y'] = dict(zip(range(1990, 2019), t2y(range(1990, 2019), tau, beta)))
    return pd.DataFrame(res)


def get_fig2e_by(tau, beta):
    rep = taubeta_rep(tau, beta)
    fitting = get_fig2e_fitting_results()
    estimation = {y: b for t, y, b in fitting[[f'{rep}_y', f'{rep}_b']].itertuples() if t >= 1997}
    target = {y: b for t, y, b in fitting[[f'{rep}_y', 'target_b']].itertuples() if t >= 1990}
    return target, estimation


def get_fig2e_dbdt(tau, beta):
    rep = taubeta_rep(tau, beta)
    fitting = get_fig2e_fitting_results()
    estimation = {t: db for t, db in fitting[f'{rep}_db'].items() if t >= 1997}
    target = {t: db for t, db in fitting['target_db'].items() if t >= 1990}
    return target, estimation
