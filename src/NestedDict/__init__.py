"""
Package to deal with nested dictionary more easily.
Currently, only dictionary of dictionaries (depth=2 dictionary)

Classes defined here simply bounds several methods to a Python dictionary object,
 not modifying their original methods. Therefore, their instances can be treated as simple Python dictionaries.

Many methods are intended to replace nested for loop into single for loop.
So if nested for loop is okay for you, then just consider them as simple Python dictionaries.
"""
from .klv import KLV
