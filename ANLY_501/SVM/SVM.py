#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 15:23:49 2021

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

# svm needs two labels, will use environment and river label
cv_svm_df = cv_df[cv_df['Label'] != 'chesapeakebay' ]
tv_svm_df = tv_df[tv_df['Label'] != 'chesapeakebay']
cv_svm_df = cv_svm_df[cv_df['Label'] != 'tributary']
tv_svm_df = tv_svm_df[tv_df['Label'] != 'tributary']
# Save dfs to csvs
cv_svm_df.to_csv('Labeled_cv_data.csv')
tv_svm_df.to_csv('Labeled_tv_data.csv')

#%% SVM on Count Vectorizer Data

# Split into testing & training dataframes
train_set, test_set = train_test_split(cv_svm_df, test_size=0.3,random_state=12)

# Remove and save labels from test data
test_labs = test_set['Label']
test_set = test_set.drop(['Label'], axis=1)

# Separate labels from training set
train_labs = train_set['Label']
train_set = train_set.drop(['Label'], axis=1)

# Create SVM models. Try multiple kernels, for now keep cost = .5

#------- LINEAR -----------
lin_model=LinearSVC(C=.5)
lin_model.fit(train_set, train_labs)
lin_pred = lin_model.predict(test_set)
#print(np.round(model.predict_proba(test_set),2))

cm = confusion_matrix(test_labs, lin_pred)
print("\nThe Linear confusion matrix is:")
print(cm)


#--------------------------

#------- RBF --------------
rbf_model=sklearn.svm.SVC(C=.5, 
                           kernel='rbf', 
                           verbose=True, 
                           gamma="auto")
rbf_model.fit(train_set, train_labs)
rbf_pred = rbf_model.predict(test_set)
#print(np.round(model.predict_proba(test_set),2))

cm = confusion_matrix(test_labs, rbf_pred)
print("\nThe RBF confusion matrix is:")
print(cm)


#--------------------------

#------- quadratic --------
quad_model=sklearn.svm.SVC(C=.5, kernel='poly',degree=2,
                           gamma="auto", verbose=True)
quad_model.fit(train_set, train_labs)
quad_pred = quad_model.predict(test_set)
#print(np.round(model.predict_proba(test_set),2))

cm = confusion_matrix(test_labs, quad_pred)
print("\nThe quadratic confusion matrix is:")
print(cm)

#--------------------------

#------- cubic ------------
cub_model=sklearn.svm.SVC(C=.5, kernel='poly',degree=3,
                           gamma="auto", verbose=True)
cub_model.fit(train_set, train_labs)
cub_pred = cub_model.predict(test_set)
#print(np.round(model.predict_proba(test_set),2))

cm = confusion_matrix(test_labs, cub_pred)
print("\nThe cubic confusion matrix is:")
print(cm)



#--------------------------

d = {'Actual':test_labs,'Predicted':lin_pred}
df = pd. DataFrame(d)
df.to_csv('cv_cm.csv')
    
import matplotlib.pyplot as plt
## Credit: https://medium.com/@aneesha/visualising-top-features-in-linear-svm-with-scikit-learn-and-matplotlib-3454ab18a14d
## Define a function to visualize the TOP words (variables)
MODEL=lin_model
COLNAMES=train_set.columns
top_features=10
    ## Model if SVM MUST be SVC, RE: SVM_Model=LinearSVC(C=10)
coef = MODEL.coef_.ravel()
top_positive_coefficients = np.argsort(coef,axis=0)[-top_features:]
top_negative_coefficients = np.argsort(coef,axis=0)[:top_features]
top_coefficients = np.hstack([top_negative_coefficients, top_positive_coefficients])
    # create plot
plt.figure(figsize=(15, 5)) 
colors = ["red" if c < 0 else "blue" for c in coef[top_coefficients]]
plt.bar(  x=  np.arange(2 * top_features)  , height=coef[top_coefficients], width=.5,  color=colors)
feature_names = np.array(COLNAMES)#,np.array(COLNAMES),np.array(COLNAMES)]
#feature_names = np.concatenate(feature_names)
plt.xticks(np.arange(0, (2*top_features)), feature_names[top_coefficients], rotation=60, ha="right")
plt.show()
plt.savefig('cv_features.png')
    

# %% Plotting top two features
from sklearn.svm import SVC
X = np.array([train_set["river"], train_set["environment"]])
X = X.transpose()

y = train_labs

from sklearn.preprocessing import LabelBinarizer
from sklearn import preprocessing
lb = preprocessing.LabelBinarizer()
y=lb.fit_transform(y)

y = np.array(y)
y = y.ravel()  


clf = SVC(C=1, kernel="linear")
clf.fit(X, y) 


margin = 2 / np.sqrt(np.sum(clf.coef_ ** 2))

w = clf.coef_[0]

a = -w[0] / w[1]

xx = np.linspace(0, 10)

yy = a * xx - (clf.intercept_[0]) / w[1]

yy_down = yy + .5*margin
yy_up = yy - .5*margin


