from itertools import product
import pandas as pd
from TimeSeries import rsrc_dir
from TimeSeries.debut import Debuts
from Fitting.data_preparation import N
from Fitting.fit_sum import TRGs, Slopes
from Fitting.waiting_time import CCWaitingTimes
from Fitting.apparent_TRGs import get_sfig6 as _get_sfig6
from Share.portion import Portions


R_FILES = {'wts': f'{rsrc_dir}/data/waiting_times.csv'}


def get_sfig1():
    """Identical to <{base_dir}/plots/raw_data/supplementary/sfig1.csv>"""
    return map(from1990to2018, [N, Debuts('any', n=1).counts])


def get_sfig3():
    """Identical to <{base_dir}/plots/raw_data/supplementary/sfig3.csv>"""
    return CCWaitingTimes()[(1980, 2016)]


def get_sfig4():
    """Identical to <{base_dir}/plots/raw_data/supplementary/sfig4.csv>"""
    news = {}
    for mtype, n in product(['any', 'paper', 'patent_gon'], [1, 2, 3, 0]):
        news[(mtype, n)] = from1990to2018(Debuts(mtype, n=n).counts)
    return news


def get_sfig5():
    """Identical to <{base_dir}/plots/raw_data/supplementary/sfig5_paper.csv> & <{base_dir}/plots/raw_data/supplementary/sfig5_patent.csv>"""
    paper = Portions('paper').transposed
    patent = Portions('patent_gon').transposed
    fields = {'Med. sci.': 'Med. sci.',
              'Blood': 'Blood-assoc.',
              'Appl. biotech': 'Appl. biotech.',
              'Metab. eng.': 'Metab. eng.',
              'Pharmacology': 'Pharma.',
              'Genetic tools': 'Genetic tools',
              'Immunology': 'Immun.',
              'Plant sci.': 'Plant sci.',
              'Gen. microb.': 'Gen. microb.',
              'Others': 'Others'}

    return {new: from1990to2018_fill(paper[old], 0) for old, new in fields.items()}, \
           {new: from1990to2015_fill(patent[old], 0) for old, new in fields.items()}


def get_sfig6():
    """Identical to <{base_dir}/plots/raw_data/supplementary/sfig6.pkl> or <{base_dir}/plots/raw_data/supplementary/sfig6.csv>"""
    return _get_sfig6()


def get_sfig7():
    """Identical to <{base_dir}/plots/raw_data/supplementary/sfig7.csv>"""
    q = pd.read_csv(R_FILES['wts'], index_col=0)
    return q.query("status=='DebutFirst'").debuted.values


def get_sfig8_trgs():
    return [v18 for v97, v99, v00, v18 in TRGs().fvalues()]


def get_sfig8_slopes():
    return Slopes().fvalues()


def get_sfig8_taus():
    return [tau for tau, beta in Slopes().fkeys()]


def from1990to2018(dct):
    return {k: v for k, v in dct.items() if 1990 <= k <= 2018}


def from1990to2015_fill(dct, fill=0):
    return {k: dct.get(k, fill) for k in range(1990, 2016)}


def from1990to2018_fill(dct, fill=0):
    return {k: dct.get(k, fill) for k in range(1990, 2019)}

