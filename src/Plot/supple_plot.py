from itertools import product
from Fitting.waiting_time import tau_fitted
from Plot.plotter import *
from Plot.supple_data import *


def plot_1row():
    return A4_row_subplots(TimeSeriesPlt.one_sided_pos)


def plot_2rows():
    fig = plt.figure(figsize=(8.268, 11.693 / 3), FigureClass=ExFigure)
    locator = TimeSeriesPlt.one_sided_pos
    for j in reversed(range(2)):
        for i in range(4):
            fig.add_axes(locator, [(i / 4, 'fig'), (j / 2, 'fig'), (0, 'fig'), (0, 'fig')])
    return fig, fig.axes


def plot_2rows5cols():
    fig = plt.figure(figsize=(9.7, 11.693 / 3), FigureClass=ExFigure)
    locator = TimeSeriesPlt.one_sided_pos
    for j in reversed(range(2)):
        for i in range(5):
            fig.add_axes(locator, [(i / 5, 'fig'), (j / 2, 'fig'), (0, 'fig'), (0, 'fig')])
    return fig, fig.axes


def plot_4rows5cols():
    fig = plt.figure(figsize=(9.7, 8), FigureClass=ExFigure)
    locator = TimeSeriesPlt.one_sided_pos
    for j in reversed(range(2)):
        for i in range(5):
            fig.add_axes(locator, [(i / 5, 'fig'), (j / 4, 'fig'), (0, 'fig'), (0, 'fig')])
    return fig, fig.axes


def plot_4rows3cols():
    fig = plt.figure(figsize=(8.268*3/4, 11.693*4/6), FigureClass=ExFigure)
    locator = TimeSeriesPlt.one_sided_pos
    for i in range(3):
        for j in reversed(range(4)):
            fig.add_axes(locator, [(i / 3, 'fig'), (j / 4, 'fig'), (0, 'fig'), (0, 'fig')])
    return fig, fig.axes


def plot_3rows4cols():
    fig = plt.figure(figsize=(8.268, 11.693/2), FigureClass=ExFigure)
    locator = TimeSeriesPlt.one_sided_pos
    for i in range(4):
        for j in reversed(range(3)):
            fig.add_axes(locator, [(i / 4, 'fig'), (j / 3, 'fig'), (0, 'fig'), (0, 'fig')])
    return fig, fig.axes


def plot_sfig1():
    fig = plt.figure(figsize=(8.268, 11.693/3), FigureClass=ExFigure)
    fig.add_axes([(0.565, 'inches'), (0.470, 'inches'),
                  (2.7, 'inches'), (2.7, 'inches')])
    fig.add_axes([(3.83, 'inches'), (0.470, 'inches'),
                  (1.35, 'inches'), (1.35, 'inches')])
    axes = fig.axes

    Nt, bt = get_sfig1()

    TimeSeriesPlt.draw_ts(axes[0], Nt, color='black')
    set_new_ylim(axes[0], (0, None))
    set_sci_yticks(axes[0], 4, '.1f', [0.0e4, 1.0e4, 2.0e4, 3.0e4, 4.0e4])
    TimeSeriesPlt.draw_ylabel(axes[0], 'New UniProtKB/Swiss-Prot entries ' + f'($\\times10^{4}$)')
    TimeSeriesPlt.draw_xlabel(axes[0], 'Times (Year)')

    TimeSeriesPlt.draw_ts(axes[1], bt, color='black')
    set_new_ylim(axes[1], (0, None))
    set_sci_yticks(axes[1], 3, '.1f', [0.0e3, 0.5e3, 1.0e3, 1.5e3, 2.0e3])
    TimeSeriesPlt.draw_ylabel(axes[1], 'New genes ' + f'($\\times10^{3}$)')
    return fig, axes


def plot_sfig3():
    fig = plt.figure(figsize=(3.5, 3.5), FigureClass=ExFigure)
    axis = fig.add_axes([(0.565, 'inches'), (0.470, 'inches'), (2.5, 'inches'), (2.5, 'inches')])
    prob = get_sfig3()[(1980, 2016)]

    ge = u'\u2265'
    x, y = tau_fitted(prob)
    axis.semilogy(prob.keys(), prob.values(), zorder=1, color='grey', marker='o', mfc='white', ms=4, mew=1.8, ls='')
    axis.plot(x, y, 'k-', zorder=0)
    axis.set_xlabel('t', fontsize=10)
    axis.set_ylabel(f'Pr(T {ge} t)', fontsize=10)
    return fig, axis


