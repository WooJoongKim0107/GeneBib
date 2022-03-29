import numpy as np
from Plot.tools import set_new_ylim, set_sci_yticks
from Plot.plotter import TimeSeriesPlt, FitResPlt, Fig1i
from Plot.data import *


def draw_fig1i_lower(axis_lower):
    inheritances = get_fig1i_lower()
    for mtype, dct in inheritances.items():
        for rank, inheritance in dct.items():
            Fig1i.draw_lower(axis_lower, inheritance)
    Fig1i.polish_lower(axis_lower)


def draw_fig1i_upper(axes_upper):
    p, (t0, t1) = get_fig1i_upper()
    Fig1i.draw_upper(axes_upper, p, t0, t1)
    Fig1i.polish_upper(axes_upper)


def draw_fig2a(axis):
    TimeSeriesPlt.draw_ts(axis, get_fig2a().to_dict(), color='black')
    set_new_ylim(axis, (0, None))
    set_sci_yticks(axis, 3, '.1f', [0.0e3, 0.5e3, 1.0e3, 1.5e3, 2.0e3])
    TimeSeriesPlt.draw_ylabel(axis, 'New genes ' + f'($\\times10^{3}$)')


def draw_fig2b(axes):
    ylim_yticks = {'Med. sci.': [(0, 100), np.arange(0, 125, 25)],
                   'Metab. eng.': [(0, 11), np.arange(0, 12.5, 2.5)],
                   'Plant sci.': [(0, 25), np.arange(0, 30, 5)]}

    p1x = get_fig2b('paper')
    t1x = get_fig2b('patent_gon')
    for axis, (field, (ylim, yticks)) in zip(axes, ylim_yticks.items()):
        TimeSeriesPlt.draw_ts(axis, p1x.loc[field].to_dict(), color='#1f77b4ff')
        TimeSeriesPlt.draw_ts(axis, t1x.loc[field].to_dict(), color='#de4e4fff')
        TimeSeriesPlt.title_on(axis, field)
        set_new_ylim(axis, ylim)
        axis.set_yticks(yticks)
        TimeSeriesPlt.draw_ylabel(axis, 'Share (%)')


def draw_fig2c(axis):
    TimeSeriesPlt.draw_ts(axis, get_fig2c().to_dict(), color='black')
    set_new_ylim(axis, (0, 2.0e5))
    set_sci_yticks(axis, 5, '.1f', [0.0e5, 0.5e5, 1.0e5, 1.5e5, 2.0e5])
    TimeSeriesPlt.draw_ylabel(axis, 'New pairs of genes ' + f'($\\times10^{5}$)')


def draw_fig2d(axes):
    title_periods = {'beta-gal': (r'$\beta$-Galactosidase', (1990, 1997)),
                     'GFP': ('GFP', (1998, 2014)),
                     'Cas9': ('', (2016, 2018))}

    for axis, (gene, (title, period)) in zip(axes, title_periods.items()):
        _draw_fig2d(axis, gene, title, period, color='black', area_color='#F6C958')
    else:
        _draw_fig2d(axis, 'mTOR', '', (), zorder=1, color='#3B3838', lw=1, ls='--', dashes=(3, 1))


def _draw_fig2d(axis, gene, title, period, area_color='grey', **kwargs):
    TimeSeriesPlt.draw_ts(axis, get_fig2d().loc[gene].to_dict(), **kwargs)
    set_new_ylim(axis, (0, 0.65))
    TimeSeriesPlt.draw_ylabel(axis, 'Share (%)')
    if period:
        TimeSeriesPlt.fill_betweenx(axis, period, color=area_color)
    if title:
        TimeSeriesPlt.title_on(axis, title)


def draw_fig2e_fitting_results(axes, tau, beta):
    by_tar, by_est = get_fig2e_by(tau, beta)
    dbdt_tar, dbdt_est = get_fig2e_dbdt(tau, beta)
    FitResPlt.draw_fig2e_fitting_results(axes, [by_tar, by_est], [dbdt_tar, dbdt_est])
