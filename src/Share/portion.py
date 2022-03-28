"""
Find the fraction of categories (genetic tools, medical science, etc) of debuted genes.
The term "field" is used as an synonym of "category" here.
"""
import json
from collections import Counter, defaultdict
import pandas as pd
from NestedDict.klv import KLV
from TimeSeries import rsrc_dir
from TimeSeries.debut import Debuts

R_FILES = {'fields': f'{rsrc_dir}/data/fields.json'}

W_FILES = {
    'count': f'{rsrc_dir}/pdata/portion/count_mtype.csv',
    'portion': f'{rsrc_dir}/pdata/portion/portion_mtype.csv',
}


def parse_fields():
    """
    parse {rsrc_dir}/data/fields.json file: dict, {field -> [genes belong to the field]}
    into :return dict, {gene -> [field ... ]}
    """
    with open(R_FILES['fields'], 'r') as file:
        fields = json.load(file)

    res = defaultdict(list)
    for field, genes in fields.items():
        for gene in genes:
            res[gene].append(field)
    return res


class Counts(KLV):
    """
    Counts: KLV, {debut -> {field -> num of genes}}
    .transposed: KLV, {field -> {debut -> num of genes}}
    """
    FIELDS = parse_fields()
    W_FILES = W_FILES['count']

    def __init__(self, mtype):
        self.mtype = mtype
        counts = self.count(mtype)
        super().__init__(counts)

    def to_csv(self):
        w_path = self.W_FILES.replace('mtype', self.mtype)
        df = pd.DataFrame(self).fillna(0)
        df.to_csv(w_path)

    @classmethod
    def count(cls, mtype):
        return {debut: cls.categorize(igenes) for debut, igenes in Debuts(mtype, n=1).transposed.items()}

    @classmethod
    def categorize(cls, igenes):
        """
        :param igenes: iterator of genes
        :return: Counter, {field -> num of genes with duplications}
        """
        counter = Counter()
        for gene in igenes:
            for field in cls.FIELDS.get(gene, ['Others']):
                counter[field] += 1
        return counter


class Portions(KLV):
    """
    Portions: KLV, {debut -> {field -> fraction of genes}}
    .transposed: KLV, {field -> {debut -> fraction of genes}}
    """
    W_FILES = W_FILES['portion']

    def __init__(self, mtype):
        self.mtype = mtype
        portions = self.calculate(mtype)
        super().__init__(portions)

    def to_csv(self):
        w_path = self.W_FILES.replace('mtype', self.mtype)
        df = pd.DataFrame(self).fillna(0)
        df.to_csv(w_path)

    @classmethod
    def calculate(cls, mtype):
        return {debut: cls.categorize(genes) for debut, genes in Debuts(mtype, n=1).transposed.items()}

    @classmethod
    def categorize(cls, genes):
        total = len(genes)
        counts = Counts.categorize(genes)
        return {field: 100*count/total for field, count in counts.items()}


def update():
    for mtype in ['paper', 'patent_gon', 'any']:
        Counts(mtype).to_csv()
        Portions(mtype).to_csv()
