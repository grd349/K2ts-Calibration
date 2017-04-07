#!/usr/bin/env python3

import pandas as pd

class APOKASC:
    def __init__(self, filename):
        self.df = pd.read_csv(filename, comment='#', delimiter=r'\s+', \
                              skipinitialspace=True)

    def get_kics(self):
        return self.df.KEPLER_ID.values


if __name__ == "__main__":
    apo = APOKASC('APOKASC_cat_v3.1.7.txt')
    df = apo.df[['KEPLER_ID', 'NU_MAXRG', 'SYD_NU_MAX', 'OCT_NU_MAX', 'CONS_EVSTATES', 'KEP_MAG']]
    df = df.loc[(df.NU_MAXRG < 350.0) & (df.KEP_MAG < 12.0) ]
    df.to_csv('~/Dropbox/K2_seismo_pipes/APOKASC_stars/apo_stars.csv', index=False)
    for _, d in df.iterrows():
        print(d.KEPLER_ID)
