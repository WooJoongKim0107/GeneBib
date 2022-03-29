"""
This code is demo-version of <fitting.py> code.

You can still run <fitting.py>, but due to the randomness of 'random_initial_paras(1_000_000, BOUNDARIES)' on line 31,
  no one can test if the code runs properly as I did.

This code uses <.../demo_initial_paras.pkl> rather than 'random_initial_paras' to eliminate the randomness.
<.../demo_initial_paras.pkl> corresponds to a valid result of 'random_initial_paras(100, BOUNDARIES)'.
"""
import pickle
from collections import deque
from TimeSeries import rsrc_dir
from fitting import fitting, write

R_FILES = {'ini_paras': f'{rsrc_dir}/data/demo_initial_paras.pkl'}


def main(taubeta):
    chi_1s, chi_2s, paras = (deque() for _ in range(3))
    for ini_paras in demo_inital_paras():
        chi1, chi2, sic = fitting(*taubeta, ini_paras)
        chi_1s.append(chi1)
        chi_2s.append(chi2)
        paras.append(sic)
    write(*taubeta, [chi_1s, chi_2s, paras])


def demo_inital_paras():
    with open(R_FILES['ini_paras'], 'rb') as file:
        return pickle.load(file)
