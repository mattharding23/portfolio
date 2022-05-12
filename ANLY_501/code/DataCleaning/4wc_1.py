#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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