#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.gridspec as gridspec
from astropy.stats import mad_std

if __name__ == "__main__":
    results = pd.read_csv('calibration_sample.csv')
    results['LogNumax'] = np.log(results.Numax)
    print(results.columns)
    rg = results[results.Numax > 0]
    other = results[results.Numax < 0]
    
    x = rg.LogNumax.values
#    y = np.log(rg.Metric1.values + rg.Metric2.values + rg.Metric3.values)
    y = np.log(rg.mean3.values / rg.med3.values)
    res = np.polyfit(x, y, 5)
    print(res)
    
    fig = plt.figure()
    gs = gridspec.GridSpec(1, 2, width_ratios=(4,2))
    
    ax1 = fig.add_subplot(gs[0])

    ax1.scatter(x, y, facecolor='none', edgecolor='m', s=20)
    xind = np.linspace(x.min(), x.max(), 100)
    fit = np.poly1d(res)(xind)
    ax1.plot(xind, fit, 'r--', lw=3)
    
    ax2 = fig.add_subplot(gs[1])
    resid = (y) - (np.poly1d(res)(x))
    ax2.hist(resid, normed=1, bins=np.linspace(-3,3,50))
    
    print("Bias : {:.4f}".format(np.median(resid)))
    print("Scatter : {:.4f}".format(np.std(resid)))
    print("Robust Scatter : {:.4f}".format(mad_std(resid)))
    plt.show()
