from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import pymysql
import datetime
from selenium.webdriver.chrome.options import Options
import jieba
import jieba.analyse
import matplotlib.pyplot as plt
from wordcloud import WordCloud
# from gensim import corpora, models, similarities
import codecs
import os
import logging
import time

db = pymysql.connect("localhost", "root", "esfortest", "text_analysis")
cursor = db.cursor()
heads = []
dates = []
texts = []
i=0
# driver = webdriver.Chrome("D:/Alia/Downloads/108-1/project/chromedriver_win32/chromedriver.exe")
# https://theme.udn.com/theme/story/6538/221532
# https://theme.udn.com/theme/story/6538/221516
# https://theme.udn.com/theme/story/6465/221549
# https://theme.udn.com/theme/story/6445/221292
# https://theme.udn.com/theme/story/6439/220959
# https://theme.udn.com/theme/story/6439/220954
# https://theme.udn.com/theme/story/6439/220957
# https://theme.udn.com/theme/story/6543/221459
# https://theme.udn.com/theme/story/6439/220871
# https://theme.udn.com/theme/story/6439/220874
# https://theme.udn.com/theme/story/6445/220723
# https://theme.udn.com/theme/story/6439/220693
# https://theme.udn.com/theme/story/6267/219739
# for i in range(len(news_url)):
# for i in range(10):
    # if i >= len(news_url):
    #     break

# print(i)
driver = webdriver.Chrome("D:/Alia/Downloads/108-1/project/chromedriver_win32/chromedriver.exe")
# url = news_url[i]
url = 'https://theme.udn.com/theme/story/6267/219739'
print(url)
driver.get(url)
url = driver.current_url
soup = bs(driver.page_source,"html.parser")

raw_data = [data.text for data in soup.find("div",id="story_body_content").find_all('p')]
print(raw_data)
text = ''.join(raw_data)
raw_data = [data.text for data in soup.find("div",'shareBar__info--author').find_all('span')]
print(raw_data)
# time = raw_data[0]
date = raw_data[0][:10]
raw_data = [data.text for data in soup.find_all("h1",id="story_art_title")]
print(raw_data)
head = raw_data[0]
print(text)
print(head)
print(date)
texts.append(text)
heads.append(head)
dates.append(date)
driver.close()

sql2="insert into `tsmc_udn_news` (`url`,`date`, `is_rise`,`head`,`text`, `text_and_head` ) VALUES"
values = "('%s','%s',%f,'%s','%s','%s')"
#print(etf[i],result_select[0][0])
#sql2 += values % (etf[i],result_select[0][0],result_select[0][i+1])

# print(newnews['date'][i])
sql2 += values % (url,date,0,head,text,head+text)
# print(sql2)
sql_select = "select * from `tsmc_udn_news` where head = '" +head+ "'"
# print(sql_select)
cursor.execute(sql_select)
result_select = cursor.fetchall()

# print(result_select)
if  result_select == ():
    try:
        cursor.execute(sql2)
        db.commit()
        print("Data are successfully inserted")
    except Exception as e:
        db.rollback()
        print("Exception Occured : ", e)
else:
    print('File already exists')
    print('title is: ',head)