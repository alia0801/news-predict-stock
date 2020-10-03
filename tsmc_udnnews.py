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

# url = 'https://udn.com/api/more?page=5&id=search:台積電&channelId=2&type=searchword&last_page=430'

##########################爬台積電的新聞網址####################################
# a=1
# url1 = "https://ec.ltn.com.tw/search/"
# url2 = '?keyword=台積電'
url = 'https://udn.com/search/word/2/台積電'

driver = webdriver.Chrome("D:/Alia/Downloads/108-1/project/chromedriver_win32/chromedriver.exe")

# for a in range(1,98):
# for a in range(1,6):
    # url = url1 + str(a) + url2
print(url)

driver.get(url)

for i in range(5):
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(1)


soup = bs(driver.page_source,"html.parser")
# headsss = [data.text for data in soup.find("div",'story-list__news').find("div",'story-list__text').find_all('h2')]
headsss = [data.text for data in soup.find_all("div",'story-list__text')]
t1 = soup.find('div','context-box__content story-list__holder story-list__holder--full').find_all('a')
# t1 = soup.find('section',class="story-list__holder--append").find_all('a')
# t1 = soup.find_all('a')
# t1 = soup.find_all('a','boxText')

# heads = [data.text for data in soup.find_all('h2')]
# t1 = soup.find_all('a')
# print(headsss[0].split('\n')[7])
# print(len(heads))
print(len(t1))
# print(t1)
# print(t1[4121].get('href')[0:21])


heads = []
times = []
for t2 in headsss:
    t = t2.split('\n')
    
    # print(t3)
    heads.append(t[2])
    times.append(t[len(t)-3])
    # count+=1
print(heads)
print(times)
print(len(times))
# hhh = headsss[0].split('\n')
# print(headsss[0].split('\n')[len(headsss[0].split('\n'))-3])
news_url = []
count = 0
# for t2 in t1:
for i in range(len(t1)):
    t2 = t1[i]
    t3 = t2.get('href')
    # print(t3)
    if(count==3):
        print('gogo')
        # print(count)
        news_url.append(t3)
        count = 0
    if(i<len(t1)-1 ):
        ttttt = t1[i+1].get('href')
        print(ttttt)
        if ttttt[21:25]!='cate' and len(ttttt)>28:
            count+=1
            print(count)
# print(t1[i].get('href'))
print(len(news_url))
print(news_url[330][:32])

# print(news_url[333])
# print(len(news_url[333]))



total_url = pd.DataFrame(news_url,columns=['url'])
# total_url = pd.concat([total_url, pd.DataFrame(heads,columns=['time'])],axis=1)
# total_url = pd.concat([total_url, pd.DataFrame(times,columns=['head'])],axis=1)

print(total_url)
total_url.to_csv('D:/Alia/Downloads/108-2/project/台積電_聯合3.csv', index= False)

##########################爬新聞內容####################################
starttime = datetime.datetime.now()

heads = []
dates = []
texts = []
i=0
for i in range(len(news_url)):
# for i in range(330,331):
    print(i)
    driver = webdriver.Chrome("D:/Alia/Downloads/108-1/project/chromedriver_win32/chromedriver.exe")
    url = news_url[i]
    print(url)
    driver.get(url)
    soup = bs(driver.page_source,"html.parser")
    
    if (url[:21] == 'https://udn.com/news/'):

        raw_data = [data.text for data in soup.find("section",'article-content__editor').find_all('p')]
        print(raw_data)
        text1 = ''.join(raw_data[0:len(raw_data)-1])
        text = ''.join( text1.split('\n') )

        raw_data = [data.text for data in soup.find_all("time",'article-content__time')]
        print(raw_data)
        time = raw_data[0]
        date = time[:10]

        raw_data = [data.text for data in soup.find_all("h1",'article-content__title')]
        print(raw_data)
        head = raw_data[0]
        

    elif(url[:23] == 'https://vision.udn.com/'):

        raw_data = [data.text for data in soup.find("div",id='story_body_content').find_all('p')]
        print(raw_data)
        text = ''.join(raw_data)

        raw_data = [data.text for data in soup.find_all("div","shareBar__info--author")]
        print(raw_data)
        time = raw_data[0]
        date = time[:10]

        raw_data = [data.text for data in soup.find_all("h1","story_art_title")]
        print(raw_data)
        head = raw_data[0]

    elif(url[:30] == 'https://ubrand.udn.com/ubrand/'):

        raw_data = [data.text for data in soup.find("div",'story_body_content').find_all('p')]
        print(raw_data)
        text1 = ''.join(raw_data[0:len(raw_data)-25])
        text = ''.join( text1.split('\n') )

        raw_data = [data.text for data in soup.find_all("div","story_bady_info_author")]
        print(raw_data)
        time = raw_data[0].strip()
        date = time[:4]+'-'+time[5:7]+'-'+time[8:10]

        raw_data = [data.text for data in soup.find_all("h1","story_art_title")]
        print(raw_data)
        head = raw_data[0]
    
    elif(url[:30] == 'https://health.udn.com/health/' or url[:21] == 'https://fund.udn.com/' or url[:28] == 'https://house.udn.com/house/'):

        raw_data = [data.text for data in soup.find("div",id='story_body_content').find_all('p')]
        print(raw_data)
        if url[:30] == 'https://health.udn.com/health/':
            text1 = ''.join(raw_data[0:len(raw_data)-18])
        else:
            text1 = ''.join(raw_data)
        text = ''.join( text1.split('\n') )

        raw_data = [data.text for data in soup.find_all("div","shareBar__info--author")]
        print(raw_data)
        time = raw_data[0]
        date = time[:10]

        raw_data = [data.text for data in soup.find_all("h1","story_art_title")]
        print(raw_data)
        head = raw_data[0]
    
    elif(url[:23] == 'https://udn.com/umedia/'):

        raw_data = [data.text for data in soup.find("div",'article-content article-content-common').find_all('p')]
        print(raw_data)
        text1 = ''.join(raw_data)
        text = ''.join( text1.split('\n') )

        raw_data = [data.text for data in soup.find_all("div","article-info")]
        print(raw_data)
        time = raw_data[0]
        date = time[:10]

        raw_data = [data.text for data in soup.find_all("h1","article-title")]
        print(raw_data)
        head = raw_data[0]

    elif(url[:32] == 'https://opinion.udn.com/opinion/'):

        raw_data = [data.text for data in soup.find("main").find_all('p')]
        print(raw_data)
        text1 = ''.join(raw_data[0:len(raw_data)-10])
        text = ''.join( text1.split('\n') )

        raw_data = soup.find_all("time")
        print(raw_data)
        # time = raw_data[0]
        date = raw_data[0].get('datetime')

        raw_data = [data.text for data in soup.find_all("h1","story_art_title")]
        print(raw_data)
        head = raw_data[0]
    
    
    # print(text)
    # print(head)
    # print(date)
    texts.append(text)
    heads.append(head)
    dates.append(date)
    driver.close()
