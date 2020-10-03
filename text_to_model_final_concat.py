# %%
from sklearn import model_selection, preprocessing, linear_model, naive_bayes, metrics, svm
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn import decomposition, ensemble
import pandas as pd
import numpy as np
import xgboost, numpy, string
import pymysql
import datetime
from pandas_ml import ConfusionMatrix
from keras.preprocessing import text, sequence
from keras import layers, models, optimizers
# %%
#從資料庫擷取要丟入模型的部份
db = pymysql.connect("localhost", "root", "esfortest", "text_analysis")
cursor = db.cursor()
sql = 'SELECT * FROM `tsmc_udn_news` ORDER BY `tsmc_udn_news`.`date` ASC'
cursor.execute(sql)
result_select1 = cursor.fetchall()
db.commit()
# print(result_select1)
news = pd.DataFrame(list(result_select1))
print(news)
# %%
date=[]
news_text=[]
for i in range(len(news)):
    if news[1][i] in date:
        continue
    else:
        date.append(news[1][i])
        news_text.append('')
# print(date)
# print(news_text)
for i in range(len(news)):
    index = date.index(news[1][i])
    news_text[index]+=news[5][i]
# news = pd.concat([news, pd.DataFrame(heads,columns=['head'])],axis=1)
news_to_model = pd.concat([pd.DataFrame(date,columns=['date']), pd.DataFrame(news_text,columns=['text'])],axis=1)

# %%
sql = 'SELECT * FROM `2330.tw`'
cursor.execute(sql)
result_select1 = cursor.fetchall()
db.commit()
# print(result_select1)
prices = pd.DataFrame(list(result_select1))
# prices = pd.read_csv('D:/Alia/Downloads/108-2/project/2330.TW_0914.csv')#台股大盤
print(prices)
cat = []

#21日700大漲
#5日 300
#1日 150

# 2330 
# 5 10 20

d = 21
big_rise = 20
for j in range(len(prices[0])-d):
    
    if (prices[1][j+d] - prices[1][j]) > big_rise:#隔天漲
        cat.append(1)
    # elif prices[1][j]>=prices[1][j+d]:#隔天跌/持平
    else:
        cat.append(0)

for j in range(d):
    cat.append(0)#最後21天未知

print(cat)
prices = pd.concat([prices, pd.DataFrame(cat,columns=['cat'])],axis=1)
prices = prices.rename(columns={0:'Date'})
prices = prices.rename(columns={1:'Close'})
print(prices)

count=0
for i in cat:
    if i ==1:
        count+=1
print(count)

rise_percent = []
j=0
today = datetime.date.today()
for j in range(len(date)):
    # ddd = datetime.date(int(news[1][j][:4]),int(news[1][j][5:7]),int(news[1][j][8:10]))
    ddd = date[j]
    if date[j] in list(prices['Date']):
        index = list(prices['Date']).index(date[j])
        # rise_percent.append(prices['is_rise'][index])
        rise_percent.append(cat[index])
        # print(index)
    else:
        # ddd = ddd + datetime.timedelta(days=1)
        yes=0
        while((str(ddd) in list(prices['Date']))==False and ( datetime.datetime.strptime(str(ddd),"%Y-%m-%d")<datetime.datetime.strptime(str(today),"%Y-%m-%d") ) ):
            ddd = ddd + datetime.timedelta(days=1)
            # print(ddd)
            if (str(ddd) in list(prices['Date']))==True:
                yes=1
        if yes==1:
            index = list(prices['Date']).index(str(ddd))
            rise_percent.append(cat[index])
        elif yes==0:
            rise_percent.append(0)

        # rise_percent.append(prices['is_rise'][index])
        
print(rise_percent)

count=0
for i in rise_percent:
    if i ==1:
        count+=1
print(count)

news_to_model = pd.concat([news_to_model, pd.DataFrame(rise_percent,columns=['is_rise_month'])],axis=1)
# %%

#將資料集分為訓練集和驗證集 x:text y:label
# train_x, valid_x, train_y, valid_y = model_selection.train_test_split(new_to_model['text'], new_to_model['cat'])
train_x, valid_x, train_y, valid_y = model_selection.train_test_split(news_to_model['text'],news_to_model['is_rise_month'])


# label編碼為目標變數(-1-->0,1-->1)
encoder = preprocessing.LabelEncoder()
train_y = encoder.fit_transform(train_y)
valid_y = encoder.fit_transform(valid_y)

# print(train_y)

#2.特徵工程


###2.2 TF-IDF向量作為特徵

# #詞性級tf-idf 矩陣代表了語料中多個詞性的TF-IDF分數
tfidf_vect_ngram_chars = TfidfVectorizer(analyzer='char', token_pattern=r'\w{1,}', ngram_range=(2,3), max_features=5000)
tfidf_vect_ngram_chars.fit(news_to_model['text'])
xtrain_tfidf_ngram_chars =  tfidf_vect_ngram_chars.transform(train_x) 
xvalid_tfidf_ngram_chars =  tfidf_vect_ngram_chars.transform(valid_x)

# %%

# #三、建模  
classifier =  xgboost.XGBClassifier()
feature_vector_train = xtrain_tfidf_ngram_chars.tocsc()
label = train_y
feature_vector_valid = xvalid_tfidf_ngram_chars.tocsc()
classifier.fit(feature_vector_train, label)    
# predict the labels on validation dataset    
predictions = classifier.predict(feature_vector_valid)    
# print('guess:')
# print(predictions)
# print('ans:')
# print(valid_y)
cm = ConfusionMatrix(valid_y,predictions)
print(cm)
print(metrics.accuracy_score(predictions, valid_y))
# %%
