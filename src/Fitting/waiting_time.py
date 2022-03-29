"""
This code summarize our measurements on waiting time (time required for debut after sequencing)
 and show the probability distribution and cumulative probability distribution of waiting time.
"""
import pickle
from itertools import accumulate, groupby
from collections import Counter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from NestedDict.klv import KLV
from TimeSeries import rsrc_dir
from TimeSeries.debut import Debuts

R_FILES = {'': f'{rsrc_dir}/data/waiting_times.csv'}

W_FILES = {
    'pdf': f'{rsrc_dir}/pdata/waiting_time/pdf.pkl',
    'ccdf': f'{rsrc_dir}/pdata/waiting_time/ccdf.pkl',
}


class PrD(dict):
    """
    pr_d = PrD()
    pr_d[deb] = Probability of a random gene has debuted in 'deb'
    """
    def __init__(self):
        data = self.calc(Measurements.load())
        super().__init__(data)

    @staticmethod
    def count(measurement):
        counter = Counter(deb for seq, deb in measurement if deb < 2019)
        total = sum(counter.values())
        return {deb: counter.get(deb, 0) / total for deb in range(1939, 2019)}

    @classmethod
    def calc(cls, measurement):
        """
        Our measurement is roughly as follows:

            measurements = []

            for interval in [range(i, i+5) for i in range(1990, 2019, 5)]:
                50_rnd_genes = randomly choose 50 genes that debuted during 'interval'

                for gene in 50_rnd_genes:
                    try:
                        seq_year = find the year when the gene has been sequenced for the first time
                        measurements.append([deb_year, seq_year, 'Success'])  # debut year is already known
                    except Exception as e:
                        measurements.append([deb_year, 0, e])

        Since genes are not randomly chosen among the whole set of genes, Pr(Deb=1990) should be calculated as:

            numerator = prob of that a random gene has debuted during 1990-1994 among all genes.
            denominator = fraction of genes that has debuted during 1990-1994 among measurements
            frac = fraction of genes that has debuted in 1990 among measurements
            Pr(Deb=1990) = frac*numerator/denominator
        """
        debuts = Debuts('any', n=1).counts
        total = sum(debuts[t] for t in range(1990, 2019))
        _prd = cls.count(measurement)

        prd = {}
        for i in range(1990, 2019, 5):
            num = sum(debuts.get(d, 0) for d in range(i, i+5)) / total
            den = sum(_prd.get(d, 0) for d in range(i, i+5))
            for t in range(i, i+5):
                if t in _prd:
                    prd[t] = _prd[t] * num / den
        return prd


class PrSD(KLV):
    """
    pr_sd = PrSD()
    pr_sd[deb][seq] = Probability of a random gene that has debuted in 'deb' has sequenced in 'seq'
    """
    def __init__(self):
        data = self.calc(Measurements.load())
        super().__init__(data)

    @staticmethod
    def count(measurement):
        counter = Counter(seq for seq, deb in measurement if deb < 2019)
        total = sum(counter.values())
        return {seq: counter.get(seq, 0) / total for seq in range(1939, 2019)}

    @classmethod
    def calc(cls, measurement):
        x = sorted(measurement, key=lambda seq_deb: seq_deb[1])
        pr_sd = {deb: cls.count(v) for deb, v in groupby(x, lambda seq_deb: seq_deb[1])}
        return pr_sd


class Measurements:
    R_FILES = R_FILES['']

    @classmethod
    def load(cls):
        temp = pd.read_csv(cls.R_FILES, index_col=0)
        return [(seq, deb) for seq, deb, stat, entry in temp.itertuples(index=False) if stat == 'Success']


