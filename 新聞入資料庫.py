from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import pymysql
import datetime
from selenium.webdriver.chrome.options import Options

db = pymysql.connect("localhost", "root", "esfortest", "text_analysis")
cursor = db.cursor()

df = pd.read_csv('D:/Alia/Downloads/108-2/project/台積電_自由_新聞.csv')
print(len(df))
print(df)
print(df['url'][0])

# values % ()
# for j in range(len(df['Date'])):
# for i in range(1):
for i in range(len(df)):
    sql2="insert into `tsmc_liberity_news` (`url`,`date`, `is_rise`,`head`,`text`, `text_and_head` ) VALUES"
    values = "('%s','%s',%f,'%s','%s','%s')"
    #print(etf[i],result_select[0][0])
    #sql2 += values % (etf[i],result_select[0][0],result_select[0][i+1])
    
    sql2 += values % (df['url'][i],df['date'][i],df['is_rise'][i],df['head'][i],df['text'][i],df['text_and_head'][i])
    # print(sql2)
    try:
        cursor.execute(sql2)
        db.commit()
        print("Data are successfully inserted")
    except Exception as e:
        db.rollback()
        print("Exception Occured : ", e)

