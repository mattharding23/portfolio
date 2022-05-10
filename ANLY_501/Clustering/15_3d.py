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