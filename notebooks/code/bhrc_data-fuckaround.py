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
import datetime as dt

import pyxlsb
from pyxlsb import convert_date

# Define local directories
master_dir = 'C:\\Users\\Bryan\\OneDrive\\02 GitHub\\rig-count_L48\\'
data_raw_dir = 'C:\\Users\\Bryan\\OneDrive\\02 GitHub\\rig-count_L48\\data\\raw\\'
data_interim_dir = 'C:\\Users\\Bryan\\OneDrive\\02 GitHub\\rig-count_L48\\data\\interim\\'
data_external_dir = 'C:\\Users\\Bryan\\OneDrive\\02 GitHub\\rig-count_L48\\data\\external\\'

# Read Excel file
filename = 'nam_rig-count_by-basin.csv'
sheet1 = "US Count by Basin"
sheet2 = "US Oil & Gas Split"
sheet3 = "US Count by Trajectory"


df = pd.read_csv(data_interim_dir + filename,parse_dates = True)

df_oil = df[df['Well Type'] == 'Oil']
fig, ax = plt.subplots()
list_basin = df.Basin.unique().tolist()
list_basin.pop(list_basin.index('Total US RigCount'))

for basin in list_basin:
    ax.plot(df_oil[df_oil['Basin']==basin]['Date'],df_oil[df_oil['Basin']==basin]['Rigs'])

plt.show()