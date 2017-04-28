#!/usr/bin/env python3

import numpy as np
import glob
import sys
sys.path.append('/home/davies/Projects/K2_seismo_pipes/K2pipes/')
import matplotlib.pyplot as plt
import pandas as pd

from K2data import Dataset
from read_database import APOKASC
from K2ts import TS
from K2ps_flicker import PS_FLICKER

if __name__ == "__main__":
    apo =  APOKASC('APOKASC_cat_v3.1.7.txt')
    data_dir = '/home/davies/Dropbox//K2_seismo_pipes/APOKASC_stars/Data/'
    vars_dict = {'Flicker': [['w100', 'mean1'],[0.5, 288.0, 250.0]]}
    cols = ['KIC', 'Numax', 'M', 'Z']
    for n in vars_dict:
        cols = cols + vars_dict[n][0]
    results = pd.DataFrame(columns=cols)

    for key, row in apo.df.iterrows():
        print(row.KEPLER_ID, key)
        data_file = glob.glob(data_dir + 'kplr*' + \
                              str(row.KEPLER_ID) + '*concat.dat')
        if len(data_file) > 0:
            x = 1
            try:
                ds = Dataset(row.KEPLER_ID, data_file[0])
                ds.read_timeseries(sigma_clip=4.0)
                ds.power_spectrum()
                method = PS_FLICKER(ds)
                res = [row.KEPLER_ID, row.NU_MAXRG, row.DR10_S1_MASS, row.FE_H_ADOP_COR]
                for n in vars_dict:
                    tmp = vars_dict[n][1]
                    w, m = method.get_metric(low_f=tmp[0], high_f=tmp[1], white=tmp[2])
                    res += [w, m]
                results.loc[len(results)] = res
            except:
                print("Failed on ", row.KEPLER_ID)
            if key % 50.0 < 1.0: 
                results.to_csv('calibration_sample.csv', index=False)
    results.to_csv('calibration_sample.csv', index=False) 
