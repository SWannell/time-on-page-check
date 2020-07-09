# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 11:48:38 2020

@author: SWannell
"""

import pandas as pd

fp = r'RawData\\20-06 Journey time event checks.xlsx'
ref_str = '>50 PVs'

xls = pd.ExcelFile(fp)
sheets = xls.sheet_names

df = pd.read_excel(xls, ref_str, skiprows=1)
# df = df[df['Pages'].str.contains('www.redcross.org.uk/stories/')]
df.dropna(inplace=True)
df.set_index('Pages', inplace=True)

df.to_csv('AmendedData\\PageTimes_Over50PVs.csv')