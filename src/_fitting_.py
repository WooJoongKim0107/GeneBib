import pickle
from multiprocessing import Pool
import numpy as np
from fitting import fitting, write, taubeta_rep, taubeta_grid
from TimeSeries import rsrc_dir


def main(taubeta):
    with open(f'{rsrc_dir}/pdata/fitting/renewed/renewed_{taubeta_rep(*taubeta)}.pkl', 'rb') as file:
        old_paras = pickle.load(file)[-1]

    x = {'chi1': [], 'chi2': [], 'sic': []}
    for s, i, [c] in old_paras:
        chi1, chi2, sic = fitting(*taubeta, np.array([s, i, c]))
        x['chi1'].append(chi1)
        x['chi2'].append(chi2)
        x['sic'].append(sic)

    write(*taubeta, x)


if __name__ == '__main__':
    grids = taubeta_grid()
    with Pool() as p:
        p.map(main, grids)
