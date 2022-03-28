"""
Calculate shares(%) of each gene community in the debuts of n-tuples (for n>2)
 and find kings (gene communities which take the greatest share) for each year.

Share of a gene community is defined as the fraction of debuted n-tuples containing the gene community.

For example, if
    Year    Debuted n-tuples (n=3)
    2000    (0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5)
    2001    (0, 1, 4), (0, 1, 3), (0, 2, 6)

, then
    Cmnt    Share (at 2000)     Share (at 2001)
    0       3/4 = 0.75          3/3 = 1.0
    1       2/4 = 0.5           2/3 = 0.66...
    2       1/4 = 0.25          1/3 = 0.33...
    3       1/4 = 0.25          1/3 = 0.33...
    4       1/4 = 0.25          1/3 = 0.33...
    5       2/4 = 0.5           0/3 = 0.0
    6       1/4 = 0.25          1/3 = 0.33...
"""
import pickle
from itertools import groupby
from collections import Counter
import pandas as pd
from NestedDict.klv import KLV
from TimeSeries import rsrc_dir
from TimeSeries.LoHL import LoHL
from TimeSeries.debut import Debuts

R_FILES = {
    'nicknames': f'{rsrc_dir}/data/nicknames.csv',

    'debut': {
        'paper': f'{rsrc_dir}/pdata/debut/debut_paper_n-tuple.pkl',
        'patent': f'{rsrc_dir}/pdata/debut/debut_patent_n-tuple.pkl',
        'patent_gon': f'{rsrc_dir}/pdata/debut/debut_patent_gon_n-tuple.pkl',
        'any': f'{rsrc_dir}/pdata/debut/debut_any_n-tuple.pkl',
    },
}

W_FILES = {
    'score': {
        'paper': f'{rsrc_dir}/pdata/share/score_paper_wl.csv',
        'patent': f'{rsrc_dir}/pdata/share/score_patent_wl.csv',
        'patent_gon': f'{rsrc_dir}/pdata/share/score_patent_gon_wl.csv',
        'any': f'{rsrc_dir}/pdata/share/score_any_wl.csv',
    },

    'share': {
        'paper': f'{rsrc_dir}/pdata/share/share_paper_wl.csv',
        'patent': f'{rsrc_dir}/pdata/share/share_patent_wl.csv',
        'patent_gon': f'{rsrc_dir}/pdata/share/share_patent_gon_wl.csv',
        'any': f'{rsrc_dir}/pdata/share/share_any_wl.csv',
    },

    'vip': {
        'paper': f'{rsrc_dir}/pdata/share/vip_paper_wl.csv',
        'patent': f'{rsrc_dir}/pdata/share/vip_patent_wl.csv',
        'patent_gon': f'{rsrc_dir}/pdata/share/vip_patent_gon_wl.csv',
        'any': f'{rsrc_dir}/pdata/share/vip_any_wl.csv',
    },

    'cum_rank': {
        'paper': f'{rsrc_dir}/pdata/share/cum_rank_paper.csv',
        'patent': f'{rsrc_dir}/pdata/share/cum_rank_patent.csv',
        'patent_gon': f'{rsrc_dir}/pdata/share/cum_rank_patent_gon.csv',
        'any': f'{rsrc_dir}/pdata/share/cum_rank_any.csv',
    },
}


class Nicknames(dict):
    R_FILES = R_FILES['nicknames']
    greeks = {'\\u03b1': 'α', '\\u03b2': 'β', '\\u03b3': 'γ',
              '\\u03b4': 'δ', '\\u03b5': 'ε', '\\u03b6': 'ζ',
              '\\u03b7': 'η', '\\u03b8': 'θ', '\\u03b9': 'ι',
              '\\u03ba': 'κ', '\\u03bb': 'λ', '\\u03bc': 'μ',
              '\\u03bd': 'ν', '\\u03be': 'ξ', '\\u03bf': 'ο',
              '\\u03c0': 'π', '\\u03c1': 'ρ', '\\u03c2': 'ς',
              '\\u03c3': 'σ', '\\u03c4': 'τ', '\\u03c5': 'υ',
              '\\u03c6': 'φ', '\\u03c7': 'χ', '\\u03c8': 'ψ',
              '\\u03c9': 'ω', '\\u03ca': 'ϊ', '\\u03cb': 'ϋ',
              '\\u03cc': 'ό', '\\u03cd': 'ύ', '\\u03ce': 'ώ'}

    def __init__(self):
        dct = pd.read_csv(self.R_FILES, index_col=0)['Nickname'].to_dict()
        super().__init__({k: self.greek_converter(v) for k, v in dct.items()})

    def __getitem__(self, item):
        if item in self:
            return super().__getitem__(item)
        else:
            return f'gene{int(item)}'

    @classmethod
    def greek_converter(cls, x: str):
        y = x
        for _p, _g in cls.greeks.items():
            y = y.replace(_p, _g)
        return y


