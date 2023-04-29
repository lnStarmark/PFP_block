# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 07:58:04 2023

@author: admin
"""

import numpy as np
import matplotlib.pyplot as plt

from io import BytesIO
import tarfile
from urllib.request import urlopen
 
url = 'http://www.dcc.fc.up.pt/~ltorgo/Regression/cal_housing.tgz'
b = BytesIO(urlopen(url).read())
fpath = 'CaliforniaHousing/cal_housing.data'
 
with tarfile.open(mode='r', fileobj=b) as archive:
    housing = np.loadtxt(archive.extractfile(fpath), delimiter=',')
 
y = housing[:, -1]
pop, age = housing[:, [4, 7]].T


def add_titlebox(ax, text, shft_x, shft_y):
    ax.text(shft_x, shft_x, text,
        horizontalalignment='center',
        transform=ax.transAxes,
        bbox=dict(facecolor='silver', alpha=0.6),
        fontsize=10.)
    return ax


gridsize = (3, 2)
fig = plt.figure(figsize=(12, 8))
ax1 = plt.subplot2grid(gridsize, (0, 0), colspan=2, rowspan=2)
ax2 = plt.subplot2grid(gridsize, (2, 0))
ax3 = plt.subplot2grid(gridsize, (2, 1))

ax1.set_title(
    'Home value as a function of home age & area population',
    fontsize=12
)

sctr = ax1.scatter(x=age, y=pop, c=y, cmap='RdYlGn')
plt.colorbar(sctr, ax=ax1, format='$%d')
ax1.set_yscale('log')
add_titlebox(ax1, 'Scatter', .60, .7)

ax2.hist(age, bins='auto')
add_titlebox(ax2, 'Histogram: home age', .60, .7)

ax3.hist(pop, bins='auto', log=True)
add_titlebox(ax3, 'Histogram: area population (log scl.)', .60, .7)

plt.show()