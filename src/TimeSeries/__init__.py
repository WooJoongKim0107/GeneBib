"""
Package for the generation of time-series data.

As genes are clusters of UniProtKB/Swiss-Prot entries, they are sometimes called 'gene communities' in our codes:
 actually, before 2022, I used the term 'community' (or 'cmnt' for short) to indicate gene in my source codes.
 So, there might be some cases where the term 'community' is used instead.
 Just consider them as 'gene'.

See <debut.py> finds the debut year of each gene (or n-tuple of genes)
See <time_series.py> to generate time-series of hits of each gene (or n-tuple of genes)
See <total.py> to generate the annual number of paper/patents with hit
See <pattern.py> to classify each gene depending on their time-series of hits
"""
from .base_functions import safe_update, swap_item

__all__ = ['demo', 'base_dir', 'rsrc_dir',
           'LoHL', 'time_series', 'debut', 'pattern', 'total',
           'safe_update', 'swap_item']

# base_dir should be modified according to your computer system.
# base_dir will be referenced whenever our python code reads or writes files.
# Python error regarding the locations of the files will be resolved by correcting 'base_dir'
# I'll leave my 'base_dir' as an example.
# 'rsrc_dir' will be modified automatically if 'base_dir' and 'demo' are corrected.
demo = False  # Since we only provides demo-inputs, set demo as True.
base_dir = 'C:/Users/lrlr9/PycharmProjects/GeneBib4'  # Location where <plots> and <src> directories exist
rsrc_dir = f'{base_dir}/demo_rsrc' if demo else f'{base_dir}/rsrc'  # Location where <data> and <pdata> directories are
