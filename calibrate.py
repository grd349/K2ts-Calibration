#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.gridspec as gridspec
from astropy.stats import mad_std

if __name__ == "__main__":
    results = pd.read_csv('calibration_sample.csv')
    results['LogNumax'] = np.log10(results.Numax)
    print(results.columns)
    rg = results[results.Numax > 0]
    other = results[results.Numax < 0]
    
    x = rg.LogNumax.values
#    y = np.log(rg.Metric1.values + rg.Metric2.values + rg.Metric3.values)
    y = np.log10(np.abs(rg.mean1 - rg.w100))
    res1 = np.polyfit(y[x > 0.8], x[x > 0.8], 2)
    print(res1)
    res = np.polyfit(x[x > 0.8], y[x > 0.8], 2)
    
    fig = plt.figure()
    gs = gridspec.GridSpec(2, 2, width_ratios=(4,2), height_ratios=(4,2))
    
    ax1 = fig.add_subplot(gs[0])

    ax1.scatter(x, y, facecolor='none', edgecolor='k', \
                alpha=0.5, s=20, label='Data')
    xind = np.linspace(x.min(), x.max(), 100)
    fit = np.poly1d(res)(xind)
    ax1.plot(xind, fit, 'r--', lw=3, label='Fit {:.4f} x**2 + {:.4f}x + {:.4f}'.format(*res))
    ax1.set_xlabel('Log10(Numax)')
    ax1.set_ylabel('Granulation Metric')
    ax1.legend(loc=3)
    
    ax2 = fig.add_subplot(gs[1])
    resid = (y) - (np.poly1d(res)(x))
    sns.kdeplot(resid, shade=True, ax=ax2)
    ax2.set_xlim([-1,1])
    ax2.set_xlabel('Resid')
    
    rg['resid'] = y - np.poly1d(res)(x)
    ax3 = fig.add_subplot(gs[2])
    ax3.scatter(rg.Numax, rg.resid, c='k', alpha=0.2)
    CS = ax3.scatter(rg.Numax[rg.M > 0], rg.resid[rg.M > 0], \
                     c=rg.M[rg.M > 0], \
                     cmap='copper', \
                     vmin=0.1)
    cbar = fig.colorbar(CS)
    cbar.ax.set_ylabel('Mass')
    ax3.set_ylim([-1,1])
    ax3.set_xlabel('Numax')
    ax3.set_ylabel('Resid')
    ax3.set_xlim([0,250])
    ax4 = fig.add_subplot(gs[3])
    
    sns.kdeplot(rg.M[rg.M > 0], rg[rg.M > 0].resid, nlevels=10, ax=ax4)
    ax4.set_xlim([0.5,3])
    ax4.set_ylim([-0.5,0.5])

    plt.tight_layout()
    fig.savefig('calibration.png')
    print("Bias : {:.4f}".format(np.median(resid)))
    print("Scatter : {:.4f}".format(np.std(resid)))
    print("Robust Scatter : {:.4f}".format(mad_std(resid)))
    plt.show()