class WaitingTimes(KLV):
    # noinspection PyPep8
    """
    wts = WaitingTimes()
    wts[(1995, 2000)] = {t: prob of a random gene that has sequenced during 1995-1999 debuts t year after its sequencing}
    """
    W_FILES = W_FILES['pdf']
    INTERVALS = [(1980, 1995), (1995, 2000), (2000, 2005), (2005, 2016), (1980, 2016)]
    # 1980 (2016) is the minimum (maximum) value observed for the year of sequencing

    def __init__(self, load=True):
        if load:
            data = self.load()
        else:
            data = self.calc(PrSD(), PrD(), self.INTERVALS)
        super().__init__(data)

    @classmethod
    def calc(cls, pr_sd, prd, intervals):
        return {intv: {wt: pr for wt in range(2019) if (pr := cls._calc(pr_sd, prd, wt, intv))} for intv in intervals}

    @staticmethod
    def _calc(pr_sd, prd, wt, intv):
        den = sum(sum(pr_sd[deb][seq] * prd[deb] for deb in pr_sd.keys() if seq <= deb) for seq in range(*intv))
        if den == 0:
            return None
        valid_seqs = (seq for seq in range(*intv) if (seq + wt < 2019) and (seq + wt in pr_sd))
        num = sum(pr_sd[seq + wt][seq] * prd[seq + wt] for seq in valid_seqs)
        return num / den

    def dump(self):
        with open(self.W_FILES, 'wb') as file:
            pickle.dump(dict(self), file)

    @classmethod
    def load(cls):
        with open(cls.W_FILES, 'rb') as file:
            return pickle.load(file)


class CCWaitingTimes(KLV):
    """
    c_wts = CCWaitingTimes()
    c_wts[(1995, 2000)] = {t: prob of a random gene that has sequenced during 1995-1999
                            debuts more than or equal to t year after its sequencing}
                        = ccdf(WaitingTimes()[(1995, 2000)])
    """
    W_FILES = W_FILES['ccdf']

    def __init__(self, load=True):
        if load:
            data = self.load()
        else:
            wts = WaitingTimes(load=False)
            data = {intv: ccdf(prs) for intv, prs in wts.items()}
        super().__init__(data)

    def dump(self):
        with open(self.W_FILES, 'wb') as file:
            pickle.dump(dict(self), file)

    @classmethod
    def load(cls):
        with open(cls.W_FILES, 'rb') as file:
            return pickle.load(file)


def ccdf(pdf):
    counter = pdf.copy()
    ks_dct = dict(sorted(counter.items(), reverse=True))  # ks: keys sorted
    aks_dct = {x: r for x, r in zip(ks_dct.keys(), accumulate(ks_dct.values()))}
    total = sum(counter.values())
    return {x: r / total for x, r in aks_dct.items()}


def most_close(x, dct):
    return min(dct, key=lambda y: abs(y-x))


def fitting_range(interval):
    """
    ini, fin = {(1997, 2000): (5, 15), (2000, 2003): (5, 9),
                (2003, 2014): (3, 12), (1997, 2014): (5, 11)}[interval]
    """
    ini, fin = {(1997, 2000): (0, 17), (2000, 2003): (0, 12),
                (2003, 2014): (0, 9), (1997, 2014): (0, 12)}[interval]
    return ini, fin


def naive_initial(prob):
    ini, fin, tau = 0, 24, 10
    med = most_close(ini+fin//2, prob)
    return np.array([prob[med]/np.exp(-med/tau), tau])


def tau_fitted(prob):
    def cost(para):
        a, tau = para
        x = np.array([k for k in prob.keys() if ini <= k <= fin])
        y = np.array([prob[k] for k in x])
        y_est = a*np.exp(-x/tau)
        return abs(y-y_est).sum()/y.sum()

    ini, fin = 0, 24
    a, tau = minimize(cost, naive_initial(prob), method='SLSQP')['x']
    print(a, tau)
    x = np.arange(ini, fin + 1)
    y = a*np.exp(-x/tau)
    return x, y


def main():
    WaitingTimes(load=False).dump()
    CCWaitingTimes(load=False).dump()
    c_wts = CCWaitingTimes()
    for intv, c_prs in c_wts.items():
        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(7, 7))
        for axis in axes[:, 1]:
            axis.semilogx()
        for axis in axes[1, :]:
            axis.semilogy()
        for axis in axes.flatten():
            axis.plot(c_prs.keys(), c_prs.values(), 'ko')
            axis.grid('both')
        fig.suptitle(f'{intv[0]}'+u'\u2013'+f'{intv[1]}')
        fig.show()
    tau_fitted(c_wts[(1980, 2016)])


if __name__ == '__main__':
    main()
