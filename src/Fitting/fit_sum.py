"""
Summarize the fitting results by measuring
 1) slope: the fraction of sequences which are taxonomically-restricted among all genes
 2) TRG: the fraction of taxonomically-restricted genes (TRG) among all genes found until 2018
 3) TDG: the fraction of taxonomically-dispersed genes (TDG) found until 1997 and 2000 among TDGs found until 2018
 4) bt & dbdt: the model estimation of the time-series (and its time-difference) of debuted genes each year
 5) chi1: the value of cost function used for fitting
"""
import pickle
import numpy as np
from NestedDict.klv import KLV
from TimeSeries import rsrc_dir
from Fitting.data_preparation import t2y
from Fitting.fit_res import FitRes
from Fitting.data_preparation import bt_estimation, dbdt_estimation
from Fitting.apparent_TRGs import estimated


W_FILES = {
    'slope': f'{rsrc_dir}/pdata/fit_sum/slope.pkl',
    'TRG': f'{rsrc_dir}/pdata/fit_sum/TRG.pkl',
    'TDG': f'{rsrc_dir}/pdata/fit_sum/TDG.pkl',
    'dbdt': f'{rsrc_dir}/pdata/fit_sum/dbdt.pkl',
    'bt': f'{rsrc_dir}/pdata/fit_sum/bt.pkl',
    'yt': f'{rsrc_dir}/pdata/fit_sum/yt.pkl',
    'chi1': f'{rsrc_dir}/pdata/fit_sum/chi1.pkl',
}


class Slopes(KLV):
    R_FILES = FitRes.W_FILES
    W_FILES = W_FILES['slope']

    def __init__(self, load=True):
        if load:
            data = self.load()
        else:
            data = KLV.from_fitems([taubeta, sic[0]] for taubeta, sic in FitRes().sic.fitems())
        super().__init__(data)

    def dump(self):
        w_path = self.W_FILES
        with open(w_path, 'wb') as file:
            pickle.dump(dict(self), file)

    @classmethod
    def load(cls):
        w_path = cls.W_FILES
        with open(w_path, 'rb') as file:
            return pickle.load(file)


class TRGs(KLV):
    R_FILES = FitRes.W_FILES
    W_FILES = W_FILES['TRG']

    def __init__(self, load=True, apparent=True):
        if load:
            data = self.load()
        else:
            func = apparent_TRGs if apparent else real_TRGs
            data = KLV.from_fitems([taubeta, func(*taubeta, *sic)] for taubeta, sic in FitRes().sic.fitems())
        super().__init__(data)

    def dump(self):
        w_path = self.W_FILES
        with open(w_path, 'wb') as file:
            pickle.dump(dict(self), file)

    @classmethod
    def load(cls):
        w_path = cls.W_FILES
        with open(w_path, 'rb') as file:
            return pickle.load(file)


class TDGs(KLV):
    R_FILES = FitRes.W_FILES
    W_FILES = W_FILES['TDG']

    def __init__(self, load=True):
        if load:
            data = self.load()
        else:
            data = KLV.from_fitems([taubeta, studied_TDGs(*taubeta, *sic)] for taubeta, sic in FitRes().sic.fitems())
        super().__init__(data)

    def dump(self):
        w_path = self.W_FILES
        with open(w_path, 'wb') as file:
            pickle.dump(dict(self), file)

    @classmethod
    def load(cls):
        w_path = cls.W_FILES
        with open(w_path, 'rb') as file:
            return pickle.load(file)


class DBDTs(KLV):
    R_FILES = FitRes.W_FILES
    W_FILES = W_FILES['dbdt']

    def __init__(self, load=True):
        if load:
            data = self.load()
        else:
            data = KLV.from_fitems([taubeta, dbdt_estimation(*taubeta, s, i)]
                                   for taubeta, (s, i, c) in FitRes().sic.fitems())
        super().__init__(data)

    def dump(self):
        w_path = self.W_FILES
        with open(w_path, 'wb') as file:
            pickle.dump(dict(self), file)

    @classmethod
    def load(cls):
        w_path = cls.W_FILES
        with open(w_path, 'rb') as file:
            return pickle.load(file)


