#%%
from selenium import webdriver
import time
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import pymysql
import datetime
from selenium.webdriver.chrome.options import Options
import requests

from dateutil.parser import parse 
from datetime import timedelta, datetime
from opencc import OpenCC
cc = OpenCC('s2tw')

import datetime
today = datetime.date.today()
# td_str = today.strftime("%Y/%m/%d")
#%%

start_y = 2020
start_m = 5
start_d = 20
start_date = '5/20/2020'
end_y = 2020
end_m = 5
end_d = 21
end_date = '5/21/2020'
target = '台積電'
# n=40
# url = 'https://www.google.com/search?q='+target+'&tbs=cdr:1,cd_min:'+start_date+',cd_max:'+end_date+'&tbm=nws&sxsrf=ALeKk02AolXyZwmpudqqKgoh8rZjq1Cgpg:1599494770895&ei=clpWX8qbNrmSr7wP56ibqA0&start='+str(n)+'&sa=N&ved=0ahUKEwjKnI6tttfrAhU5yYsBHWfUBtU4ChDy0wMIhAE&biw=802&bih=682&dpr=1.25'
# https://www.google.com/search?q=台積電&tbs=cdr:1,cd_min:3/20/2020,cd_max:4/21/2020&tbm=nws&sxsrf=ALeKk02AolXyZwmpudqqKgoh8rZjq1Cgpg:1599494770895&ei=clpWX8qbNrmSr7wP56ibqA0&start=20&sa=N&ved=0ahUKEwjKnI6tttfrAhU5yYsBHWfUBtU4ChDy0wMIhAE&biw=802&bih=682&dpr=1.25
# https://www.google.com/search?q=台積電&tbs=cdr:1,cd_min:3/20/2020,cd_max:4/21/2020&tbm=nws&sxsrf=ALeKk01XbL1QBC-zPO9rMs28GnFoZwfZCA:1599492774739&ei=plJWX6ndLNXdmAWhhr_4Aw&start=10&sa=N&ved=0ahUKEwipyKL1rtfrAhXVLqYKHSHDDz8Q8tMDCIIB&biw=802&bih=682&dpr=1.25
# url = 'https://www.google.com/search?q='+target+'&biw=1536&bih=682&sxsrf=ALeKk034tLnJ3LnO_fUVL5x-RhMI4vQFXQ%3A1599492685231&source=lnt&tbs=cdr%3A1%2Ccd_min%3A'+str(start_m)+'%2F'+str(start_d)+'%2F'+str(start_y)+'%2Ccd_max%3A'+str(end_m)+'%2F'+str(end_d)+'%2F'+str(end_y)+'&tbm=nws'

driver = webdriver.Chrome("D:/Alia/Downloads/108-1/project/chromedriver_win32/chromedriver.exe")

news_url=[]
# today - datetime.timedelta(days=1)

# for b in range(1826):
for b in range(3):
    #變換日期
    if b==0:
        end_date = today
        start_date = today - datetime.timedelta(days=1)
    else:
        end_date = start_date
        start_date = start_date - datetime.timedelta(days=1)

    start_date_str = start_date.strftime("%m/%d/%Y")
    end_date_str = end_date.strftime("%m/%d/%Y")

    for i in range(3):
        #換頁
        n=i*10
        url = 'https://www.google.com/search?q='+target+'&tbs=cdr:1,cd_min:'+start_date_str+',cd_max:'+end_date_str+'&tbm=nws&sxsrf=ALeKk02AolXyZwmpudqqKgoh8rZjq1Cgpg:1599494770895&ei=clpWX8qbNrmSr7wP56ibqA0&start='+str(n)+'&sa=N&ved=0ahUKEwjKnI6tttfrAhU5yYsBHWfUBtU4ChDy0wMIhAE&biw=802&bih=682&dpr=1.25'
        # print(url)
        driver.get(url)
        time.sleep(5)
        soup = bs(driver.page_source,"html.parser")
    
        t1 = soup.find_all('div',"dbsr")
        
        for i in range(len(t1)):
            news_url.append(t1[i].find('a').get('href'))
print(news_url)

total_url = pd.DataFrame(news_url,columns=['url'])
print(total_url)
total_url.to_csv('D:/Alia/Downloads/108-2/project/google_news_url.csv', index= False)
# total_url = pd.read_csv('D:/Alia/Downloads/108-2/project/google_news_url.csv')
total_url = pd.read_csv('D:/Alia/Downloads/108-2/project/google_news_url_2010.csv')

news_url = list(total_url['url'])

db = pymysql.connect("localhost", "root", "esfortest", "text_analysis")
cursor = db.cursor()
#%%
texts=[]
heads=[]
dates=[]