# print(texts)
print(heads)
print(dates)
print(len(texts))
# print(news_url[10][:21])
# print(len('https://vision.udn.com/'))
# print(raw_data[0:len(raw_data)-1])
# print(time.strip())
endtime = datetime.datetime.now()
print((endtime-starttime).seconds)
##################################處理成csv#########################################################

# news_from_file = pd.read_csv('D:/Alia/Downloads/108-2/project/台積電_新聞.csv')
# print(news_from_file)

# heads = news_from_file['head']
# times = news_from_file['time']
# texts = news_from_file['text']
# print(heads)
# print(times)
# print(texts)

#取新聞日期
# date = []
# j=0
# # print(times[j][5])
# for j in range(len(times)):
#     t = times[j][:10]
#     date.append(t)
# print(date)

prices = pd.read_csv('D:/Alia/Downloads/108-2/project/^TWII.csv')#台股大盤
print(prices)
cat = []
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
prices = pd.concat([prices, pd.DataFrame(cat,columns=['cat'])],axis=1)


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

print(len(heads))


# 對照新聞日期與price日期
rise_percent = []
j=0
for j in range(len(heads)):
    ddd = datetime.date(int(dates[j][:4]),int(dates[j][5:7]),int(dates[j][8:10]))
    if dates[j] in list(p_date):
        index = list(p_date).index(dates[j])
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
for j in range(len(dates)):
    ttt = heads[j] + texts[j]
    text_and_head.append(ttt)
# print(text_and_head[0])

# 將所有資料合併成一個檔
news = pd.concat([total_url, pd.DataFrame(dates,columns=['date'])],axis=1)
# news = pd.concat([news, pd.DataFrame(times,columns=['time'])],axis=1)
news = pd.concat([news, pd.DataFrame(rise_percent,columns=['is_rise'])],axis=1)
news = pd.concat([news, pd.DataFrame(heads,columns=['head'])],axis=1)
news = pd.concat([news, pd.DataFrame(texts,columns=['text'])],axis=1)
news = pd.concat([news, pd.DataFrame(text_and_head,columns=['text_and_head'])],axis=1)
print(news)


news.to_csv('D:/Alia/Downloads/108-2/project/台積電_聯合_新聞2.csv', index= False)
print(news)

#擷取要丟入模型的部份存檔
new_to_model = news.drop(['url'],axis=1)
new_to_model = new_to_model.drop(['date'],axis=1)
# new_to_model = new_to_model.drop(['time'],axis=1)
new_to_model = new_to_model.drop(['head'],axis=1)
new_to_model = new_to_model.drop(['text'],axis=1)
# new_to_model = new_to_model.drop(['cat'],axis=1)
new_to_model = new_to_model.rename(columns={'is_rise':'cat'})
new_to_model = new_to_model.rename(columns={'text_and_head':'text'})
print(new_to_model)
new_to_model.to_csv('D:/Alia/Downloads/108-2/project/news_to_model_udn_n.csv', index= False)


