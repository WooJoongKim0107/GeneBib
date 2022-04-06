"""
Plot the scatter plot on Fig.1i - 1. total paper hit vs total patent hit, 2. total patent hit/total paper hit vs
    total paper hit.
"""
from functools import partial
from more_itertools import pairwise
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from UpperBound.base import calc_gth, get_gyh_within, coordinatize, log_binned_median, isover
from Plot.plotter import ExFigure


class Coordinates(dict):
    def __init__(self, lag=5):
        gth_paper = calc_gth(get_gyh_within('paper', 1990, 2015-lag))
        gth_patent = calc_gth(get_gyh_within('patent_gon', 1990, 2015))
        data = coordinatize(gth_paper, gth_patent)
        super().__init__({gene: data[gene] for gene in sorted(data, key=data.__getitem__)})

    def draw(self, axis, a=1.86, r=0.56):
        axis.plot(*zip(*self.values()), 'ko', alpha=0.5, ms=0.35, mew=0.842)
        draw_axr(axis, a=a, r=r)
        axis.loglog()
        _ = self.linregress()
        print(f'{self.percentage_over(a=a, r=r):.4f}% are over the line')

    def draw_sublinearity(self, axis, a=1.86, r=0.56):
        q = {g: (x, y / x) for g, (x, y) in self.items()}
        axis.plot(*zip(*q.values()), 'ko', alpha=0.5, ms=0.35, mew=0.842)
        draw_axr_bottom(axis, a=a, r=r)
        draw_median(axis, q.values())
        axis.loglog()
        print(f'Median settle down to {log_binned_median(q.values())[1][-1]:.4f}')

    def percentage_over(self, a, r):
        _isover = partial(isover, a=a, r=r)
        return 100*sum(_isover(v) for v in self.values())/len(self)

    def test(self, a=1.86, r=0.56):
        fig, axes = subplots()
        self.draw(axes[0], a=a, r=r)
        self.draw_sublinearity(axes[1], a=a, r=r)
        fig.show()
        return fig, axes

    def linregress(self):
        x, y = zip(*self.values())
        lx, ly = np.log10([x, y])
        slope, intercept, rvalue, *_ = linregress(lx, ly)
        a, r = slope, 10**intercept
        print(f'(Linear regression) {a=:.4f}, {r=:.4f}, R={rvalue:.4f}')
        return a, r


def draw_axr(axis, a, r):
    xm = axis.get_xlim()[1]
    x = np.logspace(0, np.log10(xm), 29, endpoint=False)
    y = a*x**r
    axis.plot(x, y, '-', color='grey', lw=1.2)


def draw_axr_bottom(axis, a=1.86, r=0.56):
    xm = axis.get_xlim()[1]
    x = np.logspace(0, np.log10(xm), 29, endpoint=False)
    y = a*x**(r-1)
    axis.plot(x, y, '-', color='grey', lw=1.2)


def draw_median(axis, xys):
    bins, medians = log_binned_median(xys)
    x = [(i+f)/2 for i, f in pairwise(bins)]
    axis.plot(x, medians, 'ro', ms=2.0)


def subplots():
    fig = plt.figure(figsize=(2.5, 2.8), FigureClass=ExFigure)
    axis_lower = fig.add_axes([(0.5, 'figure'), (0.5, 'inches'), (1.326, 'inches'), (0.997, 'inches')], ha=0)
    axis_upper = fig.add_axes([(0.0, axis_lower), (1, axis_lower), (1.326, 'inches'), (0.997, 'inches')],
                              [(0, 0), (0.073, 'inches'), (0, 0), (0, 0)])
    axis_upper.xaxis.set_tick_params(bottom=False, labelbottom=False)
    fig.set_dpi(1000)
    return fig, (axis_upper, axis_lower)
