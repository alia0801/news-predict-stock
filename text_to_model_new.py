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

# news[1]





db = pymysql.connect("localhost", "root", "esfortest", "text_analysis")
cursor = db.cursor()
sql = 'SELECT * FROM `twii_close`'
cursor.execute(sql)
result_select1 = cursor.fetchall()
db.commit()
# print(result_select1)
prices = pd.DataFrame(list(result_select1))
# prices = pd.read_csv('D:/Alia/Downloads/108-2/project/^TWII.csv')#台股大盤
print(prices)
cat = []
for j in range(len(prices[0])-21):
    
    if prices[1][j]<prices[1][j+21]:#隔天漲
        cat.append(1)
    elif prices[1][j]>=prices[1][j+21]:#隔天跌/持平
        cat.append(-1)

for j in range(21):
    cat.append(-1)#最後21天未知

print(cat)
prices = pd.concat([prices, pd.DataFrame(cat,columns=['cat'])],axis=1)
prices = prices.rename(columns={0:'Date'})
prices = prices.rename(columns={1:'Close'})
print(prices)


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
            rise_percent.append(-1)

        # rise_percent.append(prices['is_rise'][index])
        
print(rise_percent)

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
print(new_to_model['cat'])
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

###2.1 計數向量作為特徵
#建立一個向量計數器物件
count_vect = CountVectorizer(analyzer='word', token_pattern=r'\w{1,}')
count_vect.fit(new_to_model['text'])

#使用向量計數器物件轉換訓練集和驗證集
xtrain_count =  count_vect.transform(train_x)
xvalid_count =  count_vect.transform(valid_x)


###2.2 TF-IDF向量作為特徵
# #詞語級tf-idf 矩陣代表了每個詞語在不同文件中的TF-IDF分數
tfidf_vect = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}', max_features=5000)
tfidf_vect.fit(new_to_model['text'])
xtrain_tfidf =  tfidf_vect.transform(train_x)
xvalid_tfidf =  tfidf_vect.transform(valid_x)

# ngram 級tf-idf N-grams是多個詞語在一起的組合，這個矩陣代表了N-grams的TF-IDF分數
tfidf_vect_ngram = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}', ngram_range=(2,3), max_features=5000)
tfidf_vect_ngram.fit(new_to_model['text'])
xtrain_tfidf_ngram =  tfidf_vect_ngram.transform(train_x)
xvalid_tfidf_ngram =  tfidf_vect_ngram.transform(valid_x)

# #詞性級tf-idf 矩陣代表了語料中多個詞性的TF-IDF分數
tfidf_vect_ngram_chars = TfidfVectorizer(analyzer='char', token_pattern=r'\w{1,}', ngram_range=(2,3), max_features=5000)
tfidf_vect_ngram_chars.fit(new_to_model['text'])
xtrain_tfidf_ngram_chars =  tfidf_vect_ngram_chars.transform(train_x) 
xvalid_tfidf_ngram_chars =  tfidf_vect_ngram_chars.transform(valid_x)



#2.3 詞嵌入


#2.4 基於文字/NLP的特徵






#三、建模
def train_model(classifier, feature_vector_train, label, feature_vector_valid, is_neural_net=False):
    # fit the training dataset on the classifier    
    classifier.fit(feature_vector_train, label)    

    # predict the labels on validation dataset    
    predictions = classifier.predict(feature_vector_valid)    
    if is_neural_net:    #是類神經網路模型
        predictions = predictions.argmax(axis=-1)    
    # print('guess:')
    # print(predictions)
    # print('ans:')
    # print(valid_y)
    cm = ConfusionMatrix(valid_y,predictions)
    print(cm)
    return metrics.accuracy_score(predictions, valid_y)




# 3.1 樸素貝葉斯
#特徵為計數向量的樸素貝葉斯
accuracy = train_model(naive_bayes.MultinomialNB(), xtrain_count, train_y, xvalid_count)
print('NB, Count Vectors: ', accuracy)
# NB, Count Vectors:  0.6307692307692307
# Predicted  False  True  __all__
# Actual
# False         54    11       65
# True          91   104      195
# __all__      145   115      260
# NB, Count Vectors:  0.6076923076923076