for i in range(len(news_url)):
# for i in range(1):
# for i in space2:    

    print(i)
    driver = webdriver.Chrome("D:/Alia/Downloads/108-1/project/chromedriver_win32/chromedriver.exe")
    url = news_url[i]
    print(url)

    if (url[:20] == 'https://tech.qq.com/' or url[:27] == 'https://article.pchome.net/' or url == 'http://www.techweb.com.cn/tech/2010-07-23/647128.shtml'):
        driver.close()
        text = ' '
        head = ' '
        date = ' '
        # texts[i] = text
        # heads[i] = head
        # dates[i] = date
        texts.append(text)
        heads.append(head)
        dates.append(date)
        continue

    driver.get(url)
    # url = driver.current_url
    soup = bs(driver.page_source,"html.parser")

    if (url[:28] == 'https://news.cnyes.com/news/'):#鉅亨網
        
        #內文
        raw_data = [data.text for data in soup.find("div","_1UuP").find_all('p')]
        print(raw_data)
        text1 = ''.join(raw_data[0:len(raw_data)-1])
        text = ''.join( text1.split('\n') )

        #日期
        raw_data = [data.text for data in soup.find_all("time")]
        print(raw_data)
        time = raw_data[0]
        date = time[:4]+'-'+time[5:7]+'-'+time[8:10]

        #標題
        raw_data = [data.text for data in soup.find_all("h1")]
        print(raw_data)
        head = raw_data[0]
    
    elif (url[:29] == 'https://www.ettoday.net/news/'):#ettoday
        
        #內文
        raw_data = [data.text for data in soup.find("div","story").find_all('p')]
        print(raw_data)
        text1 = ''.join(raw_data[0:len(raw_data)])
        text = ''.join( text1.split('\n') )
        
        #日期
        # raw_data = [data.text for data in soup.find("time",'date')]
        raw_data = [data for data in soup.find("time",'date')]
        print(raw_data)
        time = raw_data[0].strip('\n').strip(' ')
        date = time[:4]+'-'+time[5:7]+'-'+time[8:10]
        
        #標題
        raw_data = [data.text for data in soup.find_all("h1",'title')]
        print(raw_data)
        head = raw_data[0]

    elif (url[:26] == 'https://tw.news.yahoo.com/'):#yahoo
        
        #內文
        raw_data = [data.text for data in soup.find("div","canvas-body Wow(bw) Cl(start) Mb(20px) Lh(1.7) Fz(18px) D(i)").find_all('p')]
        print(raw_data)
        text1 = ''.join(raw_data[0:len(raw_data)])
        text = ''.join( text1.split('\n') )

        #日期
        raw_data = [data.text for data in soup.find_all("time")]
        print(raw_data)
        time = raw_data[0].strip('\n').strip(' ')

        date = time[:4]+'-'
        if str.isdigit(time[5:7]):
            date += (time[5:7] +'-')
            if str.isdigit(time[8:10]):
                date += time[8:10]
            else:
                date += ('0'+ time[8:9])
        else:
            date += ('0' + time[5:6] +'-')
            if str.isdigit(time[7:9]):
                date += time[7:9]
            else:
                date += ('0'+ time[7:8])
        print(date)

        #標題
        raw_data = [data.text for data in soup.find_all("h1",'Lh(1.39) Fz(25px)--sm Fz(36px) Ff($ff-primary) Lts($lspacing-md) Fw($fweight) Fsm($fsmoothing) Fsmw($fsmoothing) Fsmm($fsmoothing) Wow(bw)')]
        print(raw_data)
        head = raw_data[0]
    
    elif (url[:27] == 'https://www.chinatimes.com/'):#中時
        
        #內文
        raw_data = [data.text for data in soup.find("div","article-body").find_all('p')]
        print(raw_data)
        text1 = ''.join(raw_data[0:len(raw_data)])
        text = ''.join( text1.split('\n') )

        #日期
        raw_data = [data for data in soup.find("time").find('span','date')]
        print(raw_data)
        time = raw_data[0]
        date = time[:4]+'-'+time[5:7]+'-'+time[8:10]

        #標題
        raw_data = [data.text for data in soup.find_all("h1",'article-title')]
        print(raw_data)
        head = raw_data[0]

    elif (url[:21] == 'https://udn.com/news/'):#聯合

        raw_data = [data.text for data in soup.find("section",'article-content__editor').find_all('p')]
        print(raw_data)
        text1 = ''.join(raw_data[0:len(raw_data)])
        text = ''.join( text1.split('\n') )

        raw_data = [data.text for data in soup.find_all("time",'article-content__time')]
        print(raw_data)
        time = raw_data[0]
        date = time[:10]

        raw_data = [data.text for data in soup.find_all("h1",'article-content__title')]
        print(raw_data)
        head = raw_data[0]

    elif (url[:21] == 'https://www.setn.com/'):#三立

        raw_data = [data.text for data in soup.find("article").find_all('p')]
        print(raw_data)
        text1 = ''.join(raw_data[0:len(raw_data)])
        text = ''.join( text1.split('\n') )

        raw_data = [data.text for data in soup.find_all("time",'page-date')]
        print(raw_data)
        time = raw_data[0]
        date = time[:4]+'-'+time[5:7]+'-'+time[8:10]

        raw_data = [data.text for data in soup.find_all("h1",'news-title-3')]
        print(raw_data)
        head = raw_data[0]
    
    elif (url[:28] == 'https://money.udn.com/money/'):#聯合

        raw_data = [data.text for data in soup.find("div",id="article_body").find_all('p')]
        print(raw_data)
        text1 = ''.join(raw_data[0:len(raw_data)])
        text = ''.join( text1.split('\n') )

        raw_data = [data.text for data in soup.find_all("div",'shareBar__info--author')]
        print(raw_data)
        time = raw_data[0]
        date = time[:10]

        raw_data = [data.text for data in soup.find_all("h2",id = 'story_art_title')]
        print(raw_data)
        head = raw_data[0]

    elif (url[:23] == 'https://inews.hket.com/'):#香港經濟日報

        raw_data = [data.text for data in soup.find("div",'article-detail-content-container').find_all('p')]
        print(raw_data)
        text1 = ''.join(raw_data[0:len(raw_data)])
        text = ''.join( text1.split('\n') )

        raw_data = [data.text for data in soup.find_all("span",'article-details-info-container_date')]
        print(raw_data)
        time = raw_data[0]
        date = time[7:11]+'-'+time[12:14]+'-'+time[15:17]

        raw_data = [data.text for data in soup.find_all("h1")]
        print(raw_data)
        head = raw_data[0]

    elif (url[:29] == 'https://news.ltn.com.tw/news/'):#自由

        raw_data = [data.text for data in soup.find("div",'text boxTitle boxText').find_all('p')]
        print(raw_data)
        text1 = ''.join(raw_data[0:len(raw_data)])
        text = ''.join( text1.split('\n') )

        raw_data = [data.text for data in soup.find_all("span",'time')]
        print(raw_data)
        time = raw_data[0]
        date = time[5:15]

        raw_data = [data.text for data in soup.find_all("h1")]
        print(raw_data)
        head = raw_data[0]

    elif (url[:21] == 'https://www.storm.mg/'):#風傳媒

        raw_data = [data.text for data in soup.find("div",id="CMS_wrapper").find_all('p')]
        print(raw_data)
        text1 = ''.join(raw_data[0:len(raw_data)])
        text = ''.join( text1.split('\n') )

        raw_data = [data.text for data in soup.find_all("span",'info_inner_content')]
        print(raw_data)
        time = raw_data[0]
        date = time[:10]

        raw_data = [data.text for data in soup.find_all("h1",id="article_title")]
        print(raw_data)
        head = raw_data[0]

    elif (url[:32] == 'https://news.pts.org.tw/article/'):#公視

        raw_data = [data for data in soup.find("article",'post-article')]
        print(raw_data)
        for a in range(len(raw_data)):
            raw_data[a] = str(raw_data[a])
        text1 = ''.join(raw_data)
        text = ''.join( text.split('\n') )

        raw_data = [data.text for data in soup.find_all('time')]
        print(raw_data)
        time = raw_data[0]
        date = time[:10]

        raw_data = [data.text for data in soup.find_all("h1",'article-title')]
        print(raw_data)
        head = raw_data[0]

    elif (url[:28] == 'https://finance.sina.com.cn/'):#新浪

        raw_data = [data.text for data in soup.find("div",'article').find_all('p')]
        print(raw_data)
        text = ''.join(raw_data)
        
        raw_data = [data.text for data in soup.find_all('span','date')]
        print(raw_data)
        time = raw_data[0]
        date = time[:4]+'-'+time[5:7]+'-'+time[8:10]
        
        raw_data = [data.text for data in soup.find_all("h1",'main-title')]
        print(raw_data)
        head = raw_data[0]

    elif (url[:26] == 'https://tw.appledaily.com/'):#蘋果

        raw_data = [data.text for data in soup.find('div',id="article-body")]
        print(raw_data)
        text = ''.join(raw_data)
        
        raw_data = [data.text for data in soup.find_all('div','timestamp')]
        print(raw_data)
        time = raw_data[0]
        date = time[6:10]+'-'+time[11:13]+'-'+time[14:16]
        
        raw_data = [data.text for data in soup.find_all("h2",'text_medium')]
        print(raw_data)
        head = raw_data[0]
    
    elif (url[:34] == 'https://tw.finance.yahoo.com/news/' or url[:32] == 'https://tw.stock.yahoo.com/news/'):
        
        #內文
        raw_data = [data.text for data in soup.find("article").find_all('p')]
        print(raw_data)
        text1 = ''.join(raw_data[0:len(raw_data)])
        text = ''.join( text1.split('\n') )

        #日期
        raw_data = [data.text for data in soup.find_all("time")]
        print(raw_data)
        time = raw_data[0]
        date = time[:4]+'-'
        if str.isdigit(time[5:7]):
            date += (time[5:7] +'-')
            if str.isdigit(time[8:10]):
                date += time[8:10]
            else:
                date += ('0'+ time[8:9])
        else:
            date += ('0' + time[5:6] +'-')
            if str.isdigit(time[7:9]):
                date += time[7:9]
            else:
                date += ('0'+ time[7:8])
        print(date)

        #標題
        raw_data = [data.text for data in soup.find_all("h1",'Lh(1.39) Fz(25px)--sm Fz(36px) Ff($ff-primary) Lts($lspacing-md) Fw($fweight) Fsm($fsmoothing) Fsmw($fsmoothing) Fsmm($fsmoothing) Wow(bw)')]
        print(raw_data)
        head = raw_data[0]

    elif (url[:28] == 'https://www.rti.org.tw/news/'):#中央廣播電台

        raw_data = [data.text for data in soup.find('article').find_all('p')]
        print(raw_data)
        text = ''.join(raw_data)
        
        raw_data = [data.text for data in soup.find_all('li','date')]
        print(raw_data)
        time = raw_data[0].strip('\n').strip(' ')
        date = time[3:13]
        
        raw_data = [data.text for data in soup.find_all("h1")]
        print(raw_data)
        head = raw_data[0].strip('\n').strip(' ')

    elif (url[:39] == 'https://www.ustv.com.tw/UstvMedia/news/'):#非凡電視

        raw_data = [data.text for data in soup.find_all('p','main-content story')]
        print(raw_data)
        text1 = ''.join(raw_data)
        text = ''.join( text1.split('\n') )
        
        raw_data = [data.text for data in soup.find_all("h1",'module-title h3 title')]
        print(raw_data)
        raw_data2 = (raw_data[0].strip('\n').strip(' ')).split('\n')
        head = raw_data2[0].strip(' ')
        time = raw_data2[2].strip(' ')
        date = time[:10]

    elif (url[:19] == 'http://technews.tw/'):#科技新報

        raw_data = [data.text for data in soup.find('div','indent').find_all('p')]
        print(raw_data)
        text = ''.join(raw_data)
        
        raw_data = [data.text for data in soup.find_all('span','body')]
        print(raw_data)
        time = raw_data[1]
        date = time[:4]+'-'+time[7:9]+'-'+time[12:14]
        
        raw_data = [data.text for data in soup.find_all("h1",'entry-title')]
        print(raw_data)
        head = raw_data[0]

    elif (url[:37] == 'https://wealth.businessweekly.com.tw/'):#商周財富網

        raw_data = [data.text for data in soup.find('div','article_main').find_all('p')]
        print(raw_data)
        text = ''.join(raw_data)
        
        raw_data = [data.text for data in soup.find_all('div','article_date')]
        print(raw_data)
        raw_data2 = raw_data[0].split('\n')
        time = raw_data2[2]
        date = time[:4]+'-'+time[5:7]+'-'+time[8:10]
        
        raw_data = [data.text for data in soup.find_all("h1")]
        print(raw_data)
        head = raw_data[0]
    
    elif (url[:31] == 'https://house.ettoday.net/news/'):#ettoday房產雲

        raw_data = [data.text for data in soup.find('div','story lazyload').find_all('p')]
        print(raw_data)
        text1 = ''.join(raw_data)
        text = ''.join( text1.split('\n') )
        
        raw_data = [data.text for data in soup.find_all('time','date')]
        print(raw_data)
        time = raw_data[0].strip('\n').strip(' ')
        date = time[:10]
        
        raw_data = [data.text for data in soup.find_all("h1",'title')]
        print(raw_data)
        head = raw_data[0]

    elif (url[:25] == 'https://ctee.com.tw/news/'):#工商時報

        raw_data = [data.text for data in soup.find('div','entry-content clearfix single-post-content').find_all('p')]
        print(raw_data)
        text = ''.join(raw_data)
        
        raw_data = [data.text for data in soup.find_all('time','post-published updated')]
        print(raw_data)
        time = raw_data[0]
        date = time[:4]+'-'+time[5:7]+'-'+time[8:10]
        
        raw_data = [data.text for data in soup.find_all("h1",'single-post-title')]
        print(raw_data)
        head = raw_data[0].strip('\n')

    elif (url[:32] == 'https://www.businesstoday.com.tw'):#今周刊

        raw_data = [data.text for data in soup.find('div','cke_editable font__select-content').find_all('p')]
        print(raw_data)
        text1 = ''.join(raw_data)
        text = ''.join( text1.split('\xa0') )
        
        raw_data = [data.text for data in soup.find_all('p','context__info-item context__info-item--date')]
        print(raw_data)
        time = raw_data[0]
        date = time[:10]
        
        raw_data = [data.text for data in soup.find_all("h1",'article__maintitle')]
        print(raw_data)
        head = raw_data[0]

    elif (url[:31] == 'https://www.ithome.com.tw/news/'):#ithome

        raw_data = [data.text for data in soup.find('div','field field-name-body field-type-text-with-summary field-label-hidden').find_all('p')]
        print(raw_data)
        text = ''.join(raw_data)
        
        raw_data = [data.text for data in soup.find_all('span','created')]
        print(raw_data)
        time = raw_data[0]
        date = time[:10]
        
        raw_data = [data.text for data in soup.find_all("h1",'page-header')]
        print(raw_data)
        head = raw_data[0]

    elif (url[:23] == 'https://buzzorange.com/'):#報橘

        raw_data = [data.text for data in soup.find('div','entry-content').find_all('p')]
        print(raw_data)
        text1 = ''.join(raw_data)
        text = ''.join( text1.split('\n') )
        
        raw_data = [data.text for data in soup.find_all('time','entry-date published updated')]
        print(raw_data)
        time = raw_data[0]
        date = time[:4]+'-'+time[5:7]+'-'+time[8:10]
        
        raw_data = [data.text for data in soup.find_all("h1",'entry-title')]
        print(raw_data)
        head = raw_data[0]

    elif (url[:25] == 'https://www.ntdtv.com.tw/'):#新唐人亞太台

        raw_data = [data.text for data in soup.find('div',id="article_content").find_all('p')]
        print(raw_data)
        text = ''.join(raw_data)
        
        raw_data = [data.text for data in soup.find_all('div','article_info')]
        print(raw_data)
        time = raw_data[0]
        date = time[5:15]
        
        raw_data = [data.text for data in soup.find_all("h1",'article_title')]
        print(raw_data)
        head = raw_data[0]

    elif (url[:20] == 'https://technews.tw/'):#科技新報

        raw_data = [data.text for data in soup.find('div','indent').find_all('p')]
        print(raw_data)
        text = ''.join(raw_data)
        
        raw_data = [data.text for data in soup.find_all('span','body')]
        print(raw_data)
        time = raw_data[1]
        date = time[:4]+'-'+time[7:9]+'-'+time[12:14]
        
        raw_data = [data.text for data in soup.find_all('h1','entry-title')]
        print(raw_data)
        head = raw_data[0]

    elif (url[:25] == 'https://www.techbang.com/'):#T客邦

        raw_data = [data.text for data in soup.find('section','content').find_all('p')]
        print(raw_data)
        text1 = ''.join(raw_data)
        text = (''.join( text1.split('\n') )).strip(' ')
        
        raw_data = [data.text for data in soup.find('p','post-meta-info').find_all('span')]
        print(raw_data)
        time = raw_data[2]
        date = time[4:8]+'-0'+time[9:10]+'-'+time[11:13]
        
        raw_data = [data.text for data in soup.find_all('h1','post-title')]
        print(raw_data)
        head = raw_data[0].strip(' ').strip('\n')

    elif (url[:30] == 'https://ec.ltn.com.tw/article/'):#自由財經

        raw_data = [data.text for data in soup.find('div','text').find_all('p')]
        print(raw_data)
        text1 = ''.join(raw_data[:-2])
        text = (''.join( text1.split('\n') )).strip(' ')
        
        raw_data = [data.text for data in soup.find_all('span','time')]
        print(raw_data)
        time = raw_data[0]
        date = time[:4]+'-'+time[5:7]+'-'+time[8:10]
        
        raw_data = [data.text for data in soup.find_all('h1')]
        print(raw_data)
        head = raw_data[0]

    elif (url[:31] == 'http://www.digitimes.com.tw/tw/' or url[:27] == 'http://digitimes.com.tw/tw/'):#科技網

        raw_data = [data.text for data in soup.find('div',id="newsText").find_all('p','main_p')]
        print(raw_data)
        text = ''.join(raw_data[1:-2])
        
        raw_data = [data.text for data in soup.find_all('time')]
        print(raw_data)
        time = raw_data[0]
        date = time[:10]
        
        raw_data = [data.text for data in soup.find_all('p','txt-blue2 txt-bold m-b-10')]
        print(raw_data)
        head = raw_data[0]

    elif (url[:32] == 'http://www.digitimes.com.tw/iot/' or url[:33] == 'https://www.digitimes.com.tw/iot/'):#科技網

        raw_data = [data.text for data in soup.find('div',id="newsText").find_all('p','main_p')]
        print(raw_data)
        text = ''.join(raw_data[1:-2])
        
        raw_data = [data.text for data in soup.find_all('time')]
        print(raw_data)
        time = raw_data[0]
        date = time[:10]
        
        raw_data = [data.text for data in soup.find_all('p','article_header')]
        print(raw_data)
        head = raw_data[0]

    elif (url[:33] == 'http://www.digitimes.com.tw/tech/' or url[:34] == 'https://www.digitimes.com.tw/tech/'):#科技網

        raw_data = [data.text for data in soup.find('div',id="newsText").find_all('p','main_p')]
        print(raw_data)
        text = ''.join(raw_data[1:-2])
        
        raw_data = [data.text for data in soup.find_all('time')]
        print(raw_data)
        time = raw_data[0]
        date = time[:10]
        
        raw_data = [data.text for data in soup.find_all('p','txt-blue2 txt-bold m-b-10')]
        print(raw_data)
        head = raw_data[0]

    elif (url[:29] == 'https://www.digitimes.com.tw/'):#科技網

        raw_data = [data.text for data in soup.find('div',id="newsText").find_all('p','main_p')]
        print(raw_data)
        text = ''.join(raw_data[1:-2])
        
        raw_data = [data.text for data in soup.find_all('time')]
        print(raw_data)
        time = raw_data[0]
        date = time[:10]
        
        raw_data = [data.text for data in soup.find_all('p','txt-blue2 txt-bold m-b-10')]
        print(raw_data)
        head = raw_data[0]

    elif (url[:29] == 'https://chinese.engadget.com/'):#engadget中文網

        raw_data = [data.text for data in soup.find('div',id="post-center-col").find('div').find_all('div')]
        print(raw_data)
        text1 = ''.join(raw_data)
        text = ''.join(text1.split('\n'))
        
        raw_data = [data.text for data in soup.find_all('div','Mt(5px) C(engadgetFontLightGray)')]
        print(raw_data)
        time = raw_data[0]
        date = time[:4]+'-'+time[5:7]+'-'
        if str.isdigit(time[8:10]):
                date += time[8:10]
        else:
            date += ('0'+ time[8:9])
        
        raw_data = [data.text for data in soup.find_all('h1','Ff($ff-primary) M(0) C(engadgetBlack) Fw(400) Fz(36px) Mt(10px) Fz(48px)! Lh(55px) Fz(24px)!--sm Lh(n)--sm')]
        print(raw_data)
        head = raw_data[0]

    elif (url[:25] == 'http://info.ec.hc360.com/'):#慧聰電子網

        raw_data = [data.text for data in soup.find('div',id="artical").find_all('p')]
        print(raw_data)
        text1 = ''.join(raw_data)
        text = ''.join(text1.split('\xa0'))
        
        raw_data = [data.text for data in soup.find_all('span',id="endData")]
        print(raw_data)
        time = raw_data[0]
        date = time[:4]+'-'
        if str.isdigit(time[5:7]):
            date += (time[5:7] +'-')
            if str.isdigit(time[8:10]):
                date += time[8:10]
            else:
                date += ('0'+ time[8:9])
        else:
            date += ('0' + time[5:6] +'-')
            if str.isdigit(time[7:9]):
                date += time[7:9]
            else:
                date += ('0'+ time[7:8])
        print(date)
        
        raw_data = [data.text for data in soup.find_all('h1')]
        print(raw_data)
        head = raw_data[0]

    elif (url[:19] == 'https://chinese.engadget.com/'):#搜狐

        raw_data = [data.text for data in soup.find('div',id="contentText").find_all('p')]
        print(raw_data)
        text1 = ''.join(raw_data)
        text = ''.join(text1.split('\u3000'))
        
        raw_data = [data.text for data in soup.find_all('div','r')]
        print(raw_data)
        time = raw_data[0]
        date = time[:4]+'-'+time[5:7]+'-'+time[8:10]
        
        raw_data = [data.text for data in soup.find_all('h1')]
        print(raw_data)
        head = raw_data[0]

    elif (url[:27] == 'https://news.mydrivers.com/' or url[:26] == 'http://news.mydrivers.com/'):#快科技

        if url[:33] == 'https://news.mydrivers.com/1/178/':
            raw_data = [data.text for data in soup.find('div','pc_info').find_all('p')]
        else:
            raw_data = [data.text for data in soup.find('div','news_info').find_all('p')]
        print(raw_data)
        text1 = ''.join(raw_data)
        text2 = ''.join(text1.split('\xa0'))
        text = ''.join(text2.split('\n'))
        
        raw_data = [data.text for data in soup.find_all('div','news_bt1_left')]
        print(raw_data)
        time = raw_data[0]
        if url[:33] == 'https://news.mydrivers.com/1/178/':
            date = time[7:17]
        else:
            date = time[1:11]
        
        raw_data = [data.text for data in soup.find_all('div',id="thread_subject")]
        print(raw_data)
        head = raw_data[0]

    # elif (url[:26] == 'https://ee.ofweek.com/'):#維科網
        
    #     # raw_data = [data.text for data in soup.find('div',id="articleC").find_all('p')]
    #     raw_data = [data for data in soup.find_all('div','artical')]
    #     print(raw_data)
    #     text1 = ''.join(raw_data)
    #     text2 = ''.join(text1.split('\xa0'))
    #     text = ''.join(text2.split('\n'))
        
    #     raw_data = [data.text for data in soup.find_all('div','time fl')]
    #     print(raw_data)
    #     time = raw_data[0]
    #     date = time[1:11]
        
    #     raw_data = [data.text for data in soup.find_all('p','title')]
    #     print(raw_data)
    #     head = raw_data[0]

    elif (url[:27] == 'http://finance.sina.com.cn/'):#新浪財經

        raw_data = [data.text for data in soup.find('div',id="artibody").find_all('p')]
        print(raw_data)
        text1 = ''.join(raw_data[:-1])
        text = ''.join(text1.split('\u3000'))
        
        raw_data = [data.text for data in soup.find_all('span',id="pub_date")]
        print(raw_data)
        time = raw_data[0]
        date = time[:4]+'-'+time[5:7]+'-'+time[8:10]
        
        raw_data = [data.text for data in soup.find_all('h1',id="artibodyTitle")]
        print(raw_data)
        head = raw_data[0]

    elif (url[:24] == 'http://news.sina.com.cn/'):

        raw_data = [data.text for data in soup.find_all('div',id="artibody")]
        print(raw_data)
        text1 = ''.join(raw_data)
        text2 = ''.join(text1.split('\n'))
        text = ''.join(text2.split('\u3000'))
        
        raw_data = [data.text for data in soup.find_all('span',id="pub_date")]
        print(raw_data)
        time = raw_data[0]
        date = time[:4]+'-'+time[5:7]+'-'+time[8:10]
        
        raw_data = [data.text for data in soup.find_all('h1',id="artibodyTitle")]
        print(raw_data)
        head = raw_data[0]

    elif (url[:20] == 'http://tech.163.com/'):

        raw_data = [data.text for data in soup.find('div',id="endText").find_all('p')]
        print(raw_data)
        text1 = ''.join(raw_data)
        text = text1.strip(' ').strip('\n').strip(' ')
        
        raw_data = [data.text for data in soup.find_all('div','post_time_source')]
        print(raw_data)
        time = raw_data[0].strip('\n').strip(' ')
        date = time[:10]
        
        raw_data = [data.text for data in soup.find_all('h1')]
        print(raw_data)
        head = raw_data[0]

    elif (url[:24] == 'http://digi.it.sohu.com/'):

        raw_data = [data.text for data in soup.find('div',id="contentText").find_all('p')]
        print(raw_data)
        text1 = ''.join(raw_data)
        text = ''.join(text1.split('\u3000'))
        
        raw_data = [data.text for data in soup.find_all('div','r')]
        print(raw_data)
        time = raw_data[0]
        date = time[:4]+'-'+time[5:7]+'-'+time[8:10]
        
        raw_data = [data.text for data in soup.find_all('h1')]
        print(raw_data)
        head = raw_data[0]

    elif (url[:26] == 'http://www.techweb.com.cn/' or url[:29] == 'http://people.techweb.com.cn/'):

        raw_data = [data.text for data in soup.find('div',id="content").find_all('p')]
        print(raw_data)
        text = ''.join(raw_data)
        
        raw_data = [data.text for data in soup.find_all('span','time')]
        print(raw_data)
        time = raw_data[0]
        date = time[:4]+'-'+time[5:7]+'-'+time[8:10]
        
        raw_data = [data.text for data in soup.find_all('h1')]
        print(raw_data)
        head = raw_data[0]

    elif (url[:21] == 'http://vga.yesky.com/'):

        raw_data = [data.text for data in soup.find('div','article_infor').find_all('p')]
        print(raw_data)
        text1 = ''.join(raw_data)
        text = ''.join(text1.split('\u3000'))
        
        
        raw_data = [data.text for data in soup.find_all('span','date')]
        print(raw_data)
        time = raw_data[0]
        date = time[:10]
        
        raw_data = [data.text for data in soup.find_all('h1')]
        print(raw_data)
        head = raw_data[0].strip('\n')

    elif (url[:27] == 'https://www.coolloud.org.tw'):

        raw_data = [data.text for data in soup.find('div','field field-name-body field-type-text-with-summary field-label-hidden').find_all('p')]
        print(raw_data)
        text1 = ''.join(raw_data)
        text2 = ''.join(text1.split('\u3000'))
        text = ''.join(text2.split(' '))
        
        raw_data = [data.text for data in soup.find_all('span','date-display-single')]
        print(raw_data)
        time = raw_data[0]
        date = time[:4]+'-'+time[5:7]+'-'+time[8:10]
        
        raw_data = [data.text for data in soup.find_all('h1','page-header')]
        print(raw_data)
        head = raw_data[0].strip('\n')

    elif (url[:20] == 'https://it.sohu.com/'):

        raw_data = [data.text for data in soup.find('div',id="contentText").find_all('p')]
        print(raw_data)
        text1 = ''.join(raw_data)
        text2 = ''.join(text1.split('\u3000'))
        text = ''.join(text2.split('\xa0'))
        
        raw_data = [data.text for data in soup.find_all('div','r')]
        print(raw_data)
        time = raw_data[0]
        date = time[:4]+'-'+time[5:7]+'-'+time[8:10]
        
        raw_data = [data.text for data in soup.find_all('h1')]
        print(raw_data)
        head = raw_data[0].strip('\n')

    elif (url[:22] == 'http://www.cnbeta.com/' or url[:23] == 'https://www.cnbeta.com/' ):

        raw_data = [data.text for data in soup.find('div',"cnbeta-article-body").find_all('div',id="artibody")]
        print(raw_data)
        text1 = ''.join(raw_data)
        text2 = ''.join(text1.split('\n'))
        text = ''.join(text2.split('\xa0'))
        
        raw_data = [data.text for data in soup.find_all('div','meta')]
        print(raw_data)
        time = raw_data[0].strip('\n')
        date = time[:4]+'-'+time[5:7]+'-'+time[8:10]
        
        raw_data = [data.text for data in soup.find_all('h1')]
        print(raw_data)
        head = raw_data[1]

    elif (url[:24] == 'https://cn.engadget.com/'):#engadget中文網

        raw_data = [data.text for data in soup.find('div',id="post-center-col").find('div').find_all('div')]
        print(raw_data)
        text1 = ''.join(raw_data)
        text = ''.join(text1.split('\n'))
        
        raw_data = [data.text for data in soup.find_all('div','Mt(5px) C(engadgetFontLightGray)')]
        print(raw_data)
        time = raw_data[0]
        date = time[:4]+'-'+time[5:7]+'-'+time[8:10]
        
        raw_data = [data.text for data in soup.find_all('h1','Ff($ff-primary) M(0) C(engadgetBlack) Fw(400) Fz(36px) Mt(10px) Fz(48px)! Lh(55px) Fz(24px)!--sm Lh(n)--sm')]
        print(raw_data)
        head = raw_data[0]

    elif (url[:23] == 'http://www.51touch.com/'):

        raw_data = [data.text for data in soup.find('div','mt tcont').find_all('p')]
        print(raw_data)
        text1 = ''.join(raw_data)
        text = ''.join(text1.split('\xa0'))
        
        raw_data = [data.text for data in soup.find_all('div','clearfix color6 mt bdx1')]
        print(raw_data)
        raw_data2 = raw_data[0].strip('\n').strip('').split('\xa0')
        time = raw_data2[4]
        date = time[3:13]
        
        raw_data = [data.text for data in soup.find_all('h1','c')]
        print(raw_data)
        head = raw_data[0]

    elif (url[:27] == 'https://article.pchome.net/'):

        raw_data = [data.text for data in soup.find('div','mt tcont').find_all('p')]
        print(raw_data)
        text1 = ''.join(raw_data)
        text = ''.join(text1.split('\xa0'))
        
        raw_data = [data.text for data in soup.find_all('div','clearfix color6 mt bdx1')]
        print(raw_data)
        raw_data2 = raw_data[0].strip('\n').strip('').split('\xa0')
        time = raw_data2[4]
        date = time[3:13]
        
        raw_data = [data.text for data in soup.find_all('div',id="thread_subject")]
        print(raw_data)
        head = raw_data[0]

    elif (url[:30] == 'https://www.epochtimes.com/gb/'):

        raw_data = [data.text for data in soup.find('div',id="artbody").find_all('p')]
        print(raw_data)
        text = ''.join(raw_data)
        
        raw_data = [data for data in soup.find('div','mbottom10 large-12 medium-12 small-12 columns').find('time')]
        print(raw_data)
        time = raw_data[0].strip('更新: ').strip('')
        date = time[:10]
        
        raw_data = [data.text for data in soup.find_all('h1','blue18 title')]
        print(raw_data)
        head = raw_data[0]

    elif (url[:23] == 'http://stor.zol.com.cn/'):

        raw_data = [data.text for data in soup.find('div',id="cotent_idd").find_all('p')]
        print(raw_data)
        text1 = ''.join(raw_data[:-1])
        text = ''.join(text1.split('\u3000'))
        
        if url[:27] == 'http://stor.zol.com.cn/204/' or url[:27] == 'http://stor.zol.com.cn/188/' or url[:27] == 'http://stor.zol.com.cn/197/' or url[:27] == 'http://stor.zol.com.cn/194/':
            raw_data = [data.text for data in soup.find_all('div','tit_t1 clearfix')]
        else:
            raw_data = [data.text for data in soup.find_all('div','tit_t1 clearfix tc')]
        print(raw_data)
        
        if url[:27] == 'http://stor.zol.com.cn/194/':
            raw_data2 = raw_data[0].strip(' ').split(' ')
            time = raw_data2[1]
            date = time[-10:]
        else:
            raw_data2 = raw_data[0].strip(' ').split('  ')
            time = raw_data2[2].strip(' ')
            date = time[:4]+'-'+time[5:7]+'-'+time[8:10]
        
        raw_data = [data.text for data in soup.find_all('h1')]
        print(raw_data)
        head = raw_data[0]

    elif (url[:27] == 'https://3g.ali213.net/news/'):

        raw_data = [data.text for data in soup.find('div',id="Content").find_all('p')]
        print(raw_data)
        text1 = ''.join(raw_data)
        text = ''.join(text1.split('\u3000'))
        
        raw_data = [data.text for data in soup.find_all('div','header-info')]
        print(raw_data)
        time = raw_data[0].strip('\n')
        date = time[:10]
        
        raw_data = [data.text for data in soup.find_all('h3')]
        print(raw_data)
        head = raw_data[0]

    elif (url[:24] == 'https://newtalk.tw/news/'):

        raw_data = [data.text for data in soup.find('div','fontsize news-content').find_all('p')]
        print(raw_data)
        text = ''.join(raw_data)
        
        raw_data = [data.text for data in soup.find_all('div','content_date')]
        print(raw_data)
        time = raw_data[0].strip('\n').strip(' ')
        date = time[3:7]+'-'+time[8:10]+'-'+time[11:13]
        
        raw_data = [data.text for data in soup.find_all('h1','content_title')]
        print(raw_data)
        head = raw_data[0]

    elif (url[:22] == 'http://www.sinotf.com/'):

        raw_data = [data.text for data in soup.find('div',id="endText").find_all('p')]
        print(raw_data)
        text1 = ''.join(raw_data)
        text = ''.join(text1.split('\u3000'))
        
        raw_data = [data.text for data in soup.find_all('div','text')]
        print(raw_data)
        time = raw_data[1].strip('时间: ')
        date = time[:10]
        
        raw_data = [data.text for data in soup.find_all('h1',id="endTitle")]
        print(raw_data)
        head = raw_data[0]

    else:
        text = ' '
        head = ' '
        date = ' '
        texts.append(text)
        heads.append(head)
        dates.append(date)
        driver.close()
        continue

    # DELETE FROM `tsmc_udn_news` WHERE head = ' '
    driver.close()
    text = cc.convert(text)
    head = cc.convert(head)
    print(text)
    print(head)
    print(date)

    
    sql2="insert into `tsmc_udn_news` (`url`,`date`, `is_rise`,`head`,`text`, `text_and_head` ) VALUES"
    values = "('%s','%s',%f,'%s','%s','%s')"
    
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

    # texts[i] = text
    # heads[i] = head
    # dates[i] = date


    texts.append(text)
    heads.append(head)
    dates.append(date)
    # driver.close()

print(len(texts))
print(heads)
print(dates)