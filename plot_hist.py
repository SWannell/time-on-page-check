# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 12:08:51 2020

@author: SWannell
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt; plt.style.use('ggplot')

df = pd.read_csv('AmendedData\\PageTimes_Over50PVs.csv', index_col=0)

df.index = df.index.str.replace('www.redcross.org.uk/stories', '')
df.index = df.index.str.replace('/.*/', '/')
df = df[df.index.str.contains('corona') | df.index.str.contains('nhs')]

time_minsecs = df.columns[-20:]
time_ints = [30*i for i in range(1, 20+1)]
new_cols = list(df.columns[:len(df.columns)-20]) + time_ints
df.columns = new_cols

page = [df.index[0]]
a = df.loc[page, time_ints].columns
b = df.loc[page, time_ints]
avg_capped = np.dot(a, b.values[0]) / df.loc[page, "Unique Pageviews"]
avg_default = df.loc[page, "Avg time on page"]
cumsum = df.loc[page, time_ints].cumsum(axis=1)
median_person = cumsum.loc[page, 600].values[0] / 2
avg_median = 0
for i in cumsum.columns:
    if cumsum.loc[page, i].values[0] > median_person:
        avg_median = i
        break

mins_to_x = lambda mins: (mins - 30) / 30


def add_annotate_line(text, mins, ax, color='#000000'):
    """Add a vertical line at xy, annotated with the text."""
    ymax = ax.get_ylim()[1]
    ax.axvline(x=mins_to_x(mins), color=color)
    ax.annotate(text, (mins_to_x(mins)+0.1, ymax-ymax/10), rotation=90,
                ha='right', color=color)


figs, axs = plt.subplots(2, 3, figsize=(15, 10))
for (ax, page) in zip(axs.flatten(), df.index):
    page_df = df.loc[page, time_ints]
    views = df.loc[page, "Unique Pageviews"]
    page_df.plot.bar(color='#f1b13b', ax=ax)
    ymax = ax.get_ylim()[1]
    ax.set_ylim((0, ymax))
    time_counts = page_df.values
    avg_capped = np.dot(time_ints, time_counts) / views
    add_annotate_line('Mean (capped)', avg_capped, ax, color='#158aba')
    avg_default = df.loc[page, "Avg time on page"]
    add_annotate_line('"Avg time on page"', avg_default, ax, color='#1a3351')
    cumsum = page_df.cumsum()
    median_person = cumsum.iloc[-1] / 2
    avg_median = 0
    for i in cumsum.index:
        if cumsum.loc[i] > median_person:
            avg_median = i
            break
    add_annotate_line('Median', avg_median, ax, color='#158aba')
    ax.set_title(page, fontsize=10)
    ax.set_xticklabels(time_minsecs)
axs[0, 0].set_ylabel('Users')
axs[1, 0].set_ylabel('Users')
axs[-1, -1].axis('off')
plt.tight_layout()
plt.savefig('Outputs\\TimeDistvsAvgTime.png')