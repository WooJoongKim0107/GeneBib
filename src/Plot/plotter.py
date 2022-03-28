from Plot.tools import *


def A4_row_subplots(locator):
    fig = plt.figure(figsize=(8.268, 11.693/6), FigureClass=ExFigure)
    for i in range(4):
        fig.add_axes(locator, [(i/4, 'fig'), (0, 'fig'), (0, 'fig'), (0, 'fig')])
    return fig, fig.axes


class TimeSeriesPlt:
    one_sided_pos = [(0.565, 'inches'), (0.470, 'inches'), (1.35, 'inches'), (1.35, 'inches')]
    two_sided_pos = [(0.4150, 'inches'), (0.5050, 'inches'), (1.2450, 'inches'), (1.2450, 'inches')]

    @classmethod
    def subplots(cls, one_sided=True):
        fig: ExFigure = plt.figure(figsize=(8.268/4, 11.693/6), FigureClass=ExFigure)
        axis: plt.Axes = fig.add_axes(cls.one_sided_pos if one_sided else cls.two_sided_pos)
        axis.tick_params(axis='both', labelsize=8)
        return fig, axis

    @classmethod
    def draw_ts(cls, axis, data, **kwargs):
        axis.plot(data.keys(), data.values(), **kwargs)
        cls.draw_xlabel(axis, 'Year')
        cls.draw_xticks(axis)

    @staticmethod
    def title_on(axis, title):
        axis.text(x=0.5, y=0.95, s=title, ha='center', va='top', transform=axis.transAxes, size=10)

    @staticmethod
    def y_ticklabel_as_sci(axis, exponent, format_, yticks=None):
        set_sci_yticks(axis, exponent, format_, yticks)
        draw_exponent(axis, exponent)

    @staticmethod
    def draw_ylabel(axis: plt.Axes, label, left=True, **kwargs):
        if not left:
            axis.yaxis.set_label_position('right')
            axis.yaxis.set_tick_params(which='both', right=True, labelright=True, left=False, labelleft=False)
        kw = dict(fontsize=10, rotation=90 if left else 270, va='bottom')
        kw.update(kwargs)
        axis.set_ylabel(label, **kw)

    @staticmethod
    def fill_betweenx(axis, xs, w=1, ha=0, **kwargs):
        kwargs.setdefault('color', 'grey')
        x0, x1 = xs + np.array([-w, +w])*(ha+1)/2
        axis.fill_betweenx(axis.get_ylim(), x0, x1, zorder=0, **kwargs)

    @staticmethod
    def draw_xlabel(axis: plt.Axes, label, **kwargs):
        kwargs.setdefault('fontsize', 10)
        axis.set_xlabel(label, **kwargs)

    @classmethod
    def draw_xticks(cls, axis, ticks=(1990, 2000, 2010, 2018), **kwargs):
        set_new_xlim(axis, [ticks[0], ticks[-1]])
        axis.set_xticks(ticks)
        cls._draw_xticklabels(axis, ticks, pad=0, **kwargs)

    @staticmethod
    def _draw_xticklabels(axis, ticks, pad, **kwargs):
        kw = dict(fontsize=8, rotation=45, rotation_mode='anchor', ha='right', va='top')
        kw.update(kwargs)
        axis.set_xticklabels(ticks, **kw)
        axis.tick_params(axis='x', pad=pad)


