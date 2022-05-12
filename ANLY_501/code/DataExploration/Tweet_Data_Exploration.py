#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 09:32:48 2021

@author: mattharding
"""

## LIBRARIES ------------------------------------------------
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import text 
import numpy as np
import pandas as pd
import os
import csv
import warnings
warnings.filterwarnings('ignore')

#-----------------


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
cv = CountVectorizer(input='filename',
                        stop_words=text.ENGLISH_STOP_WORDS.union('https')
                        )
# Get Document term matrix
dtm = cv.fit_transform(file_names)

# Extract column names
col_names = cv.get_feature_names()

# Turn into pandas df
tweets_df = pd.DataFrame(dtm.toarray(),columns=col_names)

# Insert labels column
tweets_df.insert(loc=0, column='Label', value=labels)

#remove number values
keep_words = [col for col in tweets_df.columns if col.isalpha()]

tweets_df = tweets_df[keep_words]

# # Remove other words not caught by stopwords
more_stop_words = ['https','rt','ivepetthatdog']
keep_words = [col for col in tweets_df.columns if not col in more_stop_words]
tweets_df = tweets_df[keep_words]

# # Create wordcloud
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# # Find occurance frequencies of each word 
freq = dict(zip(tweets_df.columns,tweets_df.sum(axis = 0)))
freq.pop('Label',None)
freq = {key: value for key, value in freq.items() if value > 2}

# # Create word cloud
wordcloud = WordCloud(background_color='white').fit_words(freq)

# # View word cloud
fig, ax = plt.subplots(figsize=(15,15))
_ = ax.imshow(wordcloud, interpolation='bilinear')
_ = ax.axis("off")
fig.savefig(f'{path}all_tweets_wordcloud.png', bbox_inches = 'tight', pad_inches = 0)

#-------------------------


# DATA EXPLORATION


#-------------------------

# # Make more word clouds based on labels
label_names = np.unique(labels)
# # First label applies to all tweets,others are specified words added to first word.
# df of 2nd label
df_2 = tweets_df[tweets_df['Label'] == label_names[1]]
# df of 3rd label
df_3 = tweets_df[tweets_df['Label'] == label_names[2]]
# df of 4th label
df_4 = tweets_df[tweets_df['Label'] == label_names[3]]

# out dfs together in a list to loop through
dfs = [df_2,df_3,df_4]

# For naming files
names = ['environment','river','tributaries']
index = 0

# Loop through dfs and output word clouds
for df in dfs:
    freq = dict(zip(df.columns,df.sum(axis = 0)))
    freq.pop('Label',None)
    freq = {key: value for key, value in freq.items() if value > 2}
    # # Create word cloud
    wordcloud = WordCloud(background_color='white').fit_words(freq)

    # # View word cloud
    fig, ax = plt.subplots(figsize=(15,15))
    _ = ax.imshow(wordcloud, interpolation='bilinear')     
    _ = ax.axis("off")
    fig.savefig(f'{path}{names[index]}_wordcloud.png', bbox_inches = 'tight', pad_inches = 0)
    index += 1
    
