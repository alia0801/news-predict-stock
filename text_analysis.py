#https://codertw.com/%E7%A8%8B%E5%BC%8F%E8%AA%9E%E8%A8%80/37328/
#匯入資料集預處理、特徵工程和模型訓練所需的庫
from sklearn import model_selection, preprocessing, linear_model, naive_bayes, metrics, svm
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn import decomposition, ensemble
import pandas as pd
import numpy as np
import xgboost, numpy, string
# from keras.preprocessing import text, sequence
# from keras import layers, models, optimizers
# import textblob

#載入資料集
#建立一個dataframe，列名為text和label
# data = open('D:/Alia/Downloads/108-2/project/TextClassificationDatasets-20200411T150935Z-001/TextClassificationDatasets/amazon_review_full_csv/train.csv').read()
# labels, texts = [], []
# for i, line in enumerate(data.split('\n')):
#     content = line.split()
#     labels.append(content[0])
#     texts.append(content[1])
# trainDF = pandas.DataFrame()
# trainDF['text'] = texts
# trainDF['label'] = labels
trainDF = pd.read_csv('D:/Alia/Downloads/108-2/project/news_to_model3.csv')
print(trainDF)
print(trainDF['cat'])
print(trainDF['text'])

#將資料集分為訓練集和驗證集 x:text y:label
train_x, valid_x, train_y, valid_y = model_selection.train_test_split(trainDF['text'], trainDF['cat'])

# label編碼為目標變數
encoder = preprocessing.LabelEncoder()
train_y = encoder.fit_transform(train_y)
valid_y = encoder.fit_transform(valid_y)

# print(train_y)

#2.特徵工程

###2.1 計數向量作為特徵
#建立一個向量計數器物件
count_vect = CountVectorizer(analyzer='word', token_pattern=r'\w{1,}')
count_vect.fit(trainDF['text'])

#使用向量計數器物件轉換訓練集和驗證集
xtrain_count =  count_vect.transform(train_x)
xvalid_count =  count_vect.transform(valid_x)


###2.2 TF-IDF向量作為特徵
#詞語級tf-idf 矩陣代表了每個詞語在不同文件中的TF-IDF分數
tfidf_vect = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}', max_features=5000)
tfidf_vect.fit(trainDF['text'])
xtrain_tfidf =  tfidf_vect.transform(train_x)
xvalid_tfidf =  tfidf_vect.transform(valid_x)

# ngram 級tf-idf N-grams是多個詞語在一起的組合，這個矩陣代表了N-grams的TF-IDF分數
tfidf_vect_ngram = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}', ngram_range=(2,3), max_features=5000)
tfidf_vect_ngram.fit(trainDF['text'])
xtrain_tfidf_ngram =  tfidf_vect_ngram.transform(train_x)
xvalid_tfidf_ngram =  tfidf_vect_ngram.transform(valid_x)

#詞性級tf-idf 矩陣代表了語料中多個詞性的TF-IDF分數
tfidf_vect_ngram_chars = TfidfVectorizer(analyzer='char', token_pattern=r'\w{1,}', ngram_range=(2,3), max_features=5000)
tfidf_vect_ngram_chars.fit(trainDF['text'])
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
    if is_neural_net:    
        predictions = predictions.argmax(axis=-1)    
    print(predictions)
    print(valid_y)
    return metrics.accuracy_score(predictions, valid_y)


#3.5 Boosting Model

#特徵為計數向量的Xgboost
accuracy = train_model(xgboost.XGBClassifier(), xtrain_count.tocsc(), train_y, xvalid_count.tocsc())
print('Xgb, Count Vectors:' , accuracy)
#Xgb, Count Vectors: 0.8756

#特徵為詞語級別TF-IDF向量的Xgboost
accuracy = train_model(xgboost.XGBClassifier(), xtrain_tfidf.tocsc(), train_y, xvalid_tfidf.tocsc())
print('Xgb, WordLevel TF-IDF:' , accuracy)
#Xgb, WordLevel TF-IDF: 0.8744333333333333

#特徵為詞性級別TF-IDF向量的Xgboost
accuracy = train_model(xgboost.XGBClassifier(), xtrain_tfidf_ngram_chars.tocsc(), train_y, xvalid_tfidf_ngram_chars.tocsc())
print('Xgb, CharLevel Vectors:' , accuracy)
#Xgb, CharLevel Vectors: 0.8885333333333333
# news_to_model3 Xgb, CharLevel Vectors: 0.5572916666666666 

#特徵為多個詞語級別TF-IDF向量的SVM

accuracy = train_model(svm.SVC(), xtrain_tfidf_ngram, train_y, xvalid_tfidf_ngram)
print('SVM, N-Gram Vectors: ', accuracy)
# SVM, N-Gram Vectors:  0.8141666666666667
# news_to_model3 SVM, N-Gram Vectors:  0.5885416666666666 

