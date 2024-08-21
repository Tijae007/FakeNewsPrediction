# -*- coding: utf-8 -*-
"""Fake News Prediction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1a1MNSUL_Cmaw6q96ti65GFcM7D368kvD

1: Fake news
0: Real news

Importing Dependencies
"""

import numpy as np
import pandas as pd
import re
from nltk.corpus import stopwords #words that dont add value to sentences
from nltk.stem.porter import PorterStemmer #import important part of word
from sklearn.feature_extraction.text import TfidfVectorizer  #text to vectors
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression #model
from sklearn.metrics import accuracy_score

import nltk
nltk.download('stopwords')

#print the stopwords in english
print(stopwords.words('english'))

"""Data PreProcessing"""

# loading the dataset to a pandas dataframe
news_dataset = pd.read_csv('/content/train.csv')

news_dataset.shape

#print the first 5 rows of the datset
news_dataset.head()

#counting number of missing values in dataset
news_dataset.isnull().sum()

# replacing the null values with empty string
news_dataset = news_dataset.fillna('')

#merging the author name and news title
news_dataset['content']= news_dataset['author']+' '+news_dataset['title']

print(news_dataset['content'])

#seperating the data & label
X = news_dataset.drop(columns='label', axis=1)
Y = news_dataset['label']

print(X)
print(Y)

"""**Stemming: Reducing a word to its root word**"""

port_stem = PorterStemmer()

def stemming(content):
  stemmed_content = re.sub('[^a-zA-Z]', ' ', content)
  stemmed_content = stemmed_content.lower()
  stemmed_content = stemmed_content.split()
  stemmed_content = [port_stem.stem(word) for word in stemmed_content if not word in stopwords.words('english')]
  stemmed_content = ' '.join(stemmed_content)
  return stemmed_content

news_dataset['content'] = news_dataset['content'].apply(stemming)

print(news_dataset['content'])

#seperatng the data and label
X = news_dataset['content'].values
Y = news_dataset['label'].values

print(X)

#converting texts to numeric
vectorizer = TfidfVectorizer()
vectorizer.fit(X)

X = vectorizer.transform(X)

print(X)

"""**Splitting Dataset into training and testing dataset**"""

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, stratify=Y, random_state=2)

"""**Training the Model: Logistic Regression**"""

model = LogisticRegression()

model.fit(X_train, Y_train)

"""Evaluation: Accuracy Score"""

#Accuracy score on training data
X_train_prediction = model.predict(X_train)
training_data_accuracy = accuracy_score(X_train_prediction, Y_train)

print('Accuracy score of training data : ', training_data_accuracy)

#Accuracy score on testing data
X_test_prediction = model.predict(X_test)
testing_data_accuracy = accuracy_score(X_test_prediction, Y_test)

print('Accuracy score of testing data : ', testing_data_accuracy)

"""**Making Prediction System**"""

X_new = X_test[0]

prediction = model.predict(X_new)
print(prediction)

if (prediction[0]==0):
  print('The news is Real')
else:
  print('The news is Fake')

print(Y_test[0])
