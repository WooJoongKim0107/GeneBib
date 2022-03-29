"""
Updates all output results of Pareto library
"""
from Pareto import *
from TimeSeries import rsrc_dir


def main():
    print(f'Update all outputs of Pareto.\nFile io directory: {rsrc_dir}')
    pareto.update()
    inheritance.update()


if __name__ == '__main__':
    main()
