"""
Calculate the number of taxonomically-dispersed genes with only one sequence studied until 2018.

 expected(N, n) returns the expectation of such TDGs when N sequences and n genes are found
 estimated(N, n, n0) returns the same, but using approximation; expected(rN, rn) = expected(N, n)*r
"""
import pickle
import mpmath as mp
from mpmath import loggamma, exp
from TimeSeries import rsrc_dir

W_FILES = {'': f'{rsrc_dir}/pdata/supple_plot/omega.pkl'}


def lcomb(n, r):
    """log(comb(n, r))"""
    return loggamma(n+1) - loggamma(r+1) - loggamma(n-r+1)


def comb(n, r):
    return exp(lcomb(n, r))


def omega(n, i, x):
    m = min(i-x, (n-x)//2)
    return comb(i, x)*mp.fsum(comb(i-x, j)*comb(n-x-j-1, j-1) for j in range(1, m+1)) + int(x == n)


def expected(N, n):
    weighted = sum(x*omega(N, n, x) for x in range(1, n))
    total = comb(N + n - 1, n - 1)
    return weighted/total


def estimated(N, n, n0=500):
    k = round(N / n, 3)
    r = n / n0
    return expected(int(k * n0), n0) * r


def addictiveness(N, n):
    factors = [0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 4.0, 10.0]
    return {factor: expected(factor*N, n) for factor in factors}


def get_sfig6():
    Nns = [(125, 500), (250, 500), (500, 500), (1000, 500), (2500, 500)]
    return {(N, n): addictiveness(N, n) for N, n in Nns}


def update():
    res = get_sfig6()
    with open(W_FILES[''], 'wb') as file:
        pickle.dump(res, file)
