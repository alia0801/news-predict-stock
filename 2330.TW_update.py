from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import pymysql
import datetime
from selenium.webdriver.chrome.options import Options
from dateutil.parser import parse 
# month=['Jan','Feb']

driver = webdriver.Chrome("D:/Alia/Downloads/108-1/project/chromedriver_win32/chromedriver.exe")
# a=10
# for a in range(len(etf)):
# for a in range(16,24):
    
    # driver = webdriver.Chrome("D:/Alia/Downloads/108-1/project/chromedriver_win32/chromedriver.exe")
    
url = "https://finance.yahoo.com/quote/2330.TW/history?p=2330.TW"
# url += etf[a]
driver.get(url)
soup = bs(driver.page_source,"html.parser")

# raw_data = [data.text for data in soup.find_all("tr",["BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)"])]

raw_data = [data.text for data in soup.find_all("td",["Py(10px) Ta(start) Pend(10px)",'Py(10px) Pstart(10px)'])]
print(raw_data[0])
print(raw_data[4])
#print(raw_data[1])

# print(str(parse('January 31, 2010')))
date = str(parse(raw_data[0]))[:10]
# date = raw_data[0].strip().strip('市價()')
print(date)
close = raw_data[4].replace(',','')
print(close)
# close_arr[a] = close
driver.close()

sql="insert into `2330.tw` (`date`, `close` ) VALUES"
values = "('%s',%s)"
sql += values % (date,close)
print(sql)
# insert into `etf_close` (`name`,`date`, `close` ) VALUES('GOVT','2020-01-10',26.075001)
# insert into `etf_close` (`name`,`date`, `close` ) VALUES('VTI','2020/01/09',165.9400)
db = pymysql.connect("localhost", "root", "esfortest", "text_analysis")
cursor = db.cursor()
sql_select = "select * from `2330.tw` where date = '"+date+"'"
print(sql_select)
cursor.execute(sql_select)
result_select = cursor.fetchall()

print(result_select)


if  result_select == ():
    try:
        cursor.execute(sql)
        db.commit()
        print("Data are successfully inserted")
    except Exception as e:
        db.rollback()
        print("Exception Occured : ", e)
else:
    print('File already exists')

db.close()

# driver.close()
# print(a)
