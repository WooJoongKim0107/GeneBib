"""
Classify the time-series pattern
"""
import pickle
from more_itertools import convolve
from TimeSeries import rsrc_dir, safe_update
from TimeSeries.LoHL import LoHL
from TimeSeries.time_series import GYH

R_FILE = {
    'paper': f'{rsrc_dir}/pdata/time_series/gyh_paper_1.pkl',
    'patent_gon': f'{rsrc_dir}/pdata/time_series/gyh_patent_gon_1.pkl',
    'any': f'{rsrc_dir}/pdata/time_series/gyh_any_1.pkl',
}

W_FILE = {
    'paper': f'{rsrc_dir}/pdata/pattern/pattern_paper.pkl',
    'patent_gon': f'{rsrc_dir}/pdata/pattern/pattern_patent_gon.pkl',
    'any': f'{rsrc_dir}/pdata/pattern/pattern_any.pkl',
}


class Patterns(dict):
    """
    Patterns: dict, {gene -> pattern}  # Time-series patterns of genes with respect to paper hits if mtype='paper'
    """
    R_FILE = R_FILE
    W_FILE = W_FILE

    def __init__(self, mtype, load=True):
        self.mtype = mtype
        if load:
            super().__init__(self.load(mtype))
        else:
            gyh = _Patterns.load_gyh_to_categorize(mtype)
            super().__init__((gene, _Patterns.categorize(hits, mtype)) for gene, hits in gyh.items())

    def dump(self):
        with open(self.W_FILE[self.mtype], 'wb') as file:
            pickle.dump(dict(self), file)

    @classmethod
    def load(cls, mtype):
        with open(cls.W_FILE[mtype], 'rb') as file:
            return pickle.load(file)


class _Patterns:
    """Class to find the time-series pattern"""
    END_YEARS = LoHL.END_YEARS

    @staticmethod
    def load_gyh_to_categorize(mtype):
        if mtype in ('paper', 'any'):
            return {gene: hits for gene, hits in GYH(mtype, n=1).items()
                    if (len(hits) >= 5) and (sum(hits.values()) >= 100)}

        elif mtype in ('patent', 'patent_gon'):
            return {gene: hits for gene, hits in GYH(mtype, n=1).items()
                    if len(hits) >= 5}

        else:
            raise ValueError(f"Cannot recognize {mtype = }")

    @staticmethod
    def fill(hits, end_year):
        fhits = {year: hits.get(year, 0) for year in range(min(hits), end_year+1)}
        return fhits

    @staticmethod
    def windowed(fhits, length=3):
        """
        :param fhits: filled_hits, fill(hits), dict {year -> # hit}
        :param length: window length
        :return: windowed sum of filled_hits or wfhits,
            dict {year -> fhits.get(year) + fhits.get(year-1) + fhits.get(year-2)}  if length==3
        """
        kernel = [1]*length
        values = convolve(fhits.values(), kernel)
        wfhits = dict(zip(fhits, values))
        return wfhits

    @staticmethod
    def prime(wfhits):
        itr = reversed(wfhits)  # reversed to find the last occurrence of maximum hit
        return max(itr, key=wfhits.__getitem__)

    @staticmethod
    def windowed_delta(fhits, length=3):
        kernel = [1]+[0]*(length-1)+[-1]
        values = convolve(fhits.values(), kernel)
        wfdhits = dict(zip(fhits, values))
        return wfdhits

    @classmethod
    def nadir(cls, wfhits, prime):
        itr = (y for y in reversed(wfhits) if y >= prime)
        # 1) reversed to find the last occurrence of maximum hit
        # 2) y >= prime to find the nadir between [nadir, end year]
        return min(itr, key=wfhits.__getitem__)

    @classmethod
    def categorize(cls, hits, mtype):
        end_year = cls.END_YEARS[mtype]
        fhits = cls.fill(hits, end_year)
        wfhits = cls.windowed(fhits, length=3)
        prime = cls.prime(wfhits)

        if mtype in ('paper', 'any'):
            return cls._p_cat(fhits, wfhits, prime, end_year, wl=3)
        elif mtype in ('patent', 'patent_gon'):
            return cls._t_cat(prime, end_year)
        else:
            raise ValueError(f"Cannot recognize {mtype = }")

    @classmethod
    def _p_cat(cls, fhits, wfhits, prime, end_year, wl=3):
        if prime == end_year:
            # Growing
            delta_prime = cls.prime(cls.windowed_delta(fhits, length=wl))
            if delta_prime == end_year:
                return 'Climbing'
            else:
                return 'Growth-slowed'
        else:
            # Non-growing
            if wfhits.get(end_year, 0) / wfhits[prime] <= 0.5:
                return 'Falloff'
            else:
                nadir = cls.nadir(wfhits, prime)
                if wfhits[nadir] / wfhits[prime] <= 0.5:
                    return 'Rebound'
                else:
                    return 'Sustained'

    @classmethod
    def _t_cat(cls, prime, end_year):
        if prime == end_year:
            return 'Growing'
        else:
            return 'Non-growing'


def update():
    for mtype in ('paper', 'patent_gon', 'any'):
        safe_update(Patterns, dict(mtype=mtype, load=True), dict(mtype=mtype, load=False))
