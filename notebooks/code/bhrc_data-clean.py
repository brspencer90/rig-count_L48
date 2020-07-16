# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
import requests
from bs4 import BeautifulSoup as soup

# Define local directories
master_dir = 'C:\\Users\\Bryan\\OneDrive\\02 GitHub\\rig-count_L48\\'
data_raw_dir = 'C:\\Users\\Bryan\\OneDrive\\02 GitHub\\rig-count_L48\\data\\raw\\'
data_interim_dir = 'C:\\Users\\Bryan\\OneDrive\\02 GitHub\\rig-count_L48\\data\\interim\\'
data_external_dir = 'C:\\Users\\Bryan\\OneDrive\\02 GitHub\\rig-count_L48\\data\\external\\'

#***************************************#
# Get web files, convert to .xlsb and save
url = 'https://rigcount.bakerhughes.com/na-rig-count'

dinner = soup(requests.get(url).text,'lxml')

# Find the tag with appropriate text, extract URL
file_link = dinner.find('a', text='North America Rotary Rig Count (Jan 2000 - Current)')['href']

res = requests.get(file_link)

file_d_name = 'nam_rig-count'

with open(data_external_dir+file_d_name+'.xlsb','wb') as local:
    for chunk in res.iter_content(chunk_size=128):
        local.write(chunk)

#***************************************#
# Read Excel file
filename = 'nam_rig-count'
sheet0 = 'Current Weekly Summary'
sheet1 = 'US Count by Basin'
sheet2 = 'US Oil & Gas Split'
sheet3 = 'US Count by Trajectory'

df = pd.read_excel(data_external_dir + filename+'.xlsb', sheet_name=sheet1, header=9,usecols=range(0,65),engine='pyxlsb')

# Save raw file with date qualifier
file_date = convert_date(df.iloc[1:,0].max()).strftime('%Y-%m-%d')

df.to_excel(data_raw_dir+filename+'_'+file_date+'.xlsx',engine='xlsxwriter')

#***************************************#
# Change 'Unnamed' columns to NaN
col_list = df.columns.to_list()

for col in range(0,len(col_list)):
    if 'Unnamed' in col_list[col]:
        col_list[col] = np.nan

df.columns = pd.Series(col_list).fillna(method='ffill').tolist()

#***************************************#
# Creating new data frame, create new Basin column
col_unique = pd.Series(col_list).fillna(method='ffill').unique()[1:]
df_new = pd.DataFrame()

for num in range(0,len(col_unique)):
    try:
        df_trans = pd.DataFrame(df.iloc[1:,0:4]) 
        df_trans['Basin'] = col_unique[num]
        df_trans.columns = ['Date','Oil','Gas','Misc','Basin']
    
        df_new = df_new.append(df_trans)
        df.pop(col_unique[num])
    
        df_trans = pd.DataFrame()
    except:
        print(col_unique[num])
        print(df.head())
        
#***************************************#
# Convert date column to date time string

df_new[df_new.Date.isna()].shape     # 32 lines of NaN - across the four original data cols

df_dropped = df_new.dropna()     # drop NaN values

df_dropped.loc[:,'Date'] = df_dropped.loc[:,'Date'].apply(convert_date)

df_dropped = df_dropped.reset_index(drop=True)

#***************************************#
# Melt types of wells, sort by 'Date', reset and remove index column.
        
#df_melt = pd.melt(frame=df_dropped,id_vars=['Date','Basin'],var_name='Well Type',value_name='Rigs')
#df_melt = df_melt.sort_values(['Date','Basin']).reset_index()
#df_melt.pop('index')

#df_melt.to_csv(data_interim_dir+'nam_rig-count_by-basin.csv',index=False)

list_basin = df_dropped['Basin'].unique().tolist()

for basin in list_basin: 
    
