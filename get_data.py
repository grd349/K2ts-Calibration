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
    results = pd.DataFrame(columns=['KIC', 'Numax', 'Metric1', 'Metric2'])
    for key, row in apo.df[:1].iterrows():
        print(row.KEPLER_ID)
        data_file = glob.glob(data_dir + 'kplr*' + \
                              str(row.KEPLER_ID) + '*concat.dat')
        if len(data_file) > 0:
            ds = Dataset(row.KEPLER_ID, data_file[0])
            ds.read_timeseries(sigma_clip=5.0)
            #ds.plot_timeseries()
            ds.power_spectrum()
            #ds.plot_power_spectrum()
            #ts_method = TS(ds)
            #ts_method.smooth_flux(convolve=False)
            #F8 = ts_method.corrected_F8(sig_clip=True)
            method = PS_FLICKER(ds)
            metric1 = method.get_metric()
            metric2 = method.get_metric(low_f = 5.0)
            results.loc[len(results)] = [row.KEPLER_ID, row.NU_MAXRG, metric1, metric2]
    #results.to_csv('calibration_sample.csv', index=False)
    results = pd.read_csv('calibration_sample.csv')
    fig,ax = plt.subplots()
    results = results[results.Numax > 0]
    ax.scatter(results.Numax, results.Metric1, label='Met1', c='r')
    ax.scatter(results.Numax, results.Metric2, label='met2', c='b')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.legend()
    plt.show()
