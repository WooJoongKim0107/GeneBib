import numpy as np
from numpy import matmul
import matplotlib.pyplot as plt
from itertools import zip_longest
from matplotlib import rcParams
from matplotlib.transforms import IdentityTransform, Transform

print('Modify rcParams (Plot.tools)')
rcParams['text.usetex'] = False
rcParams['svg.fonttype'] = 'none'
rcParams["font.family"] = ["sans-serif"]
rcParams['font.sans-serif'] = ['Arial']
rcParams['font.size'] = 8.0


def set_new_xlim(ax, minmax):
    AxesLimCtrl(1/20).set_new_xlim(ax, minmax)


def set_new_ylim(ax, minmax):
    AxesLimCtrl(1/20).set_new_ylim(ax, minmax)


def set_sci_xticks(axis, exponent, format_, xticks=None):
    locs = get_xticks_in_xlim(axis) if xticks is None else xticks
    labels = [f'{v/10**exponent:{format_}}' for v in locs]
    axis.set_xticks(locs)
    axis.set_xticklabels(labels)


def draw_exponent(axis, exponent, on='y'):
    text = f"$\\times10^{exponent}$"
    x, y, ha, va = (-0.015, 1.0, 'right', 'bottom') if on == 'y' else (1.0, -0.015, 'left', 'top')
    axis.text(x, y, text, ha=ha, va=va, size=8, transform=axis.transAxes)


def set_sci_yticks(axis, exponent, format_, yticks=None):
    locs = get_yticks_in_ylim(axis) if yticks is None else yticks
    labels = [f'{v/10**exponent:{format_}}' for v in locs]
    axis.set_yticks(locs)
    axis.set_yticklabels(labels)


def legend(**kwargs):
    handles, labels = plt.gca().get_legend_handles_labels()
    labels, ids = np.unique(labels, return_index=True)
    handles = [handles[i] for i in ids]
    plt.legend(handles, labels, **kwargs)


def twin_ax(axis: plt.Axes):
    assert isinstance(axis.figure, ExFigure)
    x, y, w, h = axis.get_position().bounds
    locator = [(x, 'figure'), (y, 'figure'), (w, 'figure'), (h, 'figure')]
    ax2 = axis.figure.add_axes(locator, sharex=axis)
    ax2.set_adjustable('datalim')
    ax2.set_adjustable('datalim')
    # noinspection PyProtectedMember
    axis._twinned_axes.join(axis, ax2)
    ax2.yaxis.tick_right()
    ax2.yaxis.set_label_position('right')
    ax2.yaxis.set_offset_position('right')
    ax2.set_autoscalex_on(axis.get_autoscalex_on())
    axis.yaxis.tick_left()
    ax2.xaxis.set_visible(False)
    ax2.patch.set_visible(False)
    return ax2


class ExFigure(plt.Figure):
    def add_axes(self, *locators, ha=-1, va=-1, **kwargs):
        """
        locator: [(x, transform), (y, transform), (w, transform), (h, transform)]
        transform: Transform object that maps given position into display coordinate position

                    1)      0 / 'figure'      (use when given data is already in figure coordinate)
                    2)      'display'         (use when given data is in display coordinate)
                    3)   'inch' or 'inches'   (use when given data is in inches)
                    4)  Axes or ax.transAxes  (use when given data is in Axes coordinate)
                    5)     ax.transData       (use when given data is in Data coordinate)
                    6)   Transform object

        locator of form [(x0, transform0, x1, transform1, ...) ,...] will be converted as xywh0 + xywh1 + ...
        """
        xywh = sum(self.translate(locator) for locator in locators)
        xywh_aligned = self.align(xywh, ha=ha, va=va)
        return super().add_axes(xywh_aligned, **kwargs)

    def translate(self, locator):
        xywh = np.zeros(4)
        for _xywh, _transforms in self.unzip(locator):
            transforms = [self.convert(t) for t in _transforms]
            xywh += self.analyze(_xywh, transforms)
        return xywh

    @staticmethod
    def align(xywh, ha=-1, va=-1):
        x, y, w, h = xywh
        x -= w*(ha+1)/2
        y -= h*(va+1)/2
        return np.array([x, y, w, h])

    @staticmethod
    def analyze(xywh, transforms):
        x, _ = transforms[0].transform([xywh[0], 0])
        _, y = transforms[1].transform([0, xywh[1]])
        w, _ = transforms[2].transform([xywh[2], 0]) - transforms[2].transform([0, 0])
        _, h = transforms[3].transform([0, xywh[3]]) - transforms[3].transform([0, 0])
        return np.array([x, y, w, h])

    @staticmethod
    def unzip(locator):
        return zip(*[zip_longest(*locator, fillvalue=0)]*2)

    def convert(self, t):
        if (t == 0) or (t in ['fig', 'figure']):
            return IdentityTransform()
        elif t == 'display':
            return self.transFigure.inverted()
        elif t in ['inch', 'inches']:
            return self.dpi_scale_trans + self.transFigure.inverted()
        elif isinstance(t, plt.Axes):
            return t.transAxes + self.transFigure.inverted()
        elif isinstance(t, Transform):
            return t + self.transFigure.inverted()
        else:
            raise ValueError


class AxesLimCtrl:
    def __init__(self, r):
        self.r = r
        self.det = 1+2*r
        self.m2l = [[1+r, -r], [-r, 1+r]]
        self.l2m = [[(1+r)/self.det, r/self.det], [r/self.det, (1+r)/self.det]]

    def lim2minmax(self, lim):
        return matmul(self.l2m, lim)

    def minmax2lim(self, minmax):
        return matmul(self.m2l, minmax)

    def get_new_lim(self, old_lim, minmax):
        old_minmax = self.lim2minmax(old_lim)
        new_min = old_minmax[0] if minmax[0] is None else minmax[0]
        new_max = old_minmax[1] if minmax[1] is None else minmax[1]
        return self.minmax2lim((new_min, new_max))

    def set_new_xlim(self, ax, minmax):
        old_lim = ax.get_xlim()
        lim = self.get_new_lim(old_lim, minmax)
        ax.set_xlim(*lim)

    def set_new_ylim(self, ax, minmax):
        old_lim = ax.get_ylim()
        lim = self.get_new_lim(old_lim, minmax)
        ax.set_ylim(*lim)


def get_xticks_in_xlim(axis):
    xticks = axis.get_xticks()
    xmin, xmax = axis.get_xlim()
    return [v for v in xticks if xmin <= v <= xmax]


def get_yticks_in_ylim(axis):
    yticks = axis.get_yticks()
    ymin, ymax = axis.get_ylim()
    return [v for v in yticks if ymin <= v <= ymax]
