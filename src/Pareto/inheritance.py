import pickle
from itertools import product, takewhile
from more_itertools import pairwise
from TimeSeries import rsrc_dir
from TimeSeries.time_series import YGH
from Pareto.pareto import subplot, except_tools, after1990
from Plot.tools import set_new_xlim

R_FILES = {
    'fields': f'{rsrc_dir}/data/fields.json'
}

W_FILES = {
    'paper': f'{rsrc_dir}/pdata/inheritance/inheritance_WO_paper_rank.pkl',
    'patent': f'{rsrc_dir}/pdata/inheritance/inheritance_WO_patent_rank.pkl',
    'patent_gon': f'{rsrc_dir}/pdata/inheritance/inheritance_WO_patent_gon_rank.pkl',
    'any': f'{rsrc_dir}/pdata/inheritance/inheritance_WO_any_rank.pkl',
}


class Inheritance(dict):
    """
    {interval0 := (y0_start, y0_stop): fraction of genes which ranked within the top 'rank' in their hit counts
                                       in both interval0 and interval1 among top 'rank' genes in interval0}
    """
    R_FILES = R_FILES['fields']
    W_FILES = W_FILES

    def __init__(self, mtype, rank, without_tools=False, load=True):
        self.mtype, self.rank, self.wo = mtype, rank, without_tools
        if load:
            data = self.load(mtype, rank, without_tools)
        else:
            _ygh = after1990(load_ygh(mtype))
            ygh = except_tools(_ygh) if without_tools else _ygh
            data = count(top_x_ranks(windowed(ygh), rank))
        super().__init__(data)

    def dump(self):
        with open(self.w_file(self.mtype, self.rank, self.wo), 'wb') as file:
            pickle.dump(dict(self), file)

    @classmethod
    def load(cls, mtype, rank, without_tools):
        with open(cls.w_file(mtype, rank, without_tools), 'rb') as file:
            return pickle.load(file)

    @classmethod
    def w_file(cls, mtype, rank, without_tools):
        x = cls.W_FILES[mtype]
        rank_str = str(rank).replace('-', '_')
        return x.replace('rank', rank_str).replace('_WO', '_wo' if without_tools else '')


def load_ygh(mtype):
    if mtype in ['paper', 'any']:
        return YGH(mtype, n=1, load=True)
    else:
        return YGH.init_with_endyear(mtype, n=1, endyear=2018)


def count(top_players):
    res = {}
    for (w0, p0), (w1, p1) in pairwise(top_players.items()):
        res[w0] = len(p0.intersection(p1)) / len(p0)
    return res


def top_x_ranks(wgh, x):
    if x < 0:
        top_players = {w: top_x_rank_tie_in(len(gh), gh) for w, gh in wgh.items()}
    else:
        top_players = {w: top_x_rank_tie_in(x, gh) for w, gh in wgh.items()}
    return top_players


def top_x_rank_tie_in(x: int, gh: dict):
    """gh: {gene -> hit} of a year"""
    if x >= len(gh):
        return set(gh)
    else:
        genes = sorted(gh, key=gh.__getitem__, reverse=True)
        smallest = gh[genes[x-1]]
        return set(takewhile(lambda g: gh[g] >= smallest, genes))


def windowed(ygh, wl=3):
    """
    If ygh.keys() spans from 1990 to 2018,
        :return dct_reversed({(2014, 2019): dict_sum([ygh[y] for y in range(2014, 2019)),
                              (2009, 2014): dict_sum([ygh[y] for y in range(2009, 2014)),
                              ...
                              (1994, 1999): dict_sum([ygh[y] for y in range(1994, 1999))})

    The interval (1990, 1994) has not been used since its shorter than the window length (= 5).
    """
    wgh = {}
    args = [reversed(ygh.items())]*wl
    for window in zip(*args):
        years, ghs = zip(*window)
        intv = years[-1], years[0]+1
        wgh[intv] = dict_sum(*ghs)
    return dct_reversed(wgh)


def dct_reversed(dct):
    return dict(reversed(dct.items()))


def dict_sum(*dcts):
    """
    If dict_sum({'a': 5, 'b': 3}, {'a': 10.2, 'c': 4.2}, {'d': 5.1})
        :return {'a': 15.2, 'b': 3, 'c': 4.2, 'd': 5.1}
    """
    res = {}
    for dct in dcts:
        for k, v in dct.items():
            res[k] = res.setdefault(k, 0) + v
    return res


def plot(save=False):
    mtypes = ['paper', 'patent_gon']
    ranks = [-1, 10, 20, 50, 100]
    wos = [True, False]
    for mtype, wo in product(mtypes, wos):
        fig, axes = subplot()
        for axis, rank in zip(axes, ranks):
            q = Inheritance(mtype, rank, wo)
            keys = [i for i, f in q.keys()]
            last = next(reversed(q.keys()))[1]
            ticks = keys + [last]

            axis.bar(keys, q.values(), align='edge', width=2.1)
            axis.set_xticks(ticks)
            axis.set_xticklabels(ticks, fontsize=8, rotation=45, rotation_mode='anchor', ha='right', va='top')
            set_new_xlim(axis, (ticks[0], ticks[-1]))
            axis.set_ylim(0, 1.0)
            axis.set_title(f'{mtype} {rank}')
        fig.show()
        if save:
            fig.savefig(f'./{mtype}_{wo}.png', dpi=500)


def main():
    mtypes = ['paper', 'patent_gon']
    ranks = [-1, 10, 20, 50, 100]
    wos = [True, False]
    for mtype, rank, wo in product(mtypes, ranks, wos):
        Inheritance(mtype, rank, wo, load=False).dump()
