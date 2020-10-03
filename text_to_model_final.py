#https://codertw.com/%E7%A8%8B%E5%BC%8F%E8%AA%9E%E8%A8%80/37328/
#匯入資料集預處理、特徵工程和模型訓練所需的庫
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
# import datetime.date

#從資料庫擷取要丟入模型的部份
db = pymysql.connect("localhost", "root", "esfortest", "text_analysis")
cursor = db.cursor()
sql = 'SELECT * FROM `tsmc_udn_news`'
cursor.execute(sql)
result_select1 = cursor.fetchall()
db.commit()
# print(result_select1)
news = pd.DataFrame(list(result_select1))
print(news)


db = pymysql.connect("localhost", "root", "esfortest", "text_analysis")
cursor = db.cursor()
# sql = 'SELECT * FROM `twii_close`'
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
for j in range(len(news[1])):
    # ddd = datetime.date(int(news[1][j][:4]),int(news[1][j][5:7]),int(news[1][j][8:10]))
    ddd = news[1][j]
    if news[1][j] in list(prices['Date']):
        index = list(prices['Date']).index(news[1][j])
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

news = pd.concat([news, pd.DataFrame(rise_percent,columns=['is_rise_month'])],axis=1)


new_to_model = news.drop([0],axis=1)#url
new_to_model = new_to_model.drop([1],axis=1)#date
# new_to_model = new_to_model.drop(['time'],axis=1)
new_to_model = new_to_model.drop([3],axis=1)#head
new_to_model = new_to_model.drop([4],axis=1)#text
# new_to_model = new_to_model.drop(['cat'],axis=1)
new_to_model = new_to_model.rename(columns={2:'cat'})
new_to_model = new_to_model.rename(columns={5:'text'})
print(new_to_model)
# new_to_model.to_csv('D:/Alia/Downloads/108-2/project/news_to_model_udn_n.csv', index= False)



# trainDF = pd.read_csv('D:/Alia/Downloads/108-2/project/news_to_model3.csv')
# print(trainDF)
# print(new_to_model['cat'])
print(new_to_model['text'])
print(new_to_model['is_rise_month'])

#將資料集分為訓練集和驗證集 x:text y:label
# train_x, valid_x, train_y, valid_y = model_selection.train_test_split(new_to_model['text'], new_to_model['cat'])
train_x, valid_x, train_y, valid_y = model_selection.train_test_split(new_to_model['text'], new_to_model['is_rise_month'])


# label編碼為目標變數(-1-->0,1-->1)
encoder = preprocessing.LabelEncoder()
train_y = encoder.fit_transform(train_y)
valid_y = encoder.fit_transform(valid_y)

# print(train_y)

#2.特徵工程


###2.2 TF-IDF向量作為特徵

# #詞性級tf-idf 矩陣代表了語料中多個詞性的TF-IDF分數
tfidf_vect_ngram_chars = TfidfVectorizer(analyzer='char', token_pattern=r'\w{1,}', ngram_range=(2,3), max_features=5000)
tfidf_vect_ngram_chars.fit(new_to_model['text'])
xtrain_tfidf_ngram_chars =  tfidf_vect_ngram_chars.transform(train_x) 
xvalid_tfidf_ngram_chars =  tfidf_vect_ngram_chars.transform(valid_x)



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
# Predicted  False  True  __all__
# Actual
# False         13    39       52
# True          10   198      208
# __all__       23   237      260       
# 0.8115384615384615

# Predicted  False  True  __all__
# Actual
# False         63    61      124
# True          16   170      186
# __all__       79   231      310
# 0.7516129032258064

# 21天
# Predicted  False  True  __all__
# Actual
# False         53    55      108
# True          14   194      208
# __all__       67   249      316
# 0.7816455696202531


# 5天
# Predicted  False  True  __all__
# Actual
# False        138    36      174
# True          74    68      142
# __all__      212   104      316
# 0.6518987341772152

#21日大漲幅
# Predicted  False  True  __all__
# Actual
# False        225     4      229
# True          72    18       90
# __all__      297    22      319
# 0.7617554858934169
# precision = 18/22 = 0.8181818182
# recall = 18/90 = 0.2
# f1 = 2*(p*r)/(p+r) = 0.3214

#5日大漲幅
# Predicted  False  True  __all__
# Actual
# False        240     6      246
# True          59    14       73
# __all__      299    20      319
# 0.7962382445141066
# precision = 14/20 = 0.7 
# recall = 14/73 = 0.19178082
# f1 = 0.30096126

#1日大漲幅
# Predicted  False  True  __all__
# Actual
# False        268     4      272
# True          43     4       47
# __all__      311     8      319
# 0.8526645768025078
# precision = 4/8 = 0.5
# recall = 4/47 = 0.08510638
# f1 = 0.1454545






#增加資料量
#1日
# Predicted  False  True  __all__
# Actual
# False        839   318     1157
# True         535   409      944
# __all__     1374   727     2101
# 0.5940028557829605
# p = 0.56258597
# r = 0.43326271
# f1 = 0.48952723

#5日
# Predicted  False  True  __all__
# Actual
# False        543   496     1039
# True         296   766     1062
# __all__      839  1262     2101
# 0.6230366492146597
# p = 0.60697306
# r = 0.7212806
# f1 = 0.65920826

#21日
# Predicted  False  True  __all__
# Actual
# False        521   441      962
# True         229   910     1139
# __all__      750  1351     2101
# 0.681104236078058
# p = 0.67357513
# r = 0.79894644
# f1 = 0.7309236932753891

#1日大漲幅
# Predicted  False  True  __all__
# Actual
# False       1916     1     1917
# True         184     0      184
# __all__     2100     1     2101
# 0.9119466920514041
# p = 0
# r = 0
# f1 = 0

#5日大漲幅
# Predicted  False  True  __all__
# Actual
# False       1835     2     1837
# True         260     4      264
# __all__     2095     6     2101
# 0.8752974773917183
# p = 0.66666667
# r = 0.01515152
# f1 = 0.029629638903703643

#21日大漲幅
# Predicted  False  True  __all__
# Actual
# False       1811     3     1814
# True         270    17      287
# __all__     2081    20     2101
# 0.8700618752974774
# p = 0.85
# r = 0.05923345
# f1 = 0.11074918658128999


# Predicted  False  True  __all__        
# Actual
# False       1565    41     1606        
# True         484    82      566        
# __all__     2049   123     2172        
# 0.7582872928176796


# Predicted  False  True  __all__
# Actual
# False       2035     4     2039
# True         284    15      299
# __all__     2319    19     2338
# 0.8768177929854577

# Predicted  False  True  __all__      
# Actual
# False       1661    25     1686      
# True         568    84      652      
# __all__     2229   109     2338      
# 0.7463644140290847