#特徵為詞語級別TF-IDF向量的樸素貝葉斯
accuracy = train_model(naive_bayes.MultinomialNB(), xtrain_tfidf, train_y, xvalid_tfidf)
print( 'NB, WordLevel TF-IDF: ', accuracy)
# NB, WordLevel TF-IDF:  0.8
# Predicted  False  True  __all__
# Actual
# False          6    59       65
# True           2   193      195
# __all__        8   252      260
# NB, WordLevel TF-IDF:  0.7653846153846153

#特徵為多個詞語級別TF-IDF向量的樸素貝葉斯
accuracy = train_model(naive_bayes.MultinomialNB(), xtrain_tfidf_ngram, train_y, xvalid_tfidf_ngram)
print( 'NB, N-Gram Vectors: ', accuracy)
# NB, N-Gram Vectors:  0.8076923076923077
# Predicted  False  True  __all__
# Actual
# False          6    59       65
# True           8   187      195
# __all__       14   246      260
# NB, N-Gram Vectors:  0.7423076923076923

#特徵為詞性級別TF-IDF向量的樸素貝葉斯
accuracy = train_model(naive_bayes.MultinomialNB(), xtrain_tfidf_ngram_chars, train_y, xvalid_tfidf_ngram_chars)
print( 'NB, CharLevel Vectors: ', accuracy)
# NB, CharLevel Vectors:  0.7769230769230769
# Predicted  False  True  __all__
# Actual
# False         15    50       65
# True          14   181      195
# __all__       29   231      260
# NB, CharLevel Vectors:  0.7538461538461538

# 3.2線性分類器
# Linear Classifier on Count Vectors
accuracy = train_model(linear_model.LogisticRegression(), xtrain_count, train_y, xvalid_count)
print( 'LR, Count Vectors: ', accuracy)
# LR, Count Vectors:  0.7846153846153846
# Predicted  False  True  __all__
# Actual
# False          6    59       65
# True           2   193      195
# __all__        8   252      260
# LR, Count Vectors:  0.7653846153846153

#特徵為詞語級別TF-IDF向量的線性分類器
accuracy = train_model(linear_model.LogisticRegression(), xtrain_tfidf, train_y, xvalid_tfidf)
print( 'LR, WordLevel TF-IDF: ', accuracy)
# LR, WordLevel TF-IDF:  0.7769230769230769
# Predicted  0    1  __all__
# Actual
# 0          0   65       65
# 1          0  195      195
# __all__    0  260      260
# LR, WordLevel TF-IDF:  0.75

#特徵為多個詞語級別TF-IDF向量的線性分類器
accuracy = train_model(linear_model.LogisticRegression(), xtrain_tfidf_ngram, train_y, xvalid_tfidf_ngram)
print( 'LR, N-Gram Vectors: ', accuracy)
# LR, N-Gram Vectors:  0.7769230769230769

#特徵為詞性級別TF-IDF向量的線性分類器
accuracy = train_model(linear_model.LogisticRegression(), xtrain_tfidf_ngram_chars, train_y, xvalid_tfidf_ngram_chars)
print( 'LR, CharLevel Vectors: ', accuracy)
# LR, CharLevel Vectors:  0.7961538461538461
# Predicted  0    1  __all__
# Actual
# 0          0   65       65
# 1          0  195      195
# __all__    0  260      260
# LR, N-Gram Vectors:  0.75


# 3.3 SVM

#特徵為多個詞語級別TF-IDF向量的SVM
accuracy = train_model(svm.SVC(), xtrain_tfidf_ngram, train_y, xvalid_tfidf_ngram)
print('SVM, N-Gram Vectors: ', accuracy)
# SVM, N-Gram Vectors:  0.7769230769230769 預測月(股市21日後)
# Predicted  0    1  __all__
# Actual
# 0          0   65       65
# 1          0  195      195
# __all__    0  260      260
# SVM, N-Gram Vectors:  0.75

