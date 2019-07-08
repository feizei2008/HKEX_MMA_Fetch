# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 13:55:07 2017

@author: zack zhang
"""
from retrying import retry
from threading import Timer
import logging
import os
from retrying import retry
from collections import OrderedDict
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from business_calendar import Calendar#, MO, TU, WE, TH, FR

#@retry(stop_max_attempt_number=15, wait_exponential_multiplier=5000, wait_exponential_max=40000) 
def workdaydic(start, end):
    "start = '2017/03/17', end = '2017/06/02'"
    "返回的工作日含start不含end"
    cal = Calendar()
    daterange = cal.range(start,end)
    L = []
    [L.append(i) for i in map(lambda x: x.strftime("%Y-%m-%d"),daterange)]
    DateDictList = OrderedDict()
    for i in L:    
        if DateDictList.has_key(i) is False: 
            DateDictList[i] = {}    
            DateDictList[i]['Year'] = i.split('-')[0]
            DateDictList[i]['Month'] = i.split('-')[1]
            DateDictList[i]['Day'] = i.split('-')[2]
        else:
            print 'date dic process completed'
    return DateDictList

dic2017 = workdaydic(start = '2017/03/27', end = '2017/10/01')
LL = dic2017.values()
    
def processdata():
    driver =  webdriver.PhantomJS(executable_path=r'D:\phantomjs-2.1.1-windows\bin\phantomjs.exe')#.Firefox()
    url = 'http://www.hkexnews.hk/sdw/search/mutualmarket.aspx?t=sh'    
    for i in LL:
        try:
            driver.get(url)
            driver.implicitly_wait(30)   
            Select(driver.find_element_by_id("ddlShareholdingDay")).select_by_visible_text(i['Day'])
            Select(driver.find_element_by_id("ddlShareholdingMonth")).select_by_visible_text(i['Month'])
            Select(driver.find_element_by_id("ddlShareholdingYear")).select_by_visible_text(i['Year'])
            driver.find_element_by_id("btnSearch").click()    
            data = pd.read_html(driver.page_source)
            table1 = data[-1].dropna().iloc[1:,:]
            d = data[-1].iloc[0,:].to_dict()
            table1.rename(columns = d, inplace = True)
            format = lambda x: str(x)[-7:-1]+'.SH' 
            table1['Symbol'] = table1.iloc[:,1].map(format)
            table1.to_csv('MMA_SH%s%s%s.csv' % (i['Year'],i['Month'],i['Day']))
            driver.quit()            
            LL.remove(i)
        except:
            pass
            driver.quit()
#            path = os.path.abspath(os.path.dirname(__file__))
#            File = path+'\%s%s%s.txt'% (i['Year'],i['Month'],i['Day'])
#            f = open(File, 'w')
#            f.close()
    t = Timer(1,processdata)
    t.start()
          
if __name__ == "__main__": 
    processdata()    

''' 
直接读取沪港通网页        
url = 'http://www.hkexnews.hk/sdw/search/mutualmarket.aspx?t=sh'
#response = urllib2.urlopen(url).read().decode('utf8',errors='replace')
data = pd.read_html(url)
table1 = data[2].dropna().iloc[1:,:]
#d = {0: 'StockCode', 1: 'Stock Name', 2: 'Shareholding inCCASS', 
#     3: '% of the total number of A shareslisted and traded on the SSE'}
d = data[2].iloc[0,:].to_dict()
table1.rename(columns = d, inplace = True)
#table1.columns = ['StockCode', 'Stock Name', 'Shareholding inCCASS',
#                  '% of the total number of A shareslisted and traded on the SSE']
format = lambda x: str(x)[-7:-1]+'.SH' 
table1['Symbol'] = table1.iloc[:,1].map(format)
table1.to_csv('MMA_SH.csv')
'''

''' 
直接读取深港通网页
url2 = 'http://www.hkexnews.hk/sdw/search/mutualmarket.aspx?t=sz'
#response = urllib2.urlopen(url).read().decode('utf8',errors='replace')
data2 = pd.read_html(url2)
table2 = data2[2].dropna().iloc[1:,:]
#d = {0: 'StockCode', 1: 'Stock Name', 2: 'Shareholding inCCASS', 
#     3: '% of the total number of A shareslisted and traded on the SSE'}
d2 = data2[2].iloc[0,:].to_dict()
table2.rename(columns = d2, inplace = True)
#table1.columns = ['StockCode', 'Stock Name', 'Shareholding inCCASS',
#                  '% of the total number of A shareslisted and traded on the SSE']
format2 = lambda x: str(x)[-7:-1]+'.SZ' 
table2['Symbol'] = table2.iloc[:,1].map(format2)
table2.to_csv('MMA_SZ.csv')
'''
    
