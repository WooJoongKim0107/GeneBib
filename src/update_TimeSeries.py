"""
Updates all output results of TimeSeries library
"""
from TimeSeries import *


def main():
    print(f'Update all outputs of TimeSeries.\nFile io directory: {rsrc_dir}')
    LoHL.update()
    time_series.update()
    debut.update()
    pattern.update()
    total.update()


if __name__ == '__main__':
    main()
