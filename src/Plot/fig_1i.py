from collections import Counter
from Plot.tools import *
from Plot.plotter import TimeSeriesPlt
from TimeSeries.LoHL import LoHL
from Pareto.inheritance import Inheritance

PC = '#1f77b4ff'
TC = '#de4e4fff'
rcParams['font.size'] = 8.5
print('Modify rcParams (fig_1i.py)')


def get():
    p = Counter(y for i, y, *gs in LoHL('paper') if y >= 1990)
    t = Counter(y for i, y, *gs in LoHL.init_with_endyear('patent_gon', 2018) if y >= 1990)
    t0 = {k: v for k, v in t.items() if k <= 2015}
    t1 = {k: v for k, v in t.items() if k >= 2015}  # year=2015 included intentionally
    return p, (t0, t1)


def subplots():
    fig = plt.figure(figsize=(2.5, 2.8), FigureClass=ExFigure)
    axis0 = fig.add_axes([(0.5, 'figure'), (0.5, 'inches'), (1.326, 'inches'), (0.997, 'inches')], ha=0)
    axis1 = fig.add_axes([(0.0, axis0), (1, axis0), (1.326, 'inches'), (0.997, 'inches')],
                         [(0, 0), (0.073, 'inches'), (0, 0), (0, 0)])
    axis2 = twin_ax(axis1)
    axis1.xaxis.set_tick_params(bottom=False, labelbottom=False)
    axis1.yaxis.set_tick_params(left=True, labelleft=True)
    return fig, (axis0, (axis1, axis2))


def draw0(axis0, mtype, rank, color, makertype, linestyle):
    dct = Inheritance(mtype, rank, wl=3)
    mk = dict(zorder=1, color=color, marker='o', mfc='white' if makertype == 'filled' else None,
              ms=2.9, mew=1.1, ls='')
    if mtype in ['paper', 'any']:
        x = [f for i, f in dct]
        axis0.plot(x, dct.values(), **mk)
        axis0.plot(x, dct.values(), color=color, ls=linestyle, lw=1.1)
    else:
        x = [f for i, f in dct]
        y = [v for v in dct.values()]
        axis0.plot(x[:-1], y[:-1], **mk)
        axis0.plot(x[:-1], y[:-1], color=color, ls=linestyle, lw=1.1)
        axis0.plot(x[-2:], y[-2:], **{**mk, 'color': 'grey'})
        axis0.plot(x[-2:], y[-2:], color='grey', ls=linestyle, lw=1.1)


def polish0(axis0: plt.Axes):
    axis0.set_ylim(0.45, 1.07)
    axis0.set_yticks([0.45, 0.6, 0.8, 1.0])
    axis0.set_yticks([0.5, 0.7, 0.9], minor=True)
    axis0.set_yticklabels(['0', '60', '80', '100'])
    TimeSeriesPlt.draw_xlabel(axis0, 'Year')
    TimeSeriesPlt.draw_xticks(axis0)
    axis0.set_ylabel('Persistency (%)')


def draw1(axes):
    p, (t0, t1) = get()
    axis1, axis2 = axes
    axis1.plot(p.keys(), p.values(), '-', color=PC)
    axis2.plot(t0.keys(), t0.values(), '-', color=TC)
    axis2.plot(t1.keys(), t1.values(), '--', color=TC)


def complete_axis0(axis0):
    for mtype, color, marker in zip(['paper', 'patent_gon'], [PC, TC], ['filled', 'open']):
        for rank, ls in zip([20, 50, -1], ['-', '--', ':']):
            draw0(axis0, mtype, rank, color, marker, ls)
    polish0(axis0)


def polish1(axes):
    axis0, axis1 = axes
    axis0.set_ylim(0, 3.0e5)
    axis0.set_yticks([0, 1.0e5, 2.0e5, 3.0e5])
    axis0.set_yticks([0, 0.5e5, 1.5e5, 2.5e5], minor=True)
    axis0.set_yticklabels(['0.0', '1.0', '2.0', '3.0'])
    axis0.tick_params(axis='y', colors=PC, which='both')

    axis1.set_ylim(0, 9.0e3)
    axis1.set_yticks([0, 3.0e3, 6.0e3, 9.0e3])
    axis1.set_yticks([0, 1.5e3, 4.5e3, 7.5e3], minor=True)
    axis1.set_yticklabels(['0.0', '3.0', '6.0', '9.0'])
    axis1.tick_params(axis='y', colors=TC, which='both')

    # It must be (\u2715 10^5), not (x105),
    # but currently there is error with math expressions & unicode
    axis0.set_ylabel(f'Papers / year (x105)')
    axis1.set_ylabel(f'Patents / year (x103)', rotation=270, va='bottom')


def complete_axes(axes):
    draw1(axes)
    polish1(axes)


def main():
    fig, (axis0, axes) = subplots()
    complete_axis0(axis0)
    complete_axes(axes)
    fig.show()
    return fig, (axis0, axes)
