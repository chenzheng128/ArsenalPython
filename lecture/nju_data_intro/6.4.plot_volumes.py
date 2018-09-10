# -*- coding: utf-8 -*-
"""
plot volumes
# Filename: plot_volumes.py
 
@author: Dazhuang
"""
 
import requests
import re
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
import time
 
def retrieve_quotes_historical(stock_code):
    quotes = []
    url = 'http://finance.yahoo.com/quote/%s/history?p=%s' % (stock_code, stock_code)
    r = requests.get(url)
    m = re.findall('"HistoricalPriceStore":{"prices":(.*?),"isPending"', r.text)
    if m:
        quotes = json.loads(m[0])
        quotes = quotes[::-1]
    return  [item for item in quotes if not 'type' in item]
 
def create_volumes(stock_code):
    quotes = retrieve_quotes_historical(stock_code)
    list1 = []
    for i in range(len(quotes)):
        x = date.fromtimestamp(quotes[i]['date'])
        y = date.strftime(x,'%Y-%m-%d')   
        list1.append(y)
    quotesdf_ori = pd.DataFrame(quotes, index = list1)
    listtemp = []
    for i in range(len(quotesdf_ori)):
        temp = time.strptime(quotesdf_ori.index[i],"%Y-%m-%d")
        listtemp.append(temp.tm_mon)
    tempdf = quotesdf_ori.copy()
    tempdf['month'] = listtemp
    totalvolume = tempdf.groupby('month').volume.sum()
    return totalvolume
                   
INTC_volumes = create_volumes('INTC')
IBM_volumes = create_volumes('IBM')
quotesIIdf = pd.DataFrame()
quotesIIdf['INTC'] = INTC_volumes
quotesIIdf['IBM'] = IBM_volumes
quotesIIdf.plot(kind = 'bar')
plt.show()