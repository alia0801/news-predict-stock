
from selenium import webdriver
import time
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import pymysql
import datetime
from selenium.webdriver.chrome.options import Options
import requests
import datetime
from dateutil.parser import parse 
from datetime import timedelta, datetime
from opencc import OpenCC
cc = OpenCC('s2tw')

today = datetime.date.today()

target = '台積電'
start_date_str = '1/1/2010'
end_date_str = '12/31/2010'

driver = webdriver.Chrome("D:/Alia/Downloads/108-1/project/chromedriver_win32/chromedriver.exe")

news_url=[]

for i in range(27):
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
total_url.to_csv('D:/Alia/Downloads/108-2/project/google_news_url_2010.csv', index= False)
total_url = pd.read_csv('D:/Alia/Downloads/108-2/project/google_news_url_2010.csv')
news_url = list(total_url['url'])

# [1, 4, 6, 9, 10, 11, 13, 15, 18, 19, 23, 24, 30, 31, 32, 33, 34, 36, 37, 38, 39, 40, 42, 44, 45, 47, 48, 49

texts=[]
heads=[]
dates=[]
for i in range(len(news_url)):
# for i in range(10,11):
# for i in space:    

    print(i)
    driver = webdriver.Chrome("D:/Alia/Downloads/108-1/project/chromedriver_win32/chromedriver.exe")
    url = news_url[i]
    print(url)

    if (url[:20] == 'https://tech.qq.com/' or url[:27] == 'https://article.pchome.net/' or url == 'http://www.techweb.com.cn/tech/2010-07-23/647128.shtml'):
        driver.close()
        text = ' '
        head = ' '
        date = ' '
        texts[i] = text
        heads[i] = head
        dates[i] = date
        # texts.append(text)
        # heads.append(head)
        # dates.append(date)
        continue

    driver.get(url)
    # url = driver.current_url
    # time.sleep(5)
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

    # elif (url[:24] == 'http://tech.sina.com.cn/'):#新浪財經

    #     raw_data = [data.text for data in soup.find_all('div','blkContainerSblkCon')]
    #     print(raw_data)
    #     text1 = ''.join(raw_data[:-1])
    #     text = ''.join(text1.split('\u3000'))
        
    #     raw_data = [data.text for data in soup.find_all('div','artInfo')]
    #     print(raw_data)
    #     time = raw_data[0]
    #     date = time[:4]+'-'+time[5:7]+'-'+time[8:10]
        
    #     raw_data = [data.text for data in soup.find_all('h1')]
    #     print(raw_data)
    #     head = raw_data[1]

    # elif (url[:20] == 'http://www.52rd.com/'):

    #     raw_data = [data.text for data in soup.find('div',id="post-center-col").find('div').find_all('div')]
    #     print(raw_data)
    #     text1 = ''.join(raw_data)
    #     text = ''.join(text1.split('\n'))
        
    #     raw_data = [data.text for data in soup.find_all('div','Mt(5px) C(engadgetFontLightGray)')]
    #     print(raw_data)
    #     time = raw_data[0]
    #     date = time[:4]+'-'+time[5:7]+'-'+time[8:10]
        
    #     raw_data = [data.text for data in soup.find_all('h1','Ff($ff-primary) M(0) C(engadgetBlack) Fw(400) Fz(36px) Mt(10px) Fz(48px)! Lh(55px) Fz(24px)!--sm Lh(n)--sm')]
    #     print(raw_data)
    #     head = raw_data[0]

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
            date = raw_data2[1][-10:]
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

# https://ee.ofweek.com/ soup找不到資訊
# http://tech.sina.com.cn/ soup找不到資訊
# https://tech.qq.com/ 會壞
# http://www.52rd.com/ 找不到頁面
# https://article.pchome.net/ 會壞
# http://www.taipeitimes.com/ 英文
# https://www.cheers.com.tw/ 僅1篇
# https://www.ftchinese.com/ 僅1篇
# https://m.hc360.com/  跳回首頁
# https://news.cts.com.tw/cts/  多無關
# https://news.eastday.com 1篇 無關
# https://e-info.org.tw/node/ 1篇 無關
# https://dc.pconline.com.cn/ 無關
# http://blovesky.blog.techweb.com.cn/ 網誌不用
# http://www.ithome.com.tw/node/ 無關
    
    else:
        text = ' '
        head = ' '
        date = ' '
        # driver.close()
        # continue

    driver.close()

    text = cc.convert(text)
    head = cc.convert(head)

    print(text)
    print(head)
    print(date)

    texts[i] = text
    heads[i] = head
    dates[i] = date
    # texts.append(text)
    # heads.append(head)
    # dates.append(date)

    #134

# print(texts)
print(heads)
print(dates)

space = []

for i in range(len(heads)):
    if heads[i] == ' ':
        space.append(i)
print(space)

for i in space:
    print(i,news_url[i])

for i in range(266):
    print(i,heads[i])

# [1, 4, 6, 9, 10, 11, 13, 15, 18, 19, 23, 24, 30, 31, 32, 33, 34, 36, 37, 38, 39, 40, 42, 44, 45, 47, 48, 49
# [9, 10, 11, 18, 23, 24, 25, 31, 32, 33, 34, 37, 38, 39, 40, 45, 49, 50, 57, 58, 61, 64, 67, 75, 76, 77, 81, 83, 85, 87, 88, 93, 94, 102, 103, 106, 107, 115, 124, 125, 127, 128, 129, 132, 134, 135, 136, 137, 141, 142, 149, 150, 154, 155, 156, 161, 162, 165, 168, 174, 177, 181, 182, 184, 185, 186, 191, 192, 193, 194, 195, 197, 198, 200, 204, 205, 208, 210, 
# 211, 212, 218, 219, 220, 221, 224, 230, 231, 233, 234, 235, 236, 240, 244, 246, 248, 249, 253, 255, 256, 259, 265]

# [9, 10, 11, 23, 24, 25, 31, 32, 33, 34, 37, 38, 39, 40, 45, 49, 50, 57, 58, 61, 67, 75, 76, 77, 81, 83, 85, 87, 107, 115, 124, 125, 127, 128, 129, 132, 134, 135, 136, 137, 141, 142, 149, 150, 154, 155, 156, 161, 162, 165, 168, 174, 177, 181, 182, 184, 185, 186, 191, 192, 193, 194, 195, 197, 198, 200, 204, 205, 208, 210, 211, 212, 218, 219, 220, 221, 224, 
# 230, 231, 233, 234, 235, 236, 240, 244, 246, 248, 249, 253, 255, 256, 259, 265]

news = pd.concat([total_url, pd.DataFrame(dates,columns=['date'])],axis=1)
news = pd.concat([news, pd.DataFrame(heads,columns=['head'])],axis=1)
news = pd.concat([news, pd.DataFrame(texts,columns=['text'])],axis=1)

print(news)
news.to_csv('D:/Alia/Downloads/108-2/project/google_news_2010.csv', index= False)