class Scores(KLV):
    """
    Scores: KLV (dict of dicts), {year -> {gene -> score:=the num of new pairs made}}
    .kings: KLV, {year -> {nickname of kings -> score}}
    .ikings: KLV, {year -> {gene index of kings -> score}}
    """
    R_FILES = R_FILES['debut']
    W_FILES = W_FILES['score']

    def __init__(self, mtype, window_len=1):
        """
        :param mtype: str, type of material. one of {paper, patent, patent_gon, any}
        :param window_len: int, length of sliding windows
        """
        self.mtype, self.wl = mtype, window_len
        super().__init__(self.measure_scores(mtype, window_len=window_len))
        self.ikings, self.kings = filter_kings(self)

    def to_csv(self):
        if self.wl != 1:
            raise ValueError
        w_path = self.W_FILES[self.mtype].replace('wl', f'wl{self.wl}')
        df_scores = pd.DataFrame(self).fillna(0).astype(int)
        df_scores.to_csv(w_path)

    @classmethod
    def measure_scores(cls, mtype, window_len=1):
        start = 1990
        stop = LoHL.END_YEARS[mtype] + 1
        return windowed(cls.raw_scores(mtype), start, stop, window_len)

    @classmethod
    def raw_scores(cls, mtype):
        r_path = cls.R_FILES[mtype].replace('n-tuple', '2')
        with open(r_path, 'rb') as file:
            debut = pickle.load(file)
        group_by = groupby(debut, key=debut.get)
        return {y: Counter(gene for gene in genes for gene in gene) for y, genes in group_by}


class Shares(KLV):
    """
    Share: KLV (dict of dicts), {year -> {gene -> share(%):=percentage of new pairs made}}
    .kings: KLV, {year -> {nickname of kings -> share(%)}}
    .ikings: KLV, {year -> {gene index of kings -> share(%)}}
    """
    R_FILES = R_FILES['debut']
    W_FILES = W_FILES['share']

    def __init__(self, mtype, window_len=1):
        """
        :param mtype: str, type of material. one of {paper, patent, patent_gon, any}
        :param window_len: int, length of sliding windows
        """
        self.mtype, self.wl = mtype, window_len
        super().__init__(self.measure_shares(mtype, window_len=window_len))
        self.ikings, self.kings = filter_kings(self)

    def kings_to_csv(self):
        if self.wl != 1:
            raise ValueError
        w_path = self.W_FILES[self.mtype].replace('wl', f'wl{self.wl}')
        df_scores = pd.DataFrame(self.kings).fillna(0).astype(int)
        df_scores.to_csv(w_path)

    @classmethod
    def measure_shares(cls, mtype, window_len=1):
        scores = Scores.measure_scores(mtype, window_len)
        return cls.calc_shares(scores)

    @classmethod
    def raw_scores(cls, mtype):
        scores = Scores.raw_scores(mtype)
        return cls.calc_shares(scores)

    @staticmethod
    def calc_shares(scores):
        shares = KLV()
        for k, lv in scores.items():
            total = sum(lv.values())
            shares[k] = {l: 100 * v / total for l, v in lv.items()}
        return shares


class VIPS(KLV):
    """
    VIPS: KLV, {year -> {grade -> nickname}}  where grade = 1, 2, ..., n
    .by_idx: KLV, {year -> {grade -> gene index}}
    """
    W_FILES = W_FILES['vip']

    def __init__(self, mtype, window_len=1, n=30):
        self.mtype, self.wl = mtype, window_len
        self.by_idx = self.find_vips(mtype, window_len=window_len, n=n)
        super().__init__(self.get_by_name(self.by_idx))

    def to_csv(self):
        w_path = self.W_FILES[self.mtype].replace('wl', f'wl{self.wl}')
        pd.DataFrame(self).to_csv(w_path, encoding='utf-8-sig')

    @staticmethod
    def find_vips(mtype, window_len=1, n=30):
        vips = {}
        scores = Scores(mtype, window_len=window_len)
        for k, lv in scores.items():
            ordered = sorted(lv, key=lv.get, reverse=True)[:n]
            vips[k] = dict(enumerate(ordered, start=1))
        return vips

    @staticmethod
    def get_by_name(by_idx):
        nicknames = Nicknames()
        return {k: {l: nicknames[v] for l, v in lv.items()} for k, lv in by_idx.items()}


def filter_kings(ycv):
    nicknames = Nicknames()
    kings = {(gene := max(v, key=v.get)): nicknames[gene] for v in ycv.values()}
    ycv_kings_by_idx = {k: {gene: lv.get(gene, 0) for gene in kings} for k, lv in ycv.items()}
    ycv_kings = {k: {name: lv.get(gene, 0) for gene, name in kings.items()} for k, lv in ycv.items()}
    return ycv_kings_by_idx, ycv_kings


def windowed(ycv: dict, start, stop, step):
    c = Counter()
    return {y: sum((ycv.get(yy, c) for yy in range(y, y+step)), c) for y in range(start, stop, step)}


def cumulative_rank(mtype, n=30):
    dy1 = Debuts(mtype, n=1, load=True)
    dy2 = Debuts(mtype, n=2, load=True)
    sc = Scores(mtype, window_len=2018-1990+1)
    sh = Shares(mtype, window_len=2018-1990+1)
    vips = VIPS(mtype, window_len=2018-1990+1, n=n)

    names = vips[1990].values()
    genes = vips.by_idx[1990].values()
    scores = [sc[1990][gene] for gene in genes]
    shares = [sh[1990][gene] for gene in genes]
    singlets = [dy1[gene] for gene in genes]
    doublets = [min(year for pair, year in dy2.items() if gene in pair) for gene in genes]
    return pd.DataFrame({'gene': genes, 'name': names,
                         'score': scores, 'share': shares,
                         'singlet': singlets, 'doublet': doublets}, index=range(1, 31))


def update():
    mtype = 'any'
    Scores(mtype, window_len=1).to_csv()
    Shares(mtype, window_len=1).kings_to_csv()
    VIPS(mtype, window_len=5).to_csv()
    cumulative_rank(mtype, n=30).to_csv(W_FILES['cum_rank'][mtype], encoding='utf-8-sig')
