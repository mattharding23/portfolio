#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 14:52:43 2021

@author: mattharding
"""

import requests
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction import text 
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import os
import csv
import warnings
import nltk
from numpy import savetxt
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import matplotlib.pyplot as plt
from nltk.corpus import stopwords

from sklearn import preprocessing
import sklearn
import re  
import matplotlib.pyplot as plt
from nltk.tokenize import sent_tokenize, word_tokenize
import os
from sklearn.model_selection import train_test_split
import random as rd
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn.naive_bayes import BernoulliNB
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree

import graphviz 
from sklearn.metrics import confusion_matrix
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.svm import LinearSVC
from sklearn.decomposition import PCA

import graphviz 
from sklearn.metrics import confusion_matrix

from sklearn.tree import export_graphviz
from IPython.display import Image  
import pydotplus
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.svm import LinearSVC


warnings.filterwarnings('ignore')

# %%
# Use data cleaning code but add tfidf vectorizer

# DATA CLEANING

#-----------------

# Identify path to folder where tweets will be saved
path = '/Users/mattharding/Documents/Georgetown/Fall_2021/ANLY_501/Mod_2_assignment/'
path_csvs = path + 'tweet_csvs/'

# Retrieve names of csv files
csv_names=os.listdir(path_csvs)

path_txt = path + 'tweets/'

# save tweets as individual txt files & labels in a label list
labels = []
file_names = []
for file in csv_names:
    count = 1
    
    # Label is name of csv file not including '.csv'
    label = file.split('.')[0]
    
    # Read in csv file
    csv_read = csv.DictReader(open(f'{path_csvs}{file}'))
    
    for row in csv_read:
        
        # Extract text
        tweet = row['text']
        
        # Create filename variable
        fn = f'{path_txt}{label}{count}.txt'
        
        # Write tweet to txt file
        f = open(fn,'w')
        f.write(tweet)
        f.close()
        
        # Save label for tweet
        labels.append(label)
        
        # Save filename for count vectorizer
        file_names.append(fn)
        count += 1



# Create count vectorizer    
cv = CountVectorizer(input='filename',stop_words="english")
tv = TfidfVectorizer(input="filename", stop_words = "english")

# Get Document term matrix
dtm_cv = cv.fit_transform(file_names)
dtm_tv = tv.fit_transform(file_names)
# Extract column names
col_names_cv = cv.get_feature_names()
col_names_tv = tv.get_feature_names()

# Turn into pandas df
cv_df = pd.DataFrame(dtm_cv.toarray(),columns=col_names_cv)
tv_df = pd.DataFrame(dtm_tv.toarray(),columns=col_names_tv)


# Insert labels column
cv_df.insert(loc=0, column='Label', value=labels)
tv_df.insert(loc=0, column='Label', value=labels)

#remove number values
keep_words = [col for col in cv_df.columns if col.isalpha()]

cv_df = cv_df[keep_words]
tv_df = tv_df[keep_words]


# # Remove other words not caught by stopwords
more_stop_words = ['https','rt','ivepetthatdog']
keep_words = [col for col in cv_df.columns if not col in more_stop_words]
cv_df = cv_df[keep_words]
tv_df = tv_df[keep_words]

# chesapeake bay label is all encompassing and also has many more tweets than other labels. Will remove for now and ma
#ybe use as testing for laters. 
cv_dt_df = cv_df[cv_df['Label'] != 'chesapeakebay']
tv_dt_df = tv_df[tv_df['Label'] != 'chesapeakebay']

# Save dfs to csvs
cv_dt_df.to_csv('Labeled_cv_data.csv')
tv_dt_df.to_csv('Labeled_tv_data.csv')

#%% Naive Bayes on Count Vectorizer Data

# Split into testing & training dataframes
train_set, test_set = train_test_split(cv_dt_df, test_size=0.3,random_state=10)

# Remove and save labels from test data
test_labs = test_set['Label']
test_set = test_set.drop(['Label'], axis=1)

# Separate labels from training set
train_labs = train_set['Label']
train_set = train_set.drop(['Label'], axis=1)

# Create NB  model
model = MultinomialNB()
nb = model.fit(train_set, train_labs)
pred = model.predict(test_set)
#print(np.round(model.predict_proba(test_set),2))

cm = confusion_matrix(test_labs, pred)
print("\nThe confusion matrix is:")
print(cm)
d = {'Actual':test_labs,'Predicted':pred}
df = pd. DataFrame(d)

df.to_csv('cv_cm.csv')


#%% Naive Bayes on tfidf Vectorizer Data

# Split into testing & training dataframes
train_set, test_set = train_test_split(tv_dt_df, test_size=0.3,random_state=10)

# Remove and save labels from test data
test_labs = test_set['Label']
test_set = test_set.drop(['Label'], axis=1)

# Separate labels from training set
train_labs = train_set['Label']
train_set = train_set.drop(['Label'], axis=1)

# Create NB  model
model = MultinomialNB()
nb = model.fit(train_set, train_labs)
pred = model.predict(test_set)
#print(np.round(model.predict_proba(test_set),2))

cm = confusion_matrix(test_labs, pred)
print("\nThe confusion matrix is:")
print(cm)
d = {'Actual':test_labs,'Predicted':pred}
df = pd. DataFrame(d)

df.to_csv('tv_cm.csv')