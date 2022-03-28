"""
Measure the size - the number of UniProtKB/Swiss-Prot entries a given gene community has -
 of genes which have at least one hit during 1990-2018.

57.20% gene communities having at least one hit during 1990-2018 are of size 1.
"""
import json
from collections import Counter
from TimeSeries import rsrc_dir
from TimeSeries.time_series import GYH

R_FILES = {'': f'{rsrc_dir}/data/clusters.json'}

W_FILES = {'': f'{rsrc_dir}/pdata/size_dist/size_dist.json'}


def get_genes_with_hits():
    return [gene for gene, yhs in GYH('any').items() if 1990 <= max(yhs) <= 2018]


def load_clusters():
    """clusters: list, clusters[i] = {entries in i-th gene community}"""
    with open(R_FILES[''], 'rb') as file:
        clusters = json.load(file)
    return clusters


def count_sizes(genes):
    """sizes: dict, {# of entries (size) -> # of genes of that size}"""
    clusters = load_clusters()
    n = len(clusters)
    sizes = Counter(len(clusters[gene]) for gene in genes if gene < n)
    return sizes


def main():
    fresh_genes = get_genes_with_hits()
    sizes = dict(count_sizes(fresh_genes).most_common())
    with open(W_FILES[''], 'wb') as file:
        json.dump(sizes, file)
    print(f'{sizes[1]/sum(sizes.values())*100:.2f}% genes having at least one hit during 1990-2018 are of size 1.')
