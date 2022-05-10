#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 11:12:26 2021

@author: mattharding
"""

#%% 
## LIBRARIES ------------------------------------------------
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN
from sklearn.cluster import AgglomerativeClustering
from sklearn.feature_extraction import text 
import numpy as np
import pandas as pd
import os
import csv
import warnings
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn import datasets
from wordcloud import WordCloud
from sklearn.preprocessing import StandardScaler
warnings.filterwarnings('ignore')

#%%
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

cv_clus = cv_df.drop(columns = 'Label')
tv_clus = tv_df.drop(columns = 'Label')




#%% 
img_path = path = '/Users/mattharding/Documents/Georgetown/Fall_2021/ANLY_501/Mod_3_assignment/'
# Data is labeled so it should cluster into those labels. However, I am going to check for an ideal k with an elbow plot
distortions = []
K = range(1,10)
for k in K:
    kmeanModel = KMeans(n_clusters=k)
    kmeanModel.fit(cv_clus)
    distortions.append(kmeanModel.inertia_)
plt.figure(figsize=(16,8))
plt.plot(K, distortions, 'bx-')
plt.xlabel('k')
plt.ylabel('Sum of Squares difference')
plt.title('The Elbow Method for Count Vectorizer of Tweet Data')
plt.show()
plt.savefig(f'{img_path}other_viz/cv.png', bbox_inches = 'tight', pad_inches = 0)


distortions = []
K = range(1,10)
for k in K:
    kmeanModel = KMeans(n_clusters=k)
    kmeanModel.fit(tv_clus)
    distortions.append(kmeanModel.inertia_)
plt.figure(figsize=(16,8))
plt.plot(K, distortions, 'bx-')
plt.xlabel('k')
plt.ylabel('Sum of Squares difference')
plt.title('The Elbow Method for TFIDF Vectorizer of Tweet Data')
plt.show()
plt.savefig(f'{img_path}other_viz/tv.png', bbox_inches = 'tight', pad_inches = 0)

#%%
# The elbow plot from the cv shows that 4 & 6 would be good k values while the tv shows that 4 would be good k values
# 4 Makes the most sense because that is how the data is labeled 

# Set k = 4
k = 4
# Run a Euclidean Distance K means clustering on the data
km = KMeans(n_clusters=k, init='k-means++', max_iter=200, n_init=10)
km.fit(cv_clus)
labels=km.labels_
prediction_kmeans = km.predict(cv_clus)
cv_clus.insert(loc=0, column='Cluster', value=labels)

#%%

# Create Word Clouds based on clusters


for i in range(0,k):
    
    # index only cluster i of dataframe
    df = cv_clus[cv_clus['Cluster'] == i]
    
    # Turn dataframe into frequency dictionary & remove labels. 
    freq = dict(zip(df.columns,df.sum(axis = 0)))
    freq.pop('Cluster',None)
    
    # Create word cloud
    wordcloud = WordCloud(background_color='white').fit_words(freq)

    # View word cloud
    fig, ax = plt.subplots(figsize=(15,15))
    _ = ax.imshow(wordcloud, interpolation='bilinear')     
    _ = ax.axis("off")
    fig.savefig(f'{img_path}k4_cv_wordclouds/clust_{i}.png', bbox_inches = 'tight', pad_inches = 0)


# Repeat for k = 6 for cv

#%%

cv_clus = cv_df.drop(columns = 'Label')

# Set k = 5
k = 6
# Run a Euclidean Distance K means clustering on the data
km = KMeans(n_clusters=k, init='k-means++', max_iter=200, n_init=10)
km.fit(cv_clus)
labels=km.labels_
prediction_kmeans = km.predict(cv_clus)
cv_clus.insert(loc=0, column='Cluster', value=labels)

#%%

# Create Word Clouds based on clusters
img_path = path = '/Users/mattharding/Documents/Georgetown/Fall_2021/ANLY_501/Mod_3_assignment/'

for i in range(0,k):
    
    # index only cluster i of dataframe
    df = cv_clus[cv_clus['Cluster'] == i]
    
    # Turn dataframe into frequency dictionary & remove labels. 
    freq = dict(zip(df.columns,df.sum(axis = 0)))
    freq.pop('Cluster',None)
    
    # Create word cloud
    wordcloud = WordCloud(background_color='white').fit_words(freq)

    # View word cloud
    fig, ax = plt.subplots(figsize=(15,15))
    _ = ax.imshow(wordcloud, interpolation='bilinear')     
    _ = ax.axis("off")
    fig.savefig(f'{img_path}k6_cv_wordclouds/clust_{i}.png', bbox_inches = 'tight', pad_inches = 0)

#%%
# Repeat kmeans with tv for k = 4
tv_clus = tv_df.drop(columns = 'Label')
# Set k = 3
k = 4

# Run a Euclidean Distance K means clustering on the data
km = KMeans(n_clusters=k, init='k-means++', max_iter=200, n_init=10)
km.fit(tv_clus)
labels=km.labels_
prediction_kmeans = km.predict(tv_clus)
tv_clus.insert(loc=0, column='Cluster', value=labels)

#%%

# Create Word Clouds based on clusters
img_path = path = '/Users/mattharding/Documents/Georgetown/Fall_2021/ANLY_501/Mod_3_assignment/'

for i in range(0,k):
    
    # index only cluster i of dataframe
    df = tv_clus[tv_clus['Cluster'] == i]
    
    # Turn dataframe into frequency dictionary & remove labels. 
    freq = dict(zip(df.columns,df.sum(axis = 0)))
    freq.pop('Cluster',None)
    
    # Create word cloud
    wordcloud = WordCloud(background_color='white').fit_words(freq)

    # View word cloud
    fig, ax = plt.subplots(figsize=(15,15))
    _ = ax.imshow(wordcloud, interpolation='bilinear')     
    _ = ax.axis("off")
    fig.savefig(f'{img_path}k4_tv_wordclouds/clust_{i}.png', bbox_inches = 'tight', pad_inches = 0)


#%%

tv_clus = tv_df.drop(columns = 'Label')
# Set k = 7
k = 3

# Run a Euclidean Distance K means clustering on the data
km = KMeans(n_clusters=k, init='k-means++', max_iter=200, n_init=10)
km.fit(tv_clus)
labels=km.labels_
prediction_kmeans = km.predict(tv_clus)

labs = ['environment','river','tributary']

centers = km.cluster_centers_

lab1_ind = tv_clus.columns.get_loc(labs[0])
lab2_ind = tv_clus.columns.get_loc(labs[1])
lab3_ind = tv_clus.columns.get_loc(labs[2])


C1=centers[0,(lab1_ind,lab2_ind,lab3_ind)]
C2=centers[1,(lab1_ind,lab2_ind,lab3_ind)]
C3=centers[2,(lab1_ind,lab2_ind,lab3_ind)]

x=C1[0],C2[0],C3[0]

y=C1[1],C2[1],C3[1]
z=C1[2],C2[2],C3[2]

fig1 = plt.figure(figsize=(12, 12))
ax1 = Axes3D(fig1, rect=[0, 0, .90, 1], elev=48, azim=134)

ax1.scatter(x,y,z, cmap="RdYlGn", edgecolor='k', s=2000)
ax1.w_xaxis.set_ticklabels([])
ax1.w_yaxis.set_ticklabels([])
ax1.w_zaxis.set_ticklabels([])

ax1.set_xlabel('Environment', fontsize=25)
ax1.set_ylabel('River', fontsize=25)
ax1.set_zlabel('Tributary', fontsize=25)
#plt.show()