class HeatMapPlt:
    heatmap_pos = [(1.5, 'inch'), (-0.39, 'inch', 1.0, 'fig'), (4.66, 'inch'), (2.33, 'inch')]

    @classmethod
    def plot_heatmap(cls, mat, cmap=None):
        fig, (axis, caxis) = cls.subplots()
        im = cls.draw_heatmap(axis, mat, cmap=cmap)
        cls.draw_colorbar(fig, im, axis, caxis)
        cls.draw_rectangles(axis, (9, 0.8), (12, 0.7), (19, 1.0))
        return fig, (axis, caxis)

    @classmethod
    def subplots(cls, heatmap_pos=None, colorbar_pos=None):
        fig: ExFigure = plt.figure(figsize=(8.268, 11.693/2), FigureClass=ExFigure)
        axis0 = fig.add_axes(cls.heatmap_pos if heatmap_pos is None else heatmap_pos, va=1)
        caxis = fig.add_axes(cls.colorbar_pos(axis0) if colorbar_pos is None else colorbar_pos, ha=1, va=0)
        return fig, (axis0, caxis)

    @classmethod
    def draw_heatmap(cls, axis: plt.Axes, x, cmap=None):
        im = axis.matshow(x, cmap='Spectral' if cmap is None else cmap)
        cls.draw_xaxis(axis)
        cls.draw_yaxis(axis)
        cls.draw_values(axis, x)
        return im

    @classmethod
    def draw_colorbar(cls, fig, im, axis, caxis: plt.Axes, on_left=True):
        fig.colorbar(im, ax=axis, cax=caxis)
        caxis.tick_params(labelsize=8)
        cls.caxis_label(caxis, on_left=on_left)

    @classmethod
    def draw_rectangles(cls, axis, *taubetas):
        for tau, beta in taubetas:
            x, y = tau - 0.5, (beta - 0.15) * 10
            rectangle = plt.Rectangle((x, y), height=1, width=1, fc='none', ec='white')
            axis.add_patch(rectangle)

    @staticmethod
    def draw_values(axis, x):
        for (row, col), val in np.ndenumerate(x):
            if val <= 0.05:
                axis.text(col, row, f'{val:.2f}', va='center', ha='center', fontsize=7, color='white')
            if row == 0 or col == 0:
                axis.text(col, row, f'{val:.2f}', va='center', ha='center', fontsize=7, color='black')

    @staticmethod
    def caxis_label(caxis, on_left=True):
        caxis.yaxis.set_label_position('left' if on_left else 'right')
        caxis.xaxis.set_tick_params(bottom=False, labelbottom=False)
        caxis.yaxis.set_tick_params(labelsize=8, left=on_left, labelleft=on_left,
                                    right=(not on_left), labelright=(not on_left))
        caxis.yaxis.set_label_text('Relative error', fontsize=9, va='bottom', rotation=90 if on_left else 270)

    @classmethod
    def draw_xaxis(cls, axis):
        cls.draw_xticks(axis)
        cls.draw_xlabels(axis)

    @classmethod
    def draw_yaxis(cls, axis):
        cls.draw_yticks(axis)
        cls.draw_ylabels(axis)

    @staticmethod
    def draw_xticks(axis):
        axis.xaxis.set_tick_params(which='major', bottom=False, labelbottom=False, top=False, labeltop=True, size=2)
        axis.xaxis.set_tick_params(which='minor', bottom=False, labelbottom=False, top=True, labeltop=False, size=5)
        axis.xaxis.set_ticks(range(20), minor=False)
        axis.xaxis.set_ticks(np.arange(-0.5, 20, 0.5), minor=True)
        axis.xaxis.set_ticklabels([f'{i:.0f}' for i in range(20)], fontsize=8)

    @staticmethod
    def draw_xlabels(axis):
        axis.xaxis.set_label_position('top')
        axis.xaxis.set_label_text('Characteristic latent period (year)', fontsize=10)

    @staticmethod
    def draw_yticks(axis):
        axis.yaxis.set_tick_params(which='major', left=False, labelleft=True, right=False, labelright=False, size=2)
        axis.yaxis.set_tick_params(which='minor', left=True, labelleft=False, right=False, labelright=False, size=5)
        axis.yaxis.set_ticks(range(10), minor=False)
        axis.yaxis.set_ticks(np.arange(-0.5, 10, 0.5), minor=True)
        axis.yaxis.set_ticklabels([f'{(i+1)/10:.1f}' for i in range(10)], fontsize=8)

    @staticmethod
    def draw_ylabels(axis):
        axis.yaxis.set_label_position('left')
        axis.yaxis.set_label_text('Proportion of genes in spotlight', fontsize=10)

    @staticmethod
    def colorbar_pos(ax):
        return [(0, ax, -0.6225, 'inch'), (0.5, ax), (0.7 / 20, ax), (0.7, ax)]