# 3.4 Bagging Model

#特徵為計數向量的RF
accuracy = train_model(ensemble.RandomForestClassifier(), xtrain_count, train_y, xvalid_count)
print( 'RF, Count Vectors: ', accuracy)
# RF, Count Vectors:  0.7769230769230769
# Predicted  False  True  __all__
# Actual
# False          4    61       65
# True           2   193      195
# __all__        6   254      260
# RF, Count Vectors:  0.7576923076923077

#特徵為詞語級別TF-IDF向量的RF
accuracy = train_model(ensemble.RandomForestClassifier(), xtrain_tfidf, train_y, xvalid_tfidf)
print( 'RF, WordLevel TF-IDF: ', accuracy)
# RF, WordLevel TF-IDF:  0.8115384615384615
# Predicted  False  True  __all__
# Actual
# False         15    50       65
# True          12   183      195
# __all__       27   233      260
# RF, WordLevel TF-IDF:  0.7615384615384615


#3.5 Boosting Model

# #特徵為計數向量的Xgboost
accuracy = train_model(xgboost.XGBClassifier(), xtrain_count.tocsc(), train_y, xvalid_count.tocsc())
print('Xgb, Count Vectors:' , accuracy)
# Xgb, Count Vectors: 0.8038461538461539 預測月(股市21日後)
# Predicted  False  True  __all__
# Actual
# False          8    57       65
# True           4   191      195
# __all__       12   248      260
# Xgb, Count Vectors: 0.7653846153846153

# #特徵為詞語級別TF-IDF向量的Xgboost
accuracy = train_model(xgboost.XGBClassifier(), xtrain_tfidf.tocsc(), train_y, xvalid_tfidf.tocsc())
print('Xgb, WordLevel TF-IDF:' , accuracy)
# Xgb, WordLevel TF-IDF: 0.8038461538461539 預測月(股市21日後)
# Predicted  False  True  __all__
# Actual
# False          8    57       65
# True           4   191      195
# __all__       12   248      260
# Xgb, WordLevel TF-IDF: 0.7653846153846153

# #特徵為詞性級別TF-IDF向量的Xgboost
accuracy = train_model(xgboost.XGBClassifier(), xtrain_tfidf_ngram_chars.tocsc(), train_y, xvalid_tfidf_ngram_chars.tocsc())
print('Xgb, CharLevel Vectors:' , accuracy)
# Xgb, CharLevel Vectors: 0.8115384615384615 預測月(股市21日後)
# Predicted  False  True  __all__
# Actual
# False         14    51       65
# True           9   186      195
# __all__       23   237      260
# Xgb, CharLevel Vectors: 0.7692307692307693***

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

# 3.6 NN
# 建立CNN模型
def create_model_architecture(input_size):

    # create input layer 
    input_layer = layers.Input((input_size, ), sparse=True)

    # create hidden layer
    hidden_layer = layers.Dense(1000, activation='relu')(input_layer)
    hidden_layer = layers.Dense(500, activation='relu')(input_layer)
    hidden_layer = layers.Dense(100, activation='relu')(input_layer)

    # create output layer
    output_layer = layers.Dense(1, activation='sigmoid')(hidden_layer)
    classifier = models.Model(inputs = input_layer, outputs = output_layer)
    classifier.compile(optimizer=optimizers.Adam(), loss='binary_crossentropy')
    return classifier 
     
classifier = create_model_architecture(xtrain_tfidf_ngram.shape[1])
accuracy = train_model(classifier, xtrain_tfidf_ngram, train_y, xvalid_tfidf_ngram, is_neural_net=True)
print('NN, Ngram Level TF IDF Vectors ',  accuracy)
# NN, Ngram Level TF IDF Vectors  0.2230769230769231(都猜0)
# Predicted    0  1  __all__
# Actual
# 0           65  0       65
# 1          195  0      195
# __all__    260  0      260
# NN, Ngram Level TF IDF Vectors  0.25

