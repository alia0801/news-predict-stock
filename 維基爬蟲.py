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
from gensim import corpora, models, similarities
import codecs
import os
import logging

month = ["00","01","02","03","04","05","06","07","08","09","10","11","12"]
day = ["00","01","02","03","04","05","06","07","08","09","10",
            "11","12","13","14","15","16","17","18","19","20",
            "21","22","23","24","25","26","27","28","29","30","31"]
day_of_month = [ 31,29,31, 30,31,30, 31,31,30, 31,30,31]


jieba.set_dictionary("C:/Users/Alia/AppData/Local/Programs/Python/Python37/Lib/site-packages/jieba/dict.txt")

driver = webdriver.Chrome("D:/Alia/Downloads/108-1/project/chromedriver_win32/chromedriver.exe")
# for a in range(len(codes)):
for a in range(1):
    # driver = webdriver.Chrome("D:/Alia/Downloads/108-1/project/chromedriver_win32/chromedriver.exe")

    url = "https://zh.wikipedia.org/wiki/"
    url += '4'
    url += '月'
    url += '12'
    url += '日'

    print(url)
    driver.get(url)
    soup = bs(driver.page_source,"html.parser")
    
    raw_data = [data.text for data in soup.find_all("li")]
    print(raw_data)
    # driver.close()
    
    text = '\n'.join(raw_data)

driver.close()
print(text)