class FitResPlt:
    tar_kws = dict(zorder=1, color='grey', marker='o', mfc='white', markevery=2, ms=2.7, mew=1.0, ls='')
    est_kws = dict(zorder=0, color='black', lw=1.25)

    @classmethod
    def draw_fig2e_fitting_results(cls, axes, bys, dbdts):
        cls.draw_b_of_y(axes[0], bys[0], **cls.tar_kws)
        cls.draw_b_of_y(axes[0], bys[1], **cls.est_kws)
        cls.draw_db_dt(axes[1], dbdts[0], **cls.tar_kws)
        cls.draw_db_dt(axes[1], dbdts[1], **cls.est_kws)

    @staticmethod
    def draw_b_of_y(axis: plt.Axes, dct, **kwargs):
        axis.plot(dct.keys(), dct.values(), **kwargs)
        axis.tick_params(size=2, pad=1)

        set_new_xlim(axis, (0, None))  # 위치 바꿔야 제대로 작동할지도 모름
        set_sci_xticks(axis, 5, '.1f')
        axis.set_xticklabels(axis.get_xticklabels(), ha='center', fontsize=7)
        axis.xaxis.set_label_text('# of sequences ($\\times10^5$)', fontsize=7)

        axis.set_ylim(0.3e4, 6.5e4)
        set_sci_yticks(axis, 4, '.1f', [0.3e4, 1.5e4, 3.0e4, 4.5e4, 6.0e4])
        axis.set_yticklabels(['0.0', '1.5', '3.0', '4.5', '6.0'], fontsize=7)
        axis.set_ylabel('# of genes ($\\times10^4$)', fontsize=7, labelpad=2)

    @staticmethod
    def draw_db_dt(axis: plt.Axes, dct, **kwargs):
        axis.plot(dct.keys(), dct.values(), **kwargs)
        axis.tick_params(size=2, pad=1)

        TimeSeriesPlt.draw_xlabel(axis, 'Year', fontsize=7)
        TimeSeriesPlt.draw_xticks(axis, fontsize=7)

        set_new_ylim(axis, (0, None))
        set_sci_yticks(axis, 3, '.1f', [0.0e3, 0.5e3, 1.0e3, 1.5e3, 2.0e3])
        axis.set_yticklabels(axis.get_yticklabels(), fontsize=7)
        TimeSeriesPlt.draw_ylabel(axis, 'New genes ($\\times10^3$)', fontsize=7, labelpad=2)

    @staticmethod
    def draw_boxes(fig, axis):
        ax0 = fig.add_axes([
            (0.0, axis, -0.1, 'inch'),
            (0.0, axis, -0.17, 'inch'),
            (0.7874, 'inch'),
            (0.7874, 'inch')], va=1)
        ax1 = fig.add_axes([(1.0, ax0, 0.5, 'inch'), (0.0, ax0), (1, ax0), (1, ax0)])
        ax2 = fig.add_axes([(1.0, ax1, 0.75, 'inch'), (0.0, ax0), (1, ax0), (1, ax0)])
        ax3 = fig.add_axes([(1.0, ax2, 0.5, 'inch'), (0.0, ax0), (1, ax0), (1, ax0)])
        ax4 = fig.add_axes([(1.0, axis, 0.6, 'inch'), (0.0, axis, 0.05, 'inch'), (1, ax0), (1, ax0)])
        ax5 = fig.add_axes([(0.0, ax4), (1.0, ax4, 0.5, 'inch'), (1, ax0), (1, ax0)])
        return [ax0, ax1, ax2, ax3, ax5, ax4]  # ..., ax3, ax5, ax4] <-- intended


class PmfPlt:
    pos0 = [(0.565, 'inches'), (0.470, 'inches'), (1.5, 'inches'), (1.5, 'inches')]
    pos1 = [(0.565, 'inches'), (0.470, 'inches'), (1.9, 'inches'), (1.5, 'inches')]

    kws_line = dict(zorder=0, color='black', lw=1.25)
    kws_marker = dict(zorder=1, color='grey', marker='o', mfc='white', ms=3.23, mew=1.24, ls='')

    @classmethod
    def subplots(cls, integrated=False):
        fig: ExFigure = plt.figure(figsize=(8.268/3, 11.693/5), FigureClass=ExFigure)
        axis: plt.Axes = fig.add_axes(cls.pos1 if integrated else cls.pos0)
        axis.tick_params(axis='both', labelsize=8)
        return fig, axis

    @staticmethod
    def draw_pmf(ax: plt.Axes, x, bins):
        ax.hist(x, bins, weights=[1/len(x)]*len(x), facecolor='grey', edgecolor='black')

    @classmethod
    def draw_pdf(cls, ax, x, start, stop, step, lc='black', mc='grey'):
        centers = np.arange(start, stop, step)
        counts, _ = np.histogram(x, centers-step/2, density=True)

        ini, *_, fin = (i for i, c in enumerate(counts) if c)
        inner = slice(ini-1, fin+2)
        outer = slice(ini-2, fin+3)

        ax.plot(centers[inner], counts[inner], **{**cls.kws_line, 'color': lc})
        ax.plot(centers[inner], counts[inner], **{**cls.kws_marker, 'color': mc})

        ax.set_xticks(centers[outer], minor=True)
        ax.set_xticks(centers[outer][1::2])
