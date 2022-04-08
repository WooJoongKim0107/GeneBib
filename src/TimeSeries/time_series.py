"""
Make time-series of hits for each n-tuple of gene communities

The time-series will be stored in two different formats:
    1. "ygh" form
        Dictionary of dictionaries of form  {year -> {gene index -> # of hits}}
    2. "gyh" form
        Dictionary of dictionaries of form  {gene index -> {year -> # of hits}}

n-tuple == 0  generates TS for combination of arbitrary number (> 1, though) of gene communities
n-tuple == 1  generates TS for each gene gene
n-tuple == 2  generates TS for each pairs of gene communities
n-tuple == 3  generates TS for each triples of gene communities
"""
import pickle
import numpy as np
from itertools import combinations, groupby
from collections import Counter
from TimeSeries import rsrc_dir, safe_update, swap_item
from TimeSeries.LoHL import LoHL
from NestedDict.klv import KLV

W_FILES = {
    'ygh': {
        'paper': f'{rsrc_dir}/pdata/time_series/ygh_paper_n-tuple.pkl',
        'patent': f'{rsrc_dir}/pdata/time_series/ygh_patent_n-tuple.pkl',
        'patent_gon': f'{rsrc_dir}/pdata/time_series/ygh_patent_gon_n-tuple.pkl',
        'any': f'{rsrc_dir}/pdata/time_series/ygh_any_n-tuple.pkl',
    },

    'gyh': {
        'paper': f'{rsrc_dir}/pdata/time_series/gyh_paper_n-tuple.pkl',
        'patent': f'{rsrc_dir}/pdata/time_series/gyh_patent_n-tuple.pkl',
        'patent_gon': f'{rsrc_dir}/pdata/time_series/gyh_patent_gon_n-tuple.pkl',
        'any': f'{rsrc_dir}/pdata/time_series/gyh_any_n-tuple.pkl',
    },
}

ZERO = np.uint32(0)
ONE = np.uint32(1)


class YGH(KLV):
    """
    Time-series of hit in ygh-format. (ygh: {year -> {gene index -> # of hits}})
    YGH: KLV, {year -> {gene -> hit}}
    """
    R_FILES = LoHL.W_FILES
    W_FILES = W_FILES['ygh']

    def __init__(self, mtype, n=1, load=True, start_from_scratch=False):
        self.mtype, self.n = mtype, n
        if start_from_scratch:
            data = make_ygh(LoHL(mtype, load=False), n)
        else:
            data = self.load(mtype, n) if load else make_ygh(LoHL(mtype, load=True), n)
        super().__init__(data)

    def dump(self):
        ygh_path = W_FILES['ygh'][self.mtype].replace('n-tuple', str(self.n))
        with open(ygh_path, 'wb') as file:
            pickle.dump(dict(self), file)

    @staticmethod
    def load(mtype, n=1):
        ygh_path = W_FILES['ygh'][mtype].replace('n-tuple', str(n))
        with open(ygh_path, 'rb') as file:
            return pickle.load(file)

    @classmethod
    def init_with_endyear(cls, mtype, n, endyear):
        with swap_item(LoHL.END_YEARS, mtype, endyear):
            return cls(mtype, n=n, start_from_scratch=True)


class GYH(KLV):
    """
    Make time-series of hit in gyh-format. gyh: {gene index -> {year -> # of hits}}
    GYH: KLV, {gene -> {year -> hit}}
    """
    R_FILES = W_FILES['ygh']
    W_FILES = W_FILES['gyh']

    def __init__(self, mtype, n=1, load=True, start_from_scratch=False):
        self.mtype, self.n = mtype, n
        if start_from_scratch:
            data = make_gyh(YGH(mtype, n, load=False))
        else:
            data = self.load(mtype, n) if load else make_gyh(YGH(mtype, n, load=True))
        super().__init__(data)

    def dump(self):
        gyh_path = W_FILES['gyh'][self.mtype].replace('n-tuple', str(self.n))
        with open(gyh_path, 'wb') as file:
            pickle.dump(dict(self), file)

    @staticmethod
    def load(mtype, n=1):
        gyh_path = W_FILES['gyh'][mtype].replace('n-tuple', str(n))
        with open(gyh_path, 'rb') as file:
            return pickle.load(file)

    @classmethod
    def init_with_endyear(cls, mtype, n, endyear):
        with swap_item(LoHL.END_YEARS, mtype, endyear):
            return cls(mtype, n=n, start_from_scratch=True)


def make_ygh(lohl, n=1):
    """
    Make time-series of hit in ygh-format.
    ygh: {year -> {gene index -> # of hits}}
    """
    ygh = {}
    for year, ilohl in groupby(lohl, lambda x: x[1]):
        if dct := Counter(comb for comb in all_combs(ilohl, n)):
            ygh[year] = dict(sorted(dct.items()))
    return ygh


def make_gyh(ygh):
    """
    Make time-series of hit in gyh-format.
    gyh: {gene index -> {year -> # of hits}}
    """
    combs = sorted(frozenset(comb for y, ch in ygh.items() for comb in ch))
    gyh = {comb: {year: ch[comb] for year, ch in ygh.items() if comb in ch} for comb in combs}
    return gyh


def all_combs(ilohl, n):
    min_size = n if n else 2
    for idx, year, *genes in ilohl:
        if len(genes) >= min_size:
            for comb in _combinations(genes, n):
                yield comb


def _combinations(x, n):
    if n > 1:
        return list(combinations(x, n))
    elif n == 1:
        return x
    else:
        return tuple(x),


def update():
    for mtype in ['paper', 'patent', 'patent_gon', 'any']:
        for n in [0, 1, 2, 3]:
            safe_update(YGH, dict(mtype=mtype, n=n, load=True), dict(mtype=mtype, n=n, load=False))
            safe_update(GYH, dict(mtype=mtype, n=n, load=True), dict(mtype=mtype, n=n, load=False))