class BTs(KLV):
    R_FILES = FitRes.W_FILES
    W_FILES = W_FILES['bt']

    def __init__(self, load=True):
        if load:
            data = self.load()
        else:
            data = KLV.from_fitems([taubeta, bt_estimation(*taubeta, *sic)] for taubeta, sic in FitRes().sic.fitems())
        super().__init__(data)

    def dump(self):
        w_path = self.W_FILES
        with open(w_path, 'wb') as file:
            pickle.dump(dict(self), file)

    @classmethod
    def load(cls):
        w_path = cls.W_FILES
        with open(w_path, 'rb') as file:
            return pickle.load(file)


class YTs(KLV):
    R_FILES = FitRes.W_FILES
    W_FILES = W_FILES['yt']

    def __init__(self, load=True):
        if load:
            data = self.load()
        else:
            data = KLV.from_fitems([taubeta, t2y(range(1997, 2019), *taubeta)] for taubeta, _ in FitRes().sic.fitems())
        super().__init__(data)

    def dump(self):
        w_path = self.W_FILES
        with open(w_path, 'wb') as file:
            pickle.dump(dict(self), file)

    @classmethod
    def load(cls):
        w_path = cls.W_FILES
        with open(w_path, 'rb') as file:
            return pickle.load(file)


class Chi1s(KLV):
    R_FILES = FitRes.W_FILES
    W_FILES = W_FILES['chi1']

    def __init__(self, load=True):
        if load:
            data = self.load()
        else:
            data = KLV.from_fitems([taubeta, chi1] for taubeta, chi1 in FitRes(load=True, thr=False).chi1.fitems())
        super().__init__(data)

    def dump(self):
        w_path = self.W_FILES
        with open(w_path, 'wb') as file:
            pickle.dump(dict(self), file)

    @classmethod
    def load(cls):
        w_path = cls.W_FILES
        with open(w_path, 'rb') as file:
            return pickle.load(file)


def real_TRGs(tau, beta, s, i, c):
    y97, y99, y00, y18 = t2y([1997, 1999, 2000, 2018], tau, beta)
    frc97 = (s*y97) / (s*y18 + i*(1-np.exp(-y18*(1-s)/i)) + c)
    frc99 = (s*y99) / (s*y18 + i*(1-np.exp(-y18*(1-s)/i)) + c)
    frc00 = (s*y00) / (s*y18 + i*(1-np.exp(-y18*(1-s)/i)) + c)
    frc18 = (s*y18) / (s*y18 + i*(1-np.exp(-y18*(1-s)/i)) + c)
    return frc97, frc99, frc00, frc18


def apparent_TRGs(tau, beta, s, i, c):
    y97, y99, y00, y18 = t2y([1997, 1999, 2000, 2018], tau, beta)
    expected97 = estimated((1-s)*y97, i, n0=200)
    expected99 = estimated((1-s)*y99, i, n0=200)
    expected00 = estimated((1-s)*y00, i, n0=200)
    expected18 = estimated((1-s)*y18, i, n0=200)

    frc97 = (s*y97 + expected97) / (s*y18 + i*(1-np.exp(-y18*(1-s)/i)) + c)
    frc99 = (s*y99 + expected99) / (s*y18 + i*(1-np.exp(-y18*(1-s)/i)) + c)
    frc00 = (s*y00 + expected00) / (s*y18 + i*(1-np.exp(-y18*(1-s)/i)) + c)
    frc18 = (s*y18 + expected18) / (s*y18 + i*(1-np.exp(-y18*(1-s)/i)) + c)
    return frc97, frc99, frc00, frc18


def studied_TDGs(tau, beta, s, i, c):
    y97, y99, y00, y18 = t2y([1997, 1999, 2000, 2018], tau, beta)
    frc97 = (1 - np.exp(-y97*(1-s)/i)) / (1 - np.exp(-y18*(1-s)/i))
    frc99 = (1 - np.exp(-y99*(1-s)/i)) / (1 - np.exp(-y18*(1-s)/i))
    frc00 = (1 - np.exp(-y00*(1-s)/i)) / (1 - np.exp(-y18*(1-s)/i))
    frc18 = (1 - np.exp(-y18*(1-s)/i)) / (1 - np.exp(-y18*(1-s)/i))
    return frc97, frc99, frc00, frc18


def main():
    Slopes(load=False).dump()
    print('TRG initiated')
    TRGs(load=False).dump()
    print('TRG finished')
    TDGs(load=False).dump()
    DBDTs(load=False).dump()
    BTs(load=False).dump()
    YTs(load=False).dump()
    Chi1s(load=False).dump()
