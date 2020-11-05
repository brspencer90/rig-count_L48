# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 14:13:36 2020

@author: Bryan
"""

import requests
from bs4 import BeautifulSoup as soup
import win32com.client as win32

data_external_dir = 'C:\\Users\\Bryan\\OneDrive\\02 GitHub\\rig-count_L48\\data\\external\\'

url = 'https://rigcount.bakerhughes.com/na-rig-count'

dinner = soup(requests.get(url).text,'lxml')

file_tag = dinner.find('a', text='North America Rotary Rig Count (Jan 2000 - Current)')

file_link = file_tag['href']

res = requests.get(file_link)

file_d_name = 'nam_rig-count'

with open(data_external_dir+file_d_name+'.xlsb','wb') as local:
    for chunk in res.iter_content(chunk_size=128):
        local.write(chunk)
      
#excel = win32.gencache.EnsureDispatch('Excel.Application')
#wb = excel.Workbooks.Open(data_external_dir+file_d_name)

#wb.SaveAs(data_external_dir+file_d_name+".xlsx", FileFormat = 51)   #FileFormat = 51 is for .xlsx extension
#wb.Close()                                                          #FileFormat = 56 is for .xls extension
#excel.Application.Quit()