def plot_sfig4():
    fig, axes = plot_4rows3cols()
    for ((mtype, ntuple), new_ts), axis in zip(get_sfig4().items(), fig.axes):
        TimeSeriesPlt.draw_ts(axis, new_ts, color='black')
        set_new_ylim(axis, (0, None))

    axis = axes[3]
    set_new_ylim(axis, (0, 9.5e4))
    set_sci_yticks(axis, 4, '.1f', [0.0e4, 1.5e4, 3.0e4, 4.5e4, 6.0e4, 7.5e4, 9.0e4])
    TimeSeriesPlt.draw_ylabel(axis, 'New combinations ' + f'($\\times10^{4}$)')

    axis = axes[11]
    set_new_ylim(axis, (0, 9.5e4))
    set_sci_yticks(axis, 4, '.1f', [0.0e4, 1.5e4, 3.0e4, 4.5e4, 6.0e4, 7.5e4, 9.0e4])
    TimeSeriesPlt.draw_ylabel(axis, 'New combinations ' + f'($\\times10^{4}$)')

    axis = axes[7]
    set_new_ylim(axis, (0, 7.5e2))
    set_sci_yticks(axis, 2, '.1f', [0.0e2, 1.5e2, 3.0e2, 4.5e2, 6.0e2, 7.5e2])
    TimeSeriesPlt.draw_ylabel(axis, 'New combinations ' + f'($\\times10^{2}$)')

    axis = axes[0]
    set_new_ylim(axis, (0, None))
    set_sci_yticks(axis, 3, '.1f', [0.0e3, 0.5e3, 1.0e3, 1.5e3, 2.0e3])
    TimeSeriesPlt.draw_ylabel(axis, 'New genes ' + f'($\\times10^{3}$)')

    axis = axes[8]
    set_new_ylim(axis, (0, None))
    set_sci_yticks(axis, 3, '.1f', [0.0e3, 0.5e3, 1.0e3, 1.5e3, 2.0e3])
    TimeSeriesPlt.draw_ylabel(axis, 'New genes ' + f'($\\times10^{3}$)')

    axis = axes[4]
    set_new_ylim(axis, (0, 1050))
    set_sci_yticks(axis, 2, '.1f', [0.0e2, 2.0e2, 4.0e2, 6.0e2, 8.0e2, 10.0e2])
    TimeSeriesPlt.draw_ylabel(axis, 'New genes ' + f'($\\times10^{2}$)')

    axis = axes[9]
    set_new_ylim(axis, (0, 2.0e5))
    set_sci_yticks(axis, 5, '.1f', [0.0e5, 0.5e5, 1.0e5, 1.5e5, 2.0e5])
    TimeSeriesPlt.draw_ylabel(axis, 'New pairs ' + f'($\\times10^{5}$)')

    axis = axes[1]
    set_new_ylim(axis, (0, 2.0e5))
    set_sci_yticks(axis, 5, '.1f', [0.0e5, 0.5e5, 1.0e5, 1.5e5, 2.0e5])
    TimeSeriesPlt.draw_ylabel(axis, 'New pairs ' + f'($\\times10^{5}$)')

    axis = axes[5]
    set_new_ylim(axis, (0, 2.1e3))
    set_sci_yticks(axis, 3, '.1f', [0.0e3, 0.5e3, 1.0e3, 1.5e3, 2.0e3])
    TimeSeriesPlt.draw_ylabel(axis, 'New pairs ' + f'($\\times10^{3}$)')

    axis = axes[2]
    set_new_ylim(axis, (0, 6.0e5))
    set_sci_yticks(axis, 5, '.1f', [0.0e5, 1.0e5, 2.0e5, 3.0e5, 4.0e5, 5.0e5, 6.0e5])
    TimeSeriesPlt.draw_ylabel(axis, 'New triplets ' + f'($\\times10^{5}$)')

    axis = axes[10]
    set_new_ylim(axis, (0, 6.0e5))
    set_sci_yticks(axis, 5, '.1f', [0.0e5, 1.0e5, 2.0e5, 3.0e5, 4.0e5, 5.0e5, 6.0e5])
    TimeSeriesPlt.draw_ylabel(axis, 'New triplets ' + f'($\\times10^{5}$)')

    axis = axes[6]
    set_new_ylim(axis, (0, 2.5e3))
    set_sci_yticks(axis, 3, '.1f', [0.0e3, 0.5e3, 1.0e3, 1.5e3, 2.0e3, 2.5e3])
    TimeSeriesPlt.draw_ylabel(axis, 'New triplets ' + f'($\\times10^{3}$)')

    return fig, axes


