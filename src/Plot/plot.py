from more_itertools import grouper
from Plot.plotter import A4_row_subplots, HeatMapPlt
from Plot.draw import *
from TimeSeries import base_dir

W_FILES = {
    'fig1i': f'{base_dir}/plots/fig1i.svg',
    'row1': f'{base_dir}/plots/row1.svg',
    'row2': f'{base_dir}/plots/row2.svg',
    'row3': f'{base_dir}/plots/row3.svg',
}


# This function produces Fig. 1i and all the other functions will produce Fig. 2
def plot_fig1i():
    fig, (axes_upper, axis_lower) = Fig1i.subplots()
    draw_fig1i_upper(axes_upper)
    draw_fig1i_lower(axis_lower)
    return fig, (axes_upper, axis_lower)


def plot_first_row():
    fig, axes = A4_row_subplots(TimeSeriesPlt.one_sided_pos)
    draw_fig2a(axes[0])
    draw_fig2b(axes[1:])
    return fig, axes


def plot_second_row():
    fig, axes = A4_row_subplots(TimeSeriesPlt.one_sided_pos)
    draw_fig2c(axes[0])
    draw_fig2d(axes[1:])
    return fig, fig.axes


def plot_middle():
    fig, (axis, cax) = HeatMapPlt.plot_heatmap(get_fig2e_chi1_matrix().values)
    axes = FitResPlt.draw_boxes(fig, axis)
    for axs, (tau, beta) in zip(grouper(axes, 2), [(9, 0.8), (12, 0.7), (19, 1.0)]):
        draw_fig2e_fitting_results(axs, tau, beta)

    axes[0].set_xticks([0.0e5, 1.0e5, 2.0e5, 3.0e5])
    axes[0].set_xticklabels(['0.0', '1.0', '2.0', '3.0'])
    axes[2].set_xticks([0.0e5, 1.0e5, 2.0e5])
    axes[2].set_xticklabels(['0.0', '1.0', '2.0'])
    axes[4].set_xticks([0.0e5, 1.0e5, 2.0e5])
    axes[4].set_xticklabels(['0.0', '1.0', '2.0'])
    set_new_ylim(axes[1], (0, 2.2e3))
    return fig, (axis, cax), axes


def main():
    fig0, _ = plot_fig1i()
    fig0.savefig(W_FILES['fig1i'], format='svg')

    fig1, axes1 = plot_first_row()
    fig1.savefig(W_FILES['row1'], format='svg')

    fig2, axes2 = plot_second_row()
    fig2.savefig(W_FILES['row2'], format='svg')

    fig3, (axis, cax), axes3 = plot_middle()
    fig3.savefig(W_FILES['row3'], format='svg')
