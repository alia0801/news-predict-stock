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

# https://udndata.com/ndapp/Searchdec?udndbid=udnfree&page=1&SearchString=%A5%78%BF%6E%B9%71%2B%A4%E9%B4%C1%3E%3D20100913%2B%A4%E9%B4%C1%3C%3D20200907%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8%7C%C1%70%A6%58%B1%DF%B3%F8%7CUpaper&sharepage=20&select=0&kind=2&showSearchString=  select=0遠->進
# https://udndata.com/ndapp/Searchdec?udndbid=udnfree&page=1&SearchString=%A5%78%BF%6E%B9%71%2B%A4%E9%B4%C1%3E%3D20100913%2B%A4%E9%B4%C1%3C%3D20200907%2B%B3%F8%A7%4F%3D%C1%70%A6%58%B3%F8%7C%B8%67%C0%D9%A4%E9%B3%F8%7C%C1%70%A6%58%B1%DF%B3%F8%7CUpaper&sharepage=20&select=1&kind=2&showSearchString=
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

for i in range(1):
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
print(len(headsss))
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
driver.close()
# print(news_url[330][:32])

# print(news_url[333])
# print(len(news_url[333]))



total_url = pd.DataFrame(news_url,columns=['url'])
# total_url = pd.concat([total_url, pd.DataFrame(heads,columns=['time'])],axis=1)
# total_url = pd.concat([total_url, pd.DataFrame(times,columns=['head'])],axis=1)

print(total_url)
# total_url.to_csv('D:/Alia/Downloads/108-2/project/台積電_聯合3.csv', index= False)

##########################爬新聞內容####################################
# starttime = datetime.datetime.now()
db = pymysql.connect("localhost", "root", "esfortest", "text_analysis")
cursor = db.cursor()
heads = []
dates = []
texts = []
i=0
# driver = webdriver.Chrome("D:/Alia/Downloads/108-1/project/chromedriver_win32/chromedriver.exe")

# for i in range(len(news_url)):
for i in range(10):
    # if i >= len(news_url):
    #     break
    print(i)
    driver = webdriver.Chrome("D:/Alia/Downloads/108-1/project/chromedriver_win32/chromedriver.exe")
    url = news_url[i]
    print(url)
    driver.get(url)
    url = driver.current_url
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
    
    else:
        # news_url.remove(news_url[i])
        # driver.close()
        # continue
        text = ' '
        head = ' '
        date = ' '
        continue
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

# print(texts)
# print(heads)
# print(dates)
# print(len(texts))
# print(news_url[10][:21])
# print(len('https://vision.udn.com/'))
# print(raw_data[0:len(raw_data)-1])
# print(time.strip())
# endtime = datetime.datetime.now()
# print((endtime-starttime).seconds)
##################################處理成csv#########################################################

