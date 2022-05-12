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