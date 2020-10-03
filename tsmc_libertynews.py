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

##########################爬台積電的新聞網址####################################
a=1
url1 = "https://ec.ltn.com.tw/search/"
url2 = '?keyword=台積電'
news_url = []
driver = webdriver.Chrome("D:/Alia/Downloads/108-1/project/chromedriver_win32/chromedriver.exe")

for a in range(1,98):
# for a in range(1,6):
    url = url1 + str(a) + url2
    print(url)
    
    driver.get(url)
    soup = bs(driver.page_source,"html.parser")
    
    t1 = soup.find_all('a','boxText')
    # print(t1)
    count = 0
    
    for t2 in t1:
        if(count>=20):
            break
        t3 = t2.get('href')
        # print(t3)
        if(t3=='https://www.ltn.com.tw/' or t3=='https://ec.ltn.com.tw/' or '//ec.ltn.com.tw/search' in t3):
            continue
        news_url.append(t3)
        count+=1
print(news_url)
print(len(news_url))

total_url = pd.DataFrame(news_url,columns=['url'])
print(total_url)
total_url.to_csv('D:/Alia/Downloads/108-2/project/台積電_自由時報.csv', index= False)

##########################爬新聞內容####################################


# t='//ec.ltn.com.tw/search/'
# print(t[0:23])
# print('//ec.ltn.com.tw/search/' not in t3)
heads = []
times = []
texts = []
i=0
for i in range(650,len(news_url)):
    driver = webdriver.Chrome("D:/Alia/Downloads/108-1/project/chromedriver_win32/chromedriver.exe")

    url = news_url[i]
    driver.get(url)
    soup = bs(driver.page_source,"html.parser")
    raw_data = [data.text for data in soup.find_all("h1")]
    head = raw_data[0].strip()
    print(head)
    heads.append(head)
    
    raw_data = [data.text for data in soup.find_all("span",'time')]
    time = raw_data[0]
    print(time)
    times.append(time)
    
    # print(soup.find_all("div",'text'))
    # texts = bs(soup.find_all("div",'text'))
    raw_data = [data.text for data in soup.find("div",'text').find_all('p')]
    print(raw_data)
    text = ''.join(raw_data)
    # print(text)
    text = text.strip().strip('按我看活動辦法')
    text = text.strip().strip('點我下載APP')
    text = text.strip().strip('不用抽 不用搶 現在用APP看新聞 保證天天中獎')
    text = text.strip().strip('點我訂閱自由財經Youtube頻道')
    text = text.strip().strip('一手掌握經濟脈動')
    text = text.strip()
    print(text)
    texts.append(text)
    driver.close()

print(i)
# print(len(news_url))
print(heads)
print(times)
print(texts)


##################################處理成csv#########################################################

news_from_file = pd.read_csv('D:/Alia/Downloads/108-2/project/台積電_新聞.csv')
print(news_from_file)

heads = news_from_file['head']
times = news_from_file['time']
texts = news_from_file['text']
print(heads)
print(times)
print(texts)

date = []
j=0
print(times[j][5])
for j in range(len(times)):
    t = times[j][:10]
    # d=t[:4]
    # if(t[5]=='0'):
    #     d=d+'/'+t[6:7]
    # else:
    #     d=d+'/'+t[5:7]
    # if(t[8]=='0'):
    #     d=d+'/'+t[9:10]
    # else:
    #     d=d+'/'+t[8:10]
    # d=t[:4]+'/'+t[5:7]+'/'+t[8:10]
    date.append(t)
print(date)


# prices = pd.read_csv('D:/Alia/Downloads/108-2/project/2330.TW.csv')
prices = pd.read_csv('D:/Alia/Downloads/108-2/project/^TWII.csv')#台股大盤
print(prices)
cat = []
# for j in range(len(prices['Date'])):
#     if prices['%'][j]=='#VALUE!':
#         cat.append('-100')
#     elif float(prices['%'][j])==0:
#         cat.append('0')
#     elif float(prices['%'][j])>0 and float(prices['%'][j])<=0.03:
#         cat.append('1')
#     elif float(prices['%'][j])>0.03 and float(prices['%'][j])<=0.06:
#         cat.append('2')
#     elif float(prices['%'][j])>0.06:
#         cat.append('3')
#     elif float(prices['%'][j])<0 and float(prices['%'][j])>=-0.03:
#         cat.append('-1')
#     elif float(prices['%'][j])<-0.03 and float(prices['%'][j])>=-0.06:
#         cat.append('-2')
#     elif float(prices['%'][j])<-0.06:
#         cat.append('-3')
for j in range(len(prices['Date'])):
    if prices['rise_percent'][j]=='#VALUE!':
        cat.append('-100')
    elif float(prices['rise_percent'][j])==0:
        cat.append('0')
    elif float(prices['rise_percent'][j])>0 :
        cat.append('1')
    elif float(prices['rise_percent'][j])<0 :
        cat.append('-1')
