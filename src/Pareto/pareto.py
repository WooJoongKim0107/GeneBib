"""
Check if Pareto's principle holds for our work, i.e., measure the fraction of papers/patents that top x genes appear.
"""
import json
import pickle
from operator import itemgetter
from itertools import groupby
from more_itertools import take
import matplotlib.pyplot as plt
from TimeSeries import rsrc_dir, safe_update
from TimeSeries.LoHL import LoHL
from TimeSeries.time_series import YGH
from Plot.tools import ExFigure
from Plot.plotter import TimeSeriesPlt

R_FILES = {
    'fields': f'{rsrc_dir}/data/fields.json'
}

W_FILES = {
    'paper': f'{rsrc_dir}/pdata/pareto/pareto_WO_paper_rank.pkl',
    'patent': f'{rsrc_dir}/pdata/pareto/pareto_WO_patent_rank.pkl',
    'patent_gon': f'{rsrc_dir}/pdata/pareto/pareto_WO_patent_gon_rank.pkl',
    'any': f'{rsrc_dir}/pdata/pareto/pareto_WO_any_rank.pkl',
}


class Pareto(dict):
    R_FILES = R_FILES['fields']
    W_FILES = W_FILES

    def __init__(self, mtype, rank, without_tools=False, load=True):
        self.mtype, self.rank, self.wo = mtype, rank, without_tools
        if load:
            data = self.load(mtype, rank, without_tools)
        else:
            lohl, _ygh = load_lohl_ygh(mtype)
            ygh = except_tools(after1990(_ygh)) if without_tools else after1990(_ygh)
            data = count_all(lohl, ygh, rank)
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
        x1 = x.replace('_WO', '_wo' if without_tools else '')
        return x1.replace('rank', str(rank))


def load_lohl_ygh(mtype):
    if mtype in ['paper', 'any']:
        lohl = LoHL(mtype, load=True)
        ygh = YGH(mtype, n=1, load=True)
    else:
        lohl = LoHL.init_with_endyear(mtype, endyear=2018)
        ygh = YGH.init_with_endyear(mtype, n=1, endyear=2018)
    return lohl, ygh


def after1990(ygh):
    return {y: gh for y, gh in ygh.items() if y >= 1990}


def except_tools(ygh):
    with open(R_FILES['fields'], 'r') as file:
        tools = json.load(file)['Genetic tools']
    return {y: {g: h for g, h in gh.items() if g not in tools} for y, gh in ygh.items()}


def count_all(lohl, ygh, rank):
    res = {}
    for year, hl in groupby(lohl, itemgetter(1)):
        if 1990 <= year <= 2018:
            top_genes = top_x_rank(rank, ygh[year])
            res[year] = count(list(hl), top_genes)
    return res


def count(hl, genes):
    total = len(hl)
    num = sum(1 for midx, year, *cmnts in hl if not genes.isdisjoint(cmnts))
    return num/total


def top_x_rank(x: float, gh: dict):
    """gh: {gene -> hit} of a year"""
    return set(take(x, sorted(gh, key=gh.__getitem__, reverse=True)))


def subplot():
    fig = plt.figure(figsize=(10.5, 2), FigureClass=ExFigure)
    locator = [(0.565, 'inches'), (0.470, 'inches'), (1.35, 'inches'), (1.35, 'inches')]
    for i in range(5):
        fig.add_axes(locator, [(i / 5, 'fig'), (0, 'fig'), (0, 'fig'), (0, 'fig')])
    return fig, fig.axes


def plot(axis, pareto, mtype, rank):
    w = {k: v for k, v in pareto.items() if k >= 1990}
    axis.plot(w.keys(), w.values(), '-')
    axis.set_title(f'{mtype} {rank}')
    TimeSeriesPlt.draw_xticks(axis)


def main():
    for wo in [True, False]:
        for mtype in ['paper', 'patent_gon']:
            fig, axes = subplot()
            for axis, rank in zip(axes, [5, 10, 20, 50, 100]):
                safe_update(Pareto,
                       dict(mtype=mtype, rank=rank, without_tools=wo, load=True),
                       dict(mtype=mtype, rank=rank, without_tools=wo, load=False))
                plot(axis, Pareto(mtype, rank, without_tools=wo, load=True), mtype, rank)
            fig.show()
