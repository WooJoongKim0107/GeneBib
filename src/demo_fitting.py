"""
This code is demo-version of <fitting.py> code.

You can still run <fitting.py>, but due to the randomness of 'random_initial_paras(1_000_000, BOUNDARIES)' on line 31,
  no one can test if the code runs properly as I did.

This code uses <.../demo_initial_paras.pkl> rather than 'random_initial_paras' to eliminate the randomness.
<.../demo_initial_paras.pkl> corresponds to a valid result of 'random_initial_paras(100, BOUNDARIES)'.
"""
import pickle
from multiprocessing import Pool
from collections import deque, Counter
from TimeSeries import rsrc_dir
from fitting import fitting, write, taubeta_grid, taubeta_rep

R_FILES = {'ini_paras': f'{rsrc_dir}/data/demo_initial_paras.pkl'}
W_FILES = {'': f'{rsrc_dir}/pdata/fit_raw/demo_TAUBETA.pkl'}


def main(taubeta):
    directory = W_FILES[''].replace('TAUBETA', taubeta_rep(*taubeta))
    chi_1s, chi_2s, paras = (deque() for _ in range(3))
    for ini_paras in demo_inital_paras():
        chi1, chi2, sic = fitting(*taubeta, ini_paras)
        chi_1s.append(chi1)
        chi_2s.append(chi2)
        paras.append(sic)
    return safe_write([chi_1s, chi_2s, paras], directory)


def safe_write(x, directory):
    try:
        with open(directory, 'rb') as file:
            existing = pickle.load(file)
    except FileNotFoundError:
        print(f'{directory} does not exist: Create new one')
        write(x, directory)
        return 'Created new one'

    except Exception as e:
        raise e
    else:
        if existing == x:
            print(f"{directory} exist and valid")
            return 'Already exist and valid'

        else:
            print(f"{directory} exist, but may be outdated. Rewrite new one")
            write(x, directory)
            return 'Already exist but updated'


def print_summary(results):
    count = Counter(results)
    total = sum(count.values())
    print('\n--------demo_fitting.py run summary--------')
    for k, v in count.items():
        print(f'{k}: {v}/{total} case(s)')
    else:
        print()


def demo_inital_paras():
    with open(R_FILES['ini_paras'], 'rb') as file:
        return pickle.load(file)


if __name__ == '__main__':
    grids = taubeta_grid()
    with Pool() as p:
        res = p.map(main, grids)
    print_summary(res)