def plot_sfig5():
    p, t = get_sfig5()

    fig, axes = plot_2rows5cols()
    ylim_yticks = {'Med. sci.': [(0, 100), np.arange(0, 125, 25)],
                   'Plant sci.': [(0, 25), np.arange(0, 30, 5)],
                   'Appl. biotech.': [(0, 15), np.arange(0, 17.5, 2.5)],
                   'Metab. eng.': [(0, 11), np.arange(0, 12.5, 2.5)],
                   'Pharma.': [(0, 11), np.arange(0, 12.5, 2.5)],
                   'Gen. microb.': [(0, 11), np.arange(0, 12.5, 2.5)],
                   'Immun.': [(0, 3), np.arange(0, 3.5, 0.5)],
                   'Genetic tools': [(0, 3), np.arange(0, 3.5, 0.5)],
                   'Blood-assoc.': [(0, 3), np.arange(0, 3.5, 0.5)],
                   'Others': [(0, 70), np.arange(0, 75, 15)]}

    for axis, (field, (ylim, yticks)) in zip(axes, ylim_yticks.items()):
        TimeSeriesPlt.draw_ts(axis, p[field], color='#1f77b4ff')
        TimeSeriesPlt.draw_ts(axis, t[field], color='#de4e4fff')
        TimeSeriesPlt.title_on(axis, field)
        set_new_ylim(axis, ylim)
        axis.set_yticks(yticks)
        TimeSeriesPlt.draw_ylabel(axis, 'Share (%)')
    return fig, axes


def plot_sfig6():
    omega = get_sfig6()

    colors = {
        'violet': '#c96bdf',
        'deep_violet': '#c052d9',

        'blue': '#558cfb',
        'deep_blue': '#3a7afa',

        'green': '#46ff72',
        'deep_green': '#28ff5c',

        'pink': '#fc4677',
        'deep_pink': '#fb1755',

        'orange': '#ff7a17',
        'deep_orange': '#ff6d00',
    }
    fig, axis = plt.subplots()

    icolors = iter(colors.values())
    for (N, n), rv in omega.items():
        axis.plot(rv.keys(), rv.values(), 'o', color=next(icolors), label=f'N={N}')
        axis.axhline(rv[1.0], ls='--', color=next(icolors), label=f'N={N}')
    axis.set_xticks([1, 3, 5, 7, 9], minor=True)
    axis.tick_params(labelsize=10)
    set_new_ylim(axis, [65, 130])
    axis.set_xlabel('r', fontsize=12)
    axis.set_ylabel('E[Nr, nr]/r', fontsize=12)
    legend(loc='best', fontsize=10)
    return fig, axis


def plot_sfig7():
    q = get_sfig7()
    fig, axis = PmfPlt.subplots(integrated=True)
    axis.hist(q, bins=range(1990, 2012), align='left', ec='black', fc='grey')
    axis.set_xlabel('Debut year', fontsize=10)
    axis.set_ylabel('Frequency', fontsize=10)
    return fig, axis


def plot_sfig8():
    fig: ExFigure = plt.figure(figsize=(8.268, 11.693 / 5), FigureClass=ExFigure)
    ax0: plt.Axes = fig.add_axes(PmfPlt.pos1)
    ax1: plt.Axes = fig.add_axes(PmfPlt.pos1, [(1 / 3, 'figure'), (0, 0), (0, 0), (0, 0)])
    ax2: plt.Axes = fig.add_axes(PmfPlt.pos1, [(2 / 3, 'figure'), (0, 0), (0, 0), (0, 0)])
    ax0.tick_params(axis='both', labelsize=8)
    ax1.tick_params(axis='both', labelsize=8)
    ax2.tick_params(axis='both', labelsize=8)
    draw_sfig8_slope(ax0)
    draw_sfig8_trgs(ax1)
    draw_sfig8_taus(ax2)
    return fig, (ax0, ax1, ax2)


