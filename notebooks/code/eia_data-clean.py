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

# Read Excel file
filename = 'nam_rotary rig count.xlsx'
sheet1 = "US Count by Basin"
sheet2 = "US Oil & Gas Split"
sheet3 = "US Count by Trajectory"


df = pd.read_excel(data_raw_dir + filename, sheet_name=sheet1, header=9,usecols=range(0,65))

# Change 'Unnamed' columns to NaN
col_list = df.columns.to_list()

for col in range(0,len(col_list)):
    if 'Unnamed' in col_list[col]:
        col_list[col] = np.nan
        
#[[col_list[col] = np.nan] if 'Unnamed' in col_list[col] for col in range(0,len(col_list))]
        
df.columns = pd.Series(col_list).fillna(method='ffill').tolist()

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

# Melt types of wells, sort by 'Date', reset and remove index column.
        
df_new = pd.melt(frame=df_new,id_vars=['Date','Basin'],var_name='Well Type',value_name='Rigs')
df_new = df_new.sort_values(['Date','Basin']).reset_index()
df_new.pop('index')

df_new.to_csv(data_interim_dir+'nam_rig-count_by-basin.csv')
