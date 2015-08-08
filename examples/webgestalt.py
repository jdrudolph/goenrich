import pandas as pd

path = 'db/webgestalt_example_results/files/final_sig_file_1439064580.tsv'

def _parse(path):
    with open(path) as f:
        res = []
        for line in f:
            if 'GO:' in line:
                res = dict(zip(['namespace', 'name', 'GO_ID'],
                    line.strip().split('\t')))
            elif len(res) > 0:
                res.update(dict(x.split('=') for x in line.strip().split(';')))
                yield res
                res = []

def read(path):
    df = pd.DataFrame(_parse(path))
    df['adjP'] = df['adjP'].astype(float)
    df['rawP'] = df['rawP'].astype(float)
    df['E'] = df['E'].astype(float)
    df['R'] = df['R'].astype(float)
    df['C'] = df['C'].astype(int)
    df['O'] = df['O'].astype(int)
    df['namespace'] = df['namespace'].str.replace(' ', '_')
    return df