def draw_sfig8_trgs(axis: plt.Axes):
    PmfPlt.draw_pdf(axis, get_sfig8_trgs(), 0.3, 0.52, 0.01, lc='#d16647', mc='#765749')
    set_new_ylim(axis, (0, 29))
    axis.set_yticks(np.arange(0, 31, 5))
    set_new_xlim(axis, (0.33, 0.5))
    axis.set_xticks(np.arange(0.35, 0.51, 0.05))
    axis.set_xticks(np.arange(0.33, 0.51, 0.01), minor=True)
    axis.set_xlabel('Estimated fraction of\nspecies-specific genes (~2018)', fontsize=10)
    axis.set_ylabel('Probability density', fontsize=10)


def draw_sfig8_slope(axis: plt.Axes):
    PmfPlt.draw_pdf(axis, get_sfig8_slopes(), 0.075, 0.14, 0.005, lc='#3077b7', mc='#3f4c8c')
    set_new_ylim(axis, (0, 50))
    set_new_xlim(axis, (0.06, 0.15))
    axis.set_xticks(np.arange(0.06, 0.15, 0.02))
    axis.set_xticks(np.arange(0.06, 0.16, 0.01), minor=True)
    axis.set_xlabel('Estimated fraction of\nspecies-specific gene sequences', fontsize=10)
    axis.set_ylabel('Probability density', fontsize=10)


def draw_sfig8_taus(axis: plt.Axes):
    PmfPlt.draw_pdf(axis, get_sfig8_taus(), 7, 22, 1, lc='#404040', mc='#404040')
    axis.set_ylim(-0.01, 0.15)
    set_new_xlim(axis, (0, 21))
    axis.set_xticks(np.arange(0, 21, 2))
    axis.set_xticks(np.arange(1, 21, 1), minor=True)
    axis.set_xlabel('Characteristic latent period (year)', fontsize=10)
    axis.set_ylabel('Probability density (year', fontsize=10)

    axis.axvline(6.94)
    axis.axvline(10)


def plot_sfig9():
    mtype2colors = {'paper': ['#011993', '#0096ff', '#00d0d7'],
                    'patent_gon': ['#941751', '#ea2613', '#ff8ad8']}
    wos = [False, True]
    ranks = [20, 50]

    fig, axes = plot_1row()
    for axis, wo in zip(axes, wos):
        for mtype, colors in mtype2colors.items():
            for rank, color in zip(ranks, colors):
                pareto = Pareto(mtype, rank, without_tools=wo)
                if mtype in ['paper', 'any']:
                    axis.plot(pareto.keys(), pareto.values(), color=color, lw=1.1)
                else:
                    dct0 = {k: v for k, v in pareto.items() if k <= 2015}
                    dct1 = {k: v for k, v in pareto.items() if k >= 2015}
                    axis.plot(dct0.keys(), dct0.values(), color=color, lw=1.1)
                    axis.plot(dct1.keys(), dct1.values(), color=color, lw=1.1, ls='--')
        set_new_ylim(axis, (0, 0.5))
        axis.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])
        # axis.set_yticks([0.1, 0.3, 0.5], minor=True)
        axis.set_yticklabels(['0', '10', '20', '30', '40', '50'])
        TimeSeriesPlt.draw_xlabel(axis, 'Year', fontsize=8)
        TimeSeriesPlt.draw_xticks(axis)
        axis.set_ylabel('Proportion (%)')
    return fig, axes


def plot_sfig10():
    mtype2colors = {'paper': ['#011993', '#0096ff', '#00d0d7'],
                    'patent_gon': ['#941751', '#ea2613', '#ff8ad8']}
    wos = [False, True]
    rankss = [[20, 50, -1], [10, 100, -1]]

    fig, axes = plot_1row()
    for axis, (ranks, wo) in zip(axes, product(rankss, wos)):
        for mtype, colors in mtype2colors.items():
            for rank, color in zip(ranks, colors):
                persistency = Persistency(mtype, rank, without_tools=wo)
                Fig1i.draw_lower(axis, persistency, color)
                Fig1i.polish_lower(axis)
    return fig, axes


def plot_sfig11():
    mtype2colors = {'paper': ['#011993', '#0096ff', '#00d0d7'],
                    'patent_gon': ['#941751', '#ea2613', '#ff8ad8']}
    wos = [False, True]
    ranks = [10, 100, -1]

    fig, axes = plot_1row()
    for axis, ((mtype, colors), wo) in zip(axes, product(mtype2colors.items(), wos)):
        for rank, color in zip(ranks, colors):
            persistency = Persistency(mtype, rank, without_tools=wo)
            Fig1i.draw_lower(axis, persistency, color)
            Fig1i.polish_lower(axis)
    return fig, axes
