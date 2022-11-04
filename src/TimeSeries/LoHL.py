"""
Parse <hitgene_list.txt> and save as python list after filtering invalid data.

Here, each row of <hitgene_list.txt> contains
    1. index of the paper (or patent)
    2. publication year (or application year in case of patent)
    3. index of genes hit if exists

Below lists all cases of the invalidity:
    1. Genes listed in python set 'EXCLUDED'
    2. Paper/patent with no genes or more than 10 genes
    3. Paper/patent with no information on publication year (those are filled with year < 1800)
"""
import pickle
import numpy as np
from TimeSeries import rsrc_dir, safe_update, swap_item

R_FILES = {
    'paper': f'{rsrc_dir}/data/paper_hitgene_list.txt',
    'patent': f'{rsrc_dir}/data/patent_hitgene_list.txt',
    'patent_gon': f'{rsrc_dir}/data/patent_hitgene_list_gon.txt',
}

W_FILES = {
    'paper': f'{rsrc_dir}/pdata/LoHL/LoHL_paper.pkl',
    'patent': f'{rsrc_dir}/pdata/LoHL/LoHL_patent.pkl',
    'patent_gon': f'{rsrc_dir}/pdata/LoHL/LoHL_patent_gon.pkl',
    'any': f'{rsrc_dir}/pdata/LoHL/LoHL_any.pkl',
}


class LoHL(list):
    """

    """
    R_FILES = R_FILES
    W_FILES = W_FILES

    # Set of genes with false positive hits
    EXCLUDED = {
        1486, 18682, 28756,
        9912, 20521, 4911,
        3898,
    }

    # The last year where valid data exist
    END_YEARS = {
        'paper': 2018,
        'patent': 2014,
        'patent_gon': 2015,
        'any': 2018,
    }

    def __init__(self, mtype: str, load=True):
        self.mtype = mtype
        data = self.load(mtype) if load else read(mtype)
        super().__init__(data)
        self.sort(key=sort_key)

    def dump(self):
        """pickle LoHL instance as list object"""
        with open(self.W_FILES[self.mtype], 'wb') as file:
            pickle.dump(list(self), file)

    @classmethod
    def load(cls, mtype):
        """unpickle the list object pickled by .dump()
        If you want to cast it into LoHL type, use LoHL(mtype, n, load=True) instead."""
        with open(cls.W_FILES[mtype], 'rb') as file:
            return pickle.load(file)

    @classmethod
    def init_with_endyear(cls, mtype, endyear):
        with swap_item(cls.END_YEARS, mtype, endyear):
            print(cls.END_YEARS[mtype])
            return cls(mtype, load=False)


def read(mtype):
    if mtype == 'any':
        return read('paper') + read('patent_gon')
    else:
        excluded = LoHL.EXCLUDED
        end_year = LoHL.END_YEARS[mtype]
        return [v for x in load_raw(mtype) if isvalid(v := removed(x, excluded), end_year)]


def isvalid(x: list, end_year):
    return valid_size(x) and valid_year(x, end_year)


def removed(x: list, excluded: set):
    """
    [material_idx, year, *genes] -> [material_idx, year, *genes_except_excluded]
    """
    return x[:2] + [v for v in x[2:] if v not in excluded]


def load_raw(mtype):
    """Parse the whole <hitgene_list.txt> file given as 'file_buffer'"""
    if mtype == 'any':
        raise ValueError
    else:
        with open(R_FILES[mtype], 'r') as file:
            return [parse(line, mtype) for line in file.readlines()[1:]]


def valid_size(x: list):
    return 0 < len(x) - 2 <= 10  # len(x) - 2 == the number of genes hit on the given paper/patent


def valid_year(x: list, end_year):
    return 1800 <= x[1] <= end_year


def parse(x: str, mtype: str):
    """Parse each row of <hitgene_list.txt> into python list"""
    if mtype == 'paper':
        midx, year, *genes = map(np.uint32, x.split(','))
    elif mtype == 'patent' or mtype == 'patent_gon':
        midx, year, *genes = x.split(',')[0], *map(np.uint32, x.split(',')[1:])
    else:
        raise ValueError
    genes = np.sort(genes)
    return [midx, year, *genes]


def sort_key(x: list):
    return x[1], x[0]


def update():
    for mtype in ['paper', 'patent', 'patent_gon', 'any']:
        safe_update(LoHL, dict(mtype=mtype, load=True), dict(mtype=mtype, load=False))
