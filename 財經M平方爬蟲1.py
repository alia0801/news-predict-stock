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

codes = ['1', '9', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21']
date=[]
text=[]
jieba.set_dictionary("C:/Users/Alia/AppData/Local/Programs/Python/Python37/Lib/site-packages/jieba/dict.txt")

driver = webdriver.Chrome("D:/Alia/Downloads/108-1/project/chromedriver_win32/chromedriver.exe")
# for a in range(len(codes)):
# for a in range(1):
# print(len(codes))
a=12
# print(codes[a])
# driver = webdriver.Chrome("D:/Alia/Downloads/108-1/project/chromedriver_win32/chromedriver.exe")
# url = "https://www.macromicro.me/time_line?id=17&stat=2"
url = "https://www.macromicro.me/time_line?id="
url += codes[a]
# url += '17'
url += '&stat=2'
print(url)
driver.get(url)
soup = bs(driver.page_source,"html.parser")

raw_data = [data.text for data in soup.find_all("td")]
print(raw_data)
# driver.close()
for i in range(len(raw_data)):
    if raw_data[i]=='':
        raw_data.pop(i)
        
for i in range(len(raw_data)):
    raw_data[i] = raw_data[i].strip().strip('事件超出商品區間')
    raw_data[i] = raw_data[i].strip().strip('事件尚未加入圖表')

print(raw_data)
# content = '\n'.join(raw_data)
# print(content)
# print(raw_data[0][10:])    

for i in range(len(raw_data)):
    date.append(raw_data[i][0:10])
    text.append(raw_data[i][10:])

# driver.close()
print(date)
print(text)
data = list(zip(date,text))
print(data)

pdframe = pd.DataFrame(data)
print(pdframe)



pdframe.to_csv('D:/Alia/Downloads/108-2/project/財經M平方/'+ codes[a] + '.csv', index= False)




pdframe_n = pdframe.sort_values(by=0)
pdframe_n = pdframe_n.rename(columns={0:'date',1:'text'})
print(pdframe_n)
pdframe_n.to_csv('D:/Alia/Downloads/108-2/project/財經M平方/total.csv', index= False)

# trainDF = pd.read_csv('D:/Alia/Downloads/108-2/project/財經M平方/'+ codes[a] + '.csv')
# print(trainDF)


