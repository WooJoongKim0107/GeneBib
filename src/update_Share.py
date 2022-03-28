"""
Updates all output results of Share library
"""
from Share import *
from TimeSeries import rsrc_dir


def main():
    print(f'Update all outputs of Share.\nFile io directory: {rsrc_dir}')
    share.update()
    portion.update()


if __name__ == '__main__':
    main()
