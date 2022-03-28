"""
Find the debut year of each n-tuple of genes.

For n-tuple of genes, say (gene_1, gene_2, ..., gene_n), for n > 1,
 the papers (patents) published (filed) in the debut years of gene_1, gene_2, ..., gene_n are disregarded.

The term 'outset' indicates the year of the first hit.
Obviously, outset = debut if n=1, and outset <= debut otherwise.
"""
import pickle
from itertools import product, groupby
from more_itertools import nth
from TimeSeries import rsrc_dir, safe_update
from TimeSeries.time_series import GYH

R_FILES = {
    'paper': f'{rsrc_dir}/pdata/time_series/gyh_paper_n-tuple.pkl',
    'patent': f'{rsrc_dir}/pdata/time_series/gyh_patent_n-tuple.pkl',
    'patent_gon': f'{rsrc_dir}/pdata/time_series/gyh_patent_gon_n-tuple.pkl',
    'any': f'{rsrc_dir}/pdata/time_series/gyh_any_n-tuple.pkl',
}

W_FILES = {
    'paper': f'{rsrc_dir}/pdata/debut/debut_paper_n-tuple.pkl',
    'patent': f'{rsrc_dir}/pdata/debut/debut_patent_n-tuple.pkl',
    'patent_gon': f'{rsrc_dir}/pdata/debut/debut_patent_gon_n-tuple.pkl',
    'any': f'{rsrc_dir}/pdata/debut/debut_any_n-tuple.pkl',
}


class Debuts(dict):
    """
    A dictionary mapping from gene index (int) to its debut year (int).

    Debuts: dict, {gene index -> debut year}
    .transposed: dict, {debut year -> list of genes debuted}
    """
    R_FILES = R_FILES
    W_FILES = W_FILES

    def __init__(self, mtype, n=1, load=True):
        self.mtype, self.n = mtype, n
        if load:
            data = self.load(mtype, n)
        elif n == 1:
            data = find_outset(GYH.load(mtype, n))
        else:
            data = _Debuts(mtype, n)()
        super().__init__(sorted_dict(data))

    @property
    def transposed(self):
        """
        :return: dict, {debut year -> list of genes debuted}
        """
        return {debut: list(igenes) for debut, igenes in groupby(self, key=self.get)}

    @property
    def counts(self):
        return {debut: len(genes) for debut, genes in self.transposed.items()}

    def dump(self):
        """pickle Debuts instance as dictionary object"""
        w_path = self.W_FILES[self.mtype].replace('n-tuple', str(self.n))
        with open(w_path, 'wb') as file:
            pickle.dump(dict(self), file)

    @classmethod
    def load(cls, mtype, n=1):
        """unpickle the dictionary object pickled by .dump()
        If you want to cast it into Debuts type, use Debuts(mtype, n, load=True) instead."""
        w_path = cls.W_FILES[mtype].replace('n-tuple', str(n))
        with open(w_path, 'rb') as file:
            return pickle.load(file)


class _Debuts:
    """Class to find the debut years for N > 1"""
    
    def __init__(self, mtype, n):
        assert n != 1
        self.singlet_outsets = find_outset(GYH.load(mtype, 1))
        self.gyh = GYH.load(mtype, n)
        self.outsets = find_outset(self.gyh)

    def __call__(self):
        mod_debuts = {}
        for genes, debut in self.outsets.items():
            if new_debut := self.find_debut(genes, debut, default=None):
                mod_debuts[genes] = new_debut
        return mod_debuts

    def any_newbie_in(self, genes, debut):
        """
        :param genes: Iterable, (gene ...), N-tuple of genes
        :param debut: int, the debut year of 'genes'
        :return: bool, if any gene in 'genes' has the same birth-year with 'genes'
        """
        return any(self.singlet_outsets[gene] == debut for gene in genes)

    def find_debut(self, genes, debut, default=None):
        if self.any_newbie_in(genes, debut):
            return nth(self.gyh[genes], 1, default)  # returns second value if exists, returns default otherwise
        else:
            return debut


def find_outset(gyh):
    """Find the year each gene appears for the first time from the given gyh"""
    return {c: next(iter(yh)) for c, yh in gyh.items()}


def sorted_dict(klv):
    debut = dict(sorted(klv.items(), key=sort_key))
    return debut


def sort_key(x):
    return x[1], x[0]


def update():
    for mtype, n in product(['paper', 'patent_gon', 'any'], [0, 1, 2, 3]):
        safe_update(Debuts, dict(mtype=mtype, n=n, load=True), dict(mtype=mtype, n=n, load=False))
