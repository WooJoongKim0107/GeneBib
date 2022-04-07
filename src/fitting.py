"""
Fitting parameters of the model describing the slow down of the exploration of new genes.

The pseudo code of the procedure is:

    for i in range(1_000_000):
        randomly pick one set of initial parameters
        do SLSQP fitting using the above initial parameter
    pickle the results

The results of each (tau, beta) will be pickled into a single file <{rsrc_dir}/pdata/fit_raw/tau7_beta09.pkl>
 if tau=7 and beta=0.9

If we call "randomly pick one set of initial parameters" + "do SLSQP fitting using the above initial parameter"
 as random initial fitting (RIF) for simplicity, then each file will contain a list of lists of form:
    [[chi_1 of the 1st RIF, chi_1 of the 2nd RIF, ..., chi_1 of the 1_000_000th RIF],
    [chi_2 of the 1st RIF, chi_2 of the 2nd RIF, ..., chi_2 of the 1_000_000th RIF],
    [(s, i, c) of the 1st RIF, (s, i, c) of the 2nd RIF, ..., (s, i, c) of the 1_000_000th RIF]]
"""
import pickle
import numpy as np
from multiprocessing import Pool
from itertools import product
from collections import deque
from TimeSeries import rsrc_dir
from Fitting.minimization import minimize_chi_1, minimize_chi_2, random_initial_paras, BOUNDARIES

W_FILES = {'': f'{rsrc_dir}/pdata/fit_raw/TAUBETA.pkl'}


def main(taubeta):
    directory = W_FILES[''].replace('TAUBETA', taubeta_rep(*taubeta))
    chi_1s, chi_2s, paras = (deque() for _ in range(3))
    for ini_paras in random_initial_paras(1_000_000, BOUNDARIES):
        chi1, chi2, sic = fitting(*taubeta, ini_paras)
        chi_1s.append(chi1)
        chi_2s.append(chi2)
        paras.append(sic)
    write([chi_1s, chi_2s, paras], directory)


# noinspection PyPep8
def fitting(tau, beta, paras):
    result1 = minimize_chi_1(tau, beta, paras[:-1], method='SLSQP', bounds=BOUNDARIES[:-1], options={'maxiter': 10_000})
    si, chi1 = result1['x'], result1['fun']
    # noinspection PyPep8
    result2 = minimize_chi_2(tau, beta, si, paras[-1:], method='SLSQP', bounds=BOUNDARIES[-1:], options={'maxiter': 10_000})
    c, chi2 = result2['x'], result2['fun']
    return chi1, chi2, (*si, *c)


def write(x, directory):
    with open(directory, 'wb') as file:
        pickle.dump(x, file)


def taubeta_rep(tau, beta):
    return f'tau{int(tau)}_beta{beta:.1f}'.replace('.', '')


def taubeta_grid():
    taus = np.arange(0, 20)
    betas = np.arange(0.1, 1.1, 0.1)
    grids = list(product(taus, betas))
    return grids


if __name__ == '__main__':
    grids = taubeta_grid()
    with Pool() as p:
        p.map(main, grids)