print(cat)
# cat.append('-100')

prices = pd.concat([prices, pd.DataFrame(cat,columns=['cat'])],axis=1)
# print(prices)
# prices['is_rise'][5093]=0
# ddd=list(prices['Date'])
# print(prices['%'][3])
# print(times[0][5:7])
# print(datetime.date(int(times[0][0:4]),int(times[0][5:7]),int(times[0][8:10])))
# print(prices['Date'])

# 轉prices日期格式
p_date = []
j=0
# print(len(prices['Date'][5]))
for j in range(len(prices['Date'])):
    t = prices['Date'][j]
    d=t[:4]
    if(t[6]=='/'):#個位數月份
        d=d+'-0'+t[5]
        if(len(t)==8):#個位數日
            d=d+'-0'+t[7]
        else:
            d=d+'-'+t[7:]
    else:
        d=d+'-'+t[5:7]
        if(len(t)==9):#個位數日
            d=d+'-0'+t[8]
        else:
            d=d+'-'+t[8:]
    
    # d=t[:4]+'/'+t[5:7]+'/'+t[8:10]
    p_date.append(d)
print(p_date)
# print(prices['Date'])

print(date)#新聞日期
j=0
# ddd = datetime.date(int(date[j][:4]),int(date[j][5:7]),int(date[j][8:10]))
# ddd = ddd + datetime.timedelta(days=1)
# print(ddd)
# 對照新聞日期與price日期
rise_percent = []
for j in range(len(times)):
    ddd = datetime.date(int(date[j][:4]),int(date[j][5:7]),int(date[j][8:10]))
    if date[j] in list(p_date):
        index = list(p_date).index(date[j])
        # rise_percent.append(prices['is_rise'][index])
        rise_percent.append(cat[index])
        # print(index)
    else:
        # ddd = ddd + datetime.timedelta(days=1)
        while((str(ddd) in list(p_date))==False):
            ddd = ddd + datetime.timedelta(days=1)
        index = list(p_date).index(str(ddd))
        # rise_percent.append(prices['is_rise'][index])
        rise_percent.append(cat[index])
print(rise_percent)

#合併標題與內文
text_and_head = []
for j in range(len(times)):
    ttt = heads[j] + texts[j]
    text_and_head.append(ttt)
print(text_and_head[0])
# print(date[10] in list(prices['Date']))
# print(type(prices['Date']))

# print(list(prices['Date']).index(date[10]))
# news.to_csv('D:/Alia/Downloads/108-2/project/台積電_新聞.csv', index= False)
# print(news)
# print(total_url)
# 將所有資料合併成一個檔
news = pd.concat([total_url, pd.DataFrame(date,columns=['date'])],axis=1)
news = pd.concat([news, pd.DataFrame(times,columns=['time'])],axis=1)
news = pd.concat([news, pd.DataFrame(rise_percent,columns=['is_rise'])],axis=1)
news = pd.concat([news, pd.DataFrame(heads,columns=['head'])],axis=1)
news = pd.concat([news, pd.DataFrame(texts,columns=['text'])],axis=1)
news = pd.concat([news, pd.DataFrame(text_and_head,columns=['text_and_head'])],axis=1)
print(news)

news.to_csv('D:/Alia/Downloads/108-2/project/台積電_自由_新聞.csv', index= False)
print(news)

#擷取要丟入模型的部份存檔
new_to_model = news.drop(['url'],axis=1)
new_to_model = new_to_model.drop(['date'],axis=1)
new_to_model = new_to_model.drop(['time'],axis=1)
new_to_model = new_to_model.drop(['head'],axis=1)
new_to_model = new_to_model.drop(['text'],axis=1)
# new_to_model = new_to_model.drop(['cat'],axis=1)
new_to_model = new_to_model.rename(columns={'is_rise':'cat'})
new_to_model = new_to_model.rename(columns={'text_and_head':'text'})
print(new_to_model)
new_to_model.to_csv('D:/Alia/Downloads/108-2/project/news_to_model3.csv', index= False)

