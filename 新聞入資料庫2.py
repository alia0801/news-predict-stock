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

newnews = pd.read_csv('D:/Alia/Downloads/108-2/project/資料庫備份/tsmc_udn_news_2.csv')
db = pymysql.connect("localhost", "root", "esfortest", "text_analysis")
cursor = db.cursor()
for i in range(len(newnews)):

    sql2="insert into `tsmc_udn_news` (`url`,`date`, `is_rise`,`head`,`text`, `text_and_head` ) VALUES"
    values = "('%s','%s',%f,'%s','%s','%s')"
    # print(newnews['date'][i])
    sql2 += values % (newnews['url'][i],newnews['date'][i],newnews['is_rise'][i],newnews['head'][i],newnews['text'][i],newnews['text_and_head'][i])
    # print(sql2)

    sql_select = "select * from `tsmc_udn_news` where head = '" +newnews['head'][i]+ "'"
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
        print('title is: ',newnews['head'][i])