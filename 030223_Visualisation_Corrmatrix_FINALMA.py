#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 10:13:29 2023

@author: michele
"""


import os
import pandas as pd
import scipy.stats
from scipy.stats import spearmanr
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from textwrap import wrap

os.chdir('/home/michele/programming/python/tables')

wd = '/home/michele/programming/python/tables'

data = wd + '/cdatrans.csv'

# load in table, set index
data = pd.read_csv(data, sep = ";", decimal = ",")
data.set_index('code', inplace=True)
display(data)

# creatle triangle mask to mask out the 'double' data
low_tri = np.triu(np.ones_like(data.corr(method = 'spearman'))).astype(bool)


fig, ax = plt.subplots(figsize=(15,10))
# one
ax =sns.heatmap(data.corr(method = 'spearman'),
                annot=True,
                fmt=".2f", # show 2 decimal places
                vmin=-1,
                vmax=1,
                cmap = 'coolwarm',
                mask = low_tri,
                cbar = True,
                linecolor='white',
                linewidths=1.5,
                square=True,
                xticklabels=True,
                annot_kws={'size':12, 'weight': 'bold', 'color': 'white'})


ax.plot([0,12,0,0],[0,12,12,0],clip_on=False, color='black', lw=2)

# set xticks for better axis display
ax.set_xticklabels(ax.get_xticklabels(), rotation=22, ha='right', rotation_mode='anchor', wrap=True)
ax.set_yticklabels(ax.get_yticklabels(),wrap=True)
# title
ax.set_title("Spearman rank correlation for community interview results\n and district specific forest cover change",
             fontsize=16)

# wrap layout
plt.tight_layout()
#save layout
plt.savefig("Corrplot_interview.png",
            dpi = 600,
            # specifying tight here so that legend is not cut
            bbox_inches= "tight")
plt.show()


## find out results of p values and print

rho, p = scipy.stats.spearmanr(data[1:12])

# plot p values for later classification of p values

fig, ax = plt.subplots(figsize=(15,10))
ax =sns.heatmap(p,
                annot=True,
                fmt=".4f", # show 2 decimal places
                vmin=-1,
                vmax=1,
                cmap = 'coolwarm',
                mask = low_tri,
                cbar = True,
                linecolor='white',
                linewidths=1.5,
                square=True,
                xticklabels=True,
                annot_kws={'size':12, 'weight': 'bold', 'color': 'white'})

ax.plot([0,12,0,0],[0,12,12,0],clip_on=False, color='black', lw=2)
#ax.set_xticks(ax)
# wrap labels
#labels = [ '\n'.join(wrap(l,20)) for l in data.code]

ax.set_xticklabels(ax.get_xticklabels(), rotation=22, ha='right', rotation_mode='anchor', wrap=True)
ax.set_yticklabels(ax.get_yticklabels(),wrap=True)
ax.set_title("Spearman rank correlation for community interview results\n and district specific forest cover change",
             fontsize=16)
#ax.text()

#ax.tick_params(left=False, bottom=False)
plt.tight_layout()

plt.show()


