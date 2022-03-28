"""
Make time-series of total papers/patents with hits.
"""
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
from TimeSeries import rsrc_dir
from TimeSeries.LoHL import LoHL

W_FILES = {'': f'{rsrc_dir}/pdata/total/total.csv'}


def measure_total_materials(mtype):
    """
    :return: {year -> num of materials}
    """
    min_year = 1990
    lohl = LoHL(mtype, load=True)
    return Counter(year for idx, year, *genes in lohl if min_year <= year)  # <= maxyear 는 TimeSeries.LoHL 에서 이미 처리됨


def draw_comparison(df, x, y0, y1, name):
    fig, ax0 = plt.subplots(figsize=(7.5, 7))
    ax1 = ax0.twinx()
    ax0.tick_params(axis='x', rotation=45, labelsize=15)
    ax0.tick_params(axis='y', colors='black', labelsize=15)
    ax1.tick_params(axis='y', colors='red', labelsize=15)
    ax1.spines['right'].set_color('red')

    ax0.plot(df.index, df[y0].to_numpy(), color='black', lw=2)
    ax1.plot(df.index, df[y1].to_numpy(), color='red', lw=2, ls='-')

    fig.suptitle(name, fontsize=20)
    ax0.set_xlabel(x, fontsize=20)
    ax0.set_ylabel(y0, fontsize=20, labelpad=15)
    ax1.set_ylabel(y1, rotation=270, labelpad=30, color='red', fontsize=20)
    plt.tight_layout()
    plt.show()

    return fig, (ax0, ax1)


def update():
    totals = {mtype: measure_total_materials(mtype) for mtype in LoHL.R_FILES.keys()}
    df = pd.DataFrame(totals).sort_index()
    df.to_csv(W_FILES[''])
