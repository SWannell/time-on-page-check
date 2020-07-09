# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 12:08:51 2020

@author: SWannell
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt; plt.style.use('ggplot')
import matplotlib.ticker as mtick

df = pd.read_csv('AmendedData\\PageTimes_Over50PVs.csv', index_col=0)

df.index = df.index.str.replace('www.redcross.org.uk/stories', '')

#bigappeal = df.groupby('appeal').sum().sort_values(by='users', ascending=False)
#bigappeal = bigappeal[bigappeal['users'] > 1000]
#df = df[df['appeal'].isin(bigappeal.index)]
#df[['formpage', 'payment']].drop_duplicates().sort_values(by='payment')
#df.to_csv('AmendedData\\FormFunnel.csv')

df.filter(regex=("\d{2}m \d{2}s"))

time_ints = [30*i for i in range(1, 20+1)]
new_cols = list(df.columns[:len(df.columns)-20]) + time_ints
print(new_cols)
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
# Test
page_df.plot.bar(color='#ee2a24')
plt.axvline(x=mins_to_x(60))
plt.axvline(x=mins_to_x(90))
plt.axvline(x=mins_to_x(420))
plt.ylim()[1]


def add_annotate_line(text, mins, ax, color='#000000'):
    """Add a vertical line at xy, annotated with the text."""
    ymax = ax.get_ylim()[1]
    ax.axvline(x=mins_to_x(mins), color=color)
    ax.annotate(text, (mins_to_x(mins)+0.1, ymax-1), rotation=90, ha='right',
                color=color)


fig, ax = plt.subplots(1, 1)
for page in [df.index[0]]:
    page_df = df.loc[page, time_ints]
    views = df.loc[page, "Unique Pageviews"]
    page_df.plot.bar(color='#ee2a24', ax=ax)
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

#for platform in payment_types:
#    by_month = pd.DataFrame(index=months)
#    for appeal in bigappeal.index:
#        _ = df[df['appeal'] == appeal]
#        a = _[_['payment'] == platform]
#        a.drop('appeal', axis=1, inplace=True)
#        b = a.pivot_table(index='month', columns='formpage')
#        for mth in b.index:
#            first_step = b['users'].max(axis=1).loc[mth]
#            ty_step = b['users'].loc[mth, 'Thank you']
#            formpct = ty_step/first_step
#            by_month.loc[mth, appeal] = formpct
#    cvr_by_platform[platform] = by_month
#
#figs, axs = plt.subplots(1, 3, sharey=True, figsize=(13, 5))
#for i, platform in enumerate(cvr_by_platform.keys()):
#    platform_data = cvr_by_platform[platform]
#    # Added these bizarre steps to get it to add xticklabels
#    platform_data = platform_data.reset_index()
#    platform_data = platform_data.rename(columns={"index": "month"})
#    platform_data.plot(legend=None, ax=axs[i], marker='o', linestyle='None',
#                       xticks=platform_data.index)
#    axs[i].set_xticklabels(months)
#    axs[i].set_title(platform)
#    axs[i].yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
#plt.suptitle('Form:TY conversion rate by appeal', fontsize=20)
#plt.savefig('Outputs\\CVR_from-form_payment-type.png')
#
#landing_cvr = pd.DataFrame(index=months)
#for appeal in bigappeal.index:
#    steps = {'Appeal Landing': 0, 'Thank you': 0}
#    for step in steps:
#        data = df[(df['formpage'] == step) & (df['appeal'] == appeal)]
#        data = data[['month', 'users']]
#        data.set_index('month', inplace=True)
#        data.columns = [appeal]
#        if len(data.index) != len(data.index.unique()):
#            data = data.groupby('month').sum()
#        steps[step] = data
#    cvr = steps['Thank you'] / steps['Appeal Landing']
#    landing_cvr = landing_cvr.join(cvr)
#
#fig, ax = plt.subplots(1, 1, figsize=(6, 6))
#landing_cvr.plot(legend=None, marker='o', ax=ax, linestyle='None')
#plt.xticks(range(len(landing_cvr.index)), landing_cvr.index)
#ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
#ax.set_title('Landing:TY conversion rate by appeal', fontsize=20)
#plt.savefig('Outputs\\CVR_from-landing.png')