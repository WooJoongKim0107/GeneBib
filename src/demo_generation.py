from TimeSeries import rsrc_dir
from TimeSeries.LoHL import LoHL
from Share.share import Shares

W_FILES = {
    'paper': f'{rsrc_dir}/demo_data/paper_hitgene_list.txt',
    'patent': f'{rsrc_dir}/demo_data/patent_hitgene_list.txt',
    'patent_gon': f'{rsrc_dir}/demo_data/patent_hitgene_list_gon.txt',
}


def lohl_of_interest(mtype, genes: set):
    return [x for x in LoHL(mtype) if not genes.isdisjoint(x[2:])]


def main():
    kings = set(Shares('paper').ikings[1990].keys())
    for mtype in ['paper', 'patent', 'patent_gon']:
        lohl = lohl_of_interest(mtype, kings)
        string = '\n'.join(','.join(str(v) for v in x) for x in lohl)

        with open(W_FILES[mtype], 'w') as file:
            file.write(string)


if __name__ == '__main__':
    main()
