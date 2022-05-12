#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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