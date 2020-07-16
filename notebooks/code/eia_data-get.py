# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# Import modules
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
from datetime import datetime as dt

import re

import requests
from bs4 import BeautifulSoup as soup

import pyxlsb
from pyxlsb import convert_date

# Define local directories
master_dir = 'C:\\Users\\Bryan\\OneDrive\\02 GitHub\\rig-count_L48\\'
data_raw_dir = 'C:\\Users\\Bryan\\OneDrive\\02 GitHub\\rig-count_L48\\data\\raw\\'
data_interim_dir = 'C:\\Users\\Bryan\\OneDrive\\02 GitHub\\rig-count_L48\\data\\interim\\'
data_external_dir = 'C:\\Users\\Bryan\\OneDrive\\02 GitHub\\rig-count_L48\\data\\external\\'

api_key_eia = '231fd0a62041a63a05da2716cd3a73d6'
url_eia = 'http://api.eia.gov/series/?api_key='+api_key_eia+'&out=json&series_id='

#***********************************************************#
# Create new data frame with wti_spot (DAILY)
url_wti_spot = url_eia+'PET.RWTC.D'
label = 'wti_spot'

r = requests.get(url_wti_spot)
wti_spot_json = r.json()

df = pd.DataFrame(list(wti_spot_json['series'][0]['data']),columns=['date',label])

df.date = pd.to_datetime(df.date, format='%Y-%m-%d')
df = df[(df.date > '2010-01-01') & (df.date < str(dt.now().date()))]

#***********************************************************#
# Download brent_spot and merge with df (DAILY)
url_trans = url_eia+'PET.RBRTE.D'
label = 'brent_spot'

r = requests.get(url_trans)
json_trans = r.json()

df_eia_trans = pd.DataFrame(list(json_trans['series'][0]['data']),columns=['date',label])
df_eia_trans.date = pd.to_datetime(df_eia_trans.date, format='%Y-%m-%d')

df_eia_trans = df_eia_trans[(df_eia_trans.date > '2010-01-01') & (df_eia_trans.date < str(dt.now().date()))]

df = df.merge(df_eia_trans, how='outer').sort_values('date', ascending=False)

#***********************************************************#
# Download wti_fut_1 and merge with df (DAILY)
url_trans = url_eia + 'PET.RCLC1.D'
label = 'wti_fut_1'

r = requests.get(url_trans)
json_trans = r.json()

df_eia_trans = pd.DataFrame(list(json_trans['series'][0]['data']),columns=['date',label])
df_eia_trans.date = pd.to_datetime(df_eia_trans.date, format='%Y-%m-%d')

df_eia_trans = df_eia_trans[(df_eia_trans.date > '2010-01-01') & (df_eia_trans.date < str(dt.now().date()))]

df = df.merge(df_eia_trans,how='outer').sort_values('date',ascending=False)

#***********************************************************#
# Download wti_fut_2 and merge with df (DAILY)
url_trans = url_eia + 'PET.RCLC2.D'
label = 'wti_fut_2'

r = requests.get(url_trans)
json_trans = r.json()

df_eia_trans = pd.DataFrame(list(json_trans['series'][0]['data']),columns=['date',label])
df_eia_trans.date = pd.to_datetime(df_eia_trans.date, format='%Y-%m-%d')

df_eia_trans = df_eia_trans[(df_eia_trans.date > '2010-01-01') & (df_eia_trans.date < str(dt.now().date()))]

df = df.merge(df_eia_trans,how='outer').sort_values('date',ascending=False)

#***********************************************************#
# Download wti_fut_3 and merge with df (DAILY)
url_trans = url_eia + 'PET.RCLC3.D'
label = 'wti_fut_3'

r = requests.get(url_trans)
json_trans = r.json()

df_eia_trans = pd.DataFrame(list(json_trans['series'][0]['data']),columns=['date',label])
df_eia_trans.date = pd.to_datetime(df_eia_trans.date, format='%Y-%m-%d')

df_eia_trans = df_eia_trans[(df_eia_trans.date > '2010-01-01') & (df_eia_trans.date < str(dt.now().date()))]

df = df.merge(df_eia_trans,how='outer').sort_values('date',ascending=False)

#***********************************************************#
# Download wti_fut_4 and merge with df (DAILY)
url_trans = url_eia + 'PET.RCLC4.D'
label = 'wti_fut_4'

r = requests.get(url_trans)
json_trans = r.json()

df_eia_trans = pd.DataFrame(list(json_trans['series'][0]['data']),columns=['date',label])
df_eia_trans.date = pd.to_datetime(df_eia_trans.date, format='%Y-%m-%d')

df_eia_trans = df_eia_trans[(df_eia_trans.date > '2010-01-01') & (df_eia_trans.date < str(dt.now().date()))]

df = df.merge(df_eia_trans,how='outer').sort_values('date',ascending=False)

#***********************************************************#
# Download usa_net_imp and merge with df (WEEKLY)
url_trans = url_eia + 'PET.WCRNTUS2.W'
label = 'usa_net_import'

r = requests.get(url_trans)
json_trans = r.json()

df_eia_trans = pd.DataFrame(list(json_trans['series'][0]['data']),columns=['date',label])
df_eia_trans.date = pd.to_datetime(df_eia_trans.date, format='%Y-%m-%d')

df_eia_trans = df_eia_trans[(df_eia_trans.date > '2010-01-01') & (df_eia_trans.date < str(dt.now().date()))]

df = df.merge(df_eia_trans,how='outer').sort_values('date',ascending=False)

#***********************************************************#
# Download usa_stocks_all and merge with df (WEEKLY)
url_trans = url_eia + 'PET.WCRSTUS1.W'
label = 'usa_stocks_all'

r = requests.get(url_trans)
json_trans = r.json()

df_eia_trans = pd.DataFrame(list(json_trans['series'][0]['data']),columns=['date',label])
df_eia_trans.date = pd.to_datetime(df_eia_trans.date, format='%Y-%m-%d')

df_eia_trans = df_eia_trans[(df_eia_trans.date > '2010-01-01') & (df_eia_trans.date < str(dt.now().date()))]

df = df.merge(df_eia_trans,how='outer').sort_values('date',ascending=False)

#***********************************************************#
# Download usa_stocks_spr and merge with df (WEEKLY)
url_trans = url_eia + 'PET.WCSSTUS1.W'
label = 'usa_stocks_spr'

r = requests.get(url_trans)
json_trans = r.json()

df_eia_trans = pd.DataFrame(list(json_trans['series'][0]['data']),columns=['date',label])
df_eia_trans.date = pd.to_datetime(df_eia_trans.date, format='%Y-%m-%d')

df_eia_trans = df_eia_trans[(df_eia_trans.date > '2010-01-01') & (df_eia_trans.date < str(dt.now().date()))]

df = df.merge(df_eia_trans,how='outer').sort_values('date',ascending=False)

#***********************************************************#
# Download usa_production and merge with df (WEEKLY)
url_trans = url_eia + 'PET.WCRFPUS2.W'
label = 'usa_production'

r = requests.get(url_trans)
json_trans = r.json()

df_eia_trans = pd.DataFrame(list(json_trans['series'][0]['data']),columns=['date',label])
df_eia_trans.date = pd.to_datetime(df_eia_trans.date, format='%Y-%m-%d')

df_eia_trans = df_eia_trans[(df_eia_trans.date > '2010-01-01') & (df_eia_trans.date < str(dt.now().date()))]

df = df.merge(df_eia_trans,how='outer').sort_values('date',ascending=False)

#***********************************************************#
# Download opec_production and merge with df (MONTHLY)
url_trans = url_eia + 'INTL.55-1-OPEC-TBPD.M'
label = 'opec_production'

r = requests.get(url_trans)
json_trans = r.json()

df_eia_trans = pd.DataFrame(list(json_trans['series'][0]['data']),columns=['date',label])
df_eia_trans.date = df_eia_trans.date + '01'
df_eia_trans.date = pd.to_datetime(df_eia_trans.date, format='%Y-%m')

df_eia_trans = df_eia_trans[(df_eia_trans.date > '2010-01-01') & (df_eia_trans.date < str(dt.now().date()))]

df = df.merge(df_eia_trans,how='outer').sort_values('date',ascending=False)

#***********************************************************#
# Download non-opec_production and merge with df (MONTHLY)
url_trans = url_eia + 'INTL.55-1-OPNO-TBPD.M'
label = 'non-opec_production'

r = requests.get(url_trans)
json_trans = r.json()

df_eia_trans = pd.DataFrame(list(json_trans['series'][0]['data']),columns=['date',label])
df_eia_trans.date = df_eia_trans.date + '01'
df_eia_trans.date = pd.to_datetime(df_eia_trans.date, format='%Y-%m')

df_eia_trans = df_eia_trans[(df_eia_trans.date > '2010-01-01') & (df_eia_trans.date < str(dt.now().date()))]

df = df.merge(df_eia_trans,how='outer').sort_values('date',ascending=False)

#***********************************************************#
# Download oecd_cons and merge with df (MONTHLY)
url_trans = url_eia + 'STEO.PATC_OECD.M'
label = 'oecd_cons'

r = requests.get(url_trans)
json_trans = r.json()

df_eia_trans = pd.DataFrame(list(json_trans['series'][0]['data']),columns=['date',label])
df_eia_trans.date = df_eia_trans.date + '01'
df_eia_trans.date = pd.to_datetime(df_eia_trans.date, format='%Y-%m')

df_eia_trans = df_eia_trans[(df_eia_trans.date > '2010-01-01') & (df_eia_trans.date < str(dt.now().date()))]

df = df.merge(df_eia_trans,how='outer').sort_values('date',ascending=False)

#***********************************************************#
# Download non-oecd_cons and merge with df (MONTHLY)
url_trans = url_eia + 'STEO.PATC_NON_OECD.M'
label = 'non-oecd_cons'

r = requests.get(url_trans)
json_trans = r.json()

df_eia_trans = pd.DataFrame(list(json_trans['series'][0]['data']),columns=['date',label])
df_eia_trans.date = df_eia_trans.date + '01'
df_eia_trans.date = pd.to_datetime(df_eia_trans.date, format='%Y-%m')

df_eia_trans = df_eia_trans[(df_eia_trans.date > '2010-01-01') & (df_eia_trans.date < str(dt.now().date()))]

df = df.merge(df_eia_trans,how='outer').sort_values('date',ascending=False)

#***********************************************************#
# 