plt.clf()
plt.plot(xx, yy, 'r-')
plt.plot(xx, yy_down, 'k--')
plt.plot(xx, yy_up, 'k--')
plt.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1], s=10,
                facecolors='none', zorder=5)
plt.scatter(X[:, 0], X[:, 1], c=y, zorder=5, cmap=plt.cm.Paired)
plt.axis('tight')
plt.savefig('cv_svm.png')



#%% SVM on tfidf Vectorizer Data

# Split into testing & training dataframes
train_set, test_set = train_test_split(tv_svm_df, test_size=0.3,random_state=12)

# Remove and save labels from test data
test_labs = test_set['Label']
test_set = test_set.drop(['Label'], axis=1)

# Separate labels from training set
train_labs = train_set['Label']
train_set = train_set.drop(['Label'], axis=1)

# Create SVM models. Try multiple kernels, for now keep cost = .5

#------- LINEAR -----------
lin_model=LinearSVC(C=.5)
lin_model.fit(train_set, train_labs)
lin_pred = lin_model.predict(test_set)
#print(np.round(model.predict_proba(test_set),2))

cm = confusion_matrix(test_labs, lin_pred)
print("\nThe Linear confusion matrix is:")
print(cm)


#--------------------------

#------- RBF --------------
rbf_model=sklearn.svm.SVC(C=.5, 
                           kernel='rbf', 
                           verbose=True, 
                           gamma="auto")
rbf_model.fit(train_set, train_labs)
rbf_pred = rbf_model.predict(test_set)
#print(np.round(model.predict_proba(test_set),2))

cm = confusion_matrix(test_labs, rbf_pred)
print("\nThe RBF confusion matrix is:")
print(cm)


#--------------------------

#------- quadratic --------
quad_model=sklearn.svm.SVC(C=.5, kernel='poly',degree=2,
                           gamma="auto", verbose=True)
quad_model.fit(train_set, train_labs)
quad_pred = quad_model.predict(test_set)
#print(np.round(model.predict_proba(test_set),2))

cm = confusion_matrix(test_labs, quad_pred)
print("\nThe quadratic confusion matrix is:")
print(cm)


#--------------------------

#------- cubic ------------
cub_model=sklearn.svm.SVC(C=.5, kernel='poly',degree=3,
                           gamma="auto", verbose=True)
cub_model.fit(train_set, train_labs)
cub_pred = cub_model.predict(test_set)
#print(np.round(model.predict_proba(test_set),2))

cm = confusion_matrix(test_labs, cub_pred)
print("\nThe cubic confusion matrix is:")
print(cm)


#--------------------------
d = {'Actual':test_labs,'Predicted':lin_pred}
df = pd. DataFrame(d)
df.to_csv('tv_cm.csv')

    
## Credit: https://medium.com/@aneesha/visualising-top-features-in-linear-svm-with-scikit-learn-and-matplotlib-3454ab18a14d
## Define a function to visualize the TOP words (variables)
MODEL=lin_model
COLNAMES=train_set.columns
top_features=10
    ## Model if SVM MUST be SVC, RE: SVM_Model=LinearSVC(C=10)
coef = MODEL.coef_.ravel()
top_positive_coefficients = np.argsort(coef,axis=0)[-top_features:]
top_negative_coefficients = np.argsort(coef,axis=0)[:top_features]
top_coefficients = np.hstack([top_negative_coefficients, top_positive_coefficients])
    # create plot
plt.figure(figsize=(15, 5)) 
colors = ["red" if c < 0 else "blue" for c in coef[top_coefficients]]
plt.bar(  x=  np.arange(2 * top_features)  , height=coef[top_coefficients], width=.5,  color=colors)
feature_names = np.array(COLNAMES)#,np.array(COLNAMES),np.array(COLNAMES)]
#feature_names = np.concatenate(feature_names)
plt.xticks(np.arange(0, (2*top_features)), feature_names[top_coefficients], rotation=60, ha="right")
plt.show()
plt.savefig('tv_features.png')
    

# %% Plotting top two features
X = np.array([train_set["river"], train_set["environment"]])
X = X.transpose()
y = train_labs

lb = preprocessing.LabelBinarizer()
y=lb.fit_transform(y)

y = np.array(y)
y = y.ravel()  


clf = SVC(C=1, kernel="linear")
clf.fit(X, y) 


margin = 2 / np.sqrt(np.sum(clf.coef_ ** 2))


w = clf.coef_[0]

a = -w[0] / w[1]

xx = np.linspace(0, 10)

yy = a * xx - (clf.intercept_[0]) / w[1]


yy_down = yy + .5*margin
yy_up = yy - .5*margin


plt.clf()
plt.plot(xx, yy, 'r-')
plt.plot(xx, yy_down, 'k--')
plt.plot(xx, yy_up, 'k--')
plt.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1], s=10,
                facecolors='none', zorder=5)
plt.scatter(X[:, 0], X[:, 1], c=y, zorder=5, cmap=plt.cm.Paired)
plt.axis('tight')
plt.savefig('tv_svm.png')


