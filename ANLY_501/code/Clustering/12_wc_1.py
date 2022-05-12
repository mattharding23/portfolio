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