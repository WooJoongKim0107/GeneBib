from collections import deque
from more_itertools import tail
import numpy as np
from NestedDict.klv import transpose
from TimeSeries.LoHL import LoHL
from TimeSeries.time_series import YGH, GYH


def isover(xy, a=1, r=1):
    return xy[1] > a*xy[0]**r


def calc_gth(gyh):
    """gth: dict, {gene -> total number of hits}"""
    return {gene: sum(yh.values()) for gene, yh in gyh.items()}


def get_gyh_within(mtype, ini, fin):
    original = LoHL.END_YEARS[mtype]
    if fin <= original:
        ygh = YGH(mtype)
        return transpose({y: gh for y, gh in ygh.items() if ini <= y <= fin})
    else:
        return GYH.init_with_endyear(mtype, n=1, endyear=fin)


def coordinatize(gth_paper, gth_patent):
    """:return: dict, {gene -> point in (total paper hit, total patent hit) coordinate"""
    genes = gth_paper.keys() & gth_patent.keys()
    return {gene: (gth_paper[gene], gth_patent[gene]) for gene in genes}


def log_binned_median(xys, n=30):
    # next(iter(xys))[0] == min(x), next(tail(1, xys))[0] == max(x)
    bins = np.geomspace(next(iter(xys))[0], next(tail(1, xys))[0], n+1)
    binned_y = binning(xys, bins)
    return bins, [np.median(by) if by else None for by in binned_y]


def binning(xys, bins):
    xs, ys = zip(*xys)
    digits = np.digitize(xs, bins=bins)
    binned = deque(deque() for _ in range(len(bins)+1))
    for digit, y in zip(digits, ys):
        binned[digit].append(y)
    return popleft_and_merge_last_two(binned)


def popleft_and_merge_last_two(dq: deque):
    if dq.popleft():
        raise ValueError()
    dq[-1] = dq[-2] + dq.pop()
    return dq
