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
    vars_dict = {'Flicker': [['w100', 'mean1', 'med1', 'std1'],[0.5, 288.0, 100]], \
                 'lowf': [['w1000', 'meanlf', 'medlf', 'stdlf'],[0.5, 10.0, 1000]], \
                 'lowb': [['w10', 'meanlb', 'medlb', 'stdlb'],[10.0, 20.0, 10]]}
    cols = 
    results = pd.DataFrame(columns=['KIC', 'Numax', \
                                    'w1', 'mean1', 'med1', 'std1', \
                                    'w2', 'mean2', 'med2', 'std2', \
                                    'w3', 'mean3', 'med3', 'std3'])
    for key, row in apo.df.iterrows():
        print(row.KEPLER_ID)
        data_file = glob.glob(data_dir + 'kplr*' + \
                              str(row.KEPLER_ID) + '*concat.dat')
        if len(data_file) > 0:
            x = 1
            try:
                ds = Dataset(row.KEPLER_ID, data_file[0])
                ds.read_timeseries(sigma_clip=5.0)
                #ds.plot_timeseries()
                ds.power_spectrum()
                #ds.plot_powerspectrum()
                #ts_method = TS(ds)
                #ts_method.smooth_flux(convolve=False)
                #F8 = ts_method.corrected_F8(sig_clip=True)
                method = PS_FLICKER(ds)
                w1, mean1, med1, std1 = method.get_metric(low_f=0.5, high_f=10.0 )
                w2, mean2, med2, std2 = method.get_metric(low_f=10.0, high_f=20.0, white_npts=10)
                w3, mean3, med3, std3 = method.get_metric(low_f=20.0, high_f=40.0, white_npts=1000)
                results.loc[len(results)] = [row.KEPLER_ID, row.NU_MAXRG, \
                                             w1, mean1, med2, std1, \
                                             w2, mean2, med2, std2, \
                                             w3, mean3, med3, std3]
            except:
                print("Failed on ", row.KEPLER_ID)
            if key % 500 == 0: 
                results.to_csv('calibration_sample.csv', index=False)
    results.to_csv('calibration_sample.csv', index=False)
    #results = pd.read_csv('calibration_sample.csv')
    fig,ax = plt.subplots()
    rg = results[results.Numax > 0]
    other = results[results.Numax < 0]
    CS = ax.scatter(rg.Metric1, rg.Metric2, \
               c=np.log(rg.Numax), cmap='viridis', \
               vmin=np.log(1.0), s=20)
    ax.scatter(other.Metric1, other.Metric2, c='k', s=5)
#    ax.scatter(results.Numax, results.Metric2, label='Met2', c='b')
#    ax.scatter(results.Numax, results.Metric3, label='Met3', c='g')
    ax.set_xscale('log')
    ax.set_yscale('log')
    cbar = fig.colorbar(CS)
    #ax.legend()
    plt.show()
 
