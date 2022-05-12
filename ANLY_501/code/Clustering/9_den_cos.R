set.seed(102)
df = data.frame(matrix(ncol = 7, nrow = 0))

for (i in 1:12){
  dat = eotb[eotb$month_col==i,4:10]
  means = colMeans(dat)
  df = rbind(df,means)
}
# Get rid of month column, not actually numeric data
df = df[,1:6]
c_names = c('Salinity','pH','Dissolved Oxygen','Turbidity','Chlorophyll','Temperature')
colnames(df) = c_names

df = scale(df)

dist_eucl = dist(df, method = "euclidean")
dist_man = dist(df, method = "manhattan")
dist_cos <- distance(as.matrix(df), method="cosine",use.row.names = F)
dist_cos<- as.dist(dist_cos)
labels = c('1','2','3','4','5','6','7','8','9','10','11','12')

eucl_clust = hclust(dist_eucl, method = "ward.D2" )
man_clust = hclust(dist_man, method = "ward.D2" )
cos_clust = hclust(dist_cos, method = "ward.D2" )
cos_clust$labels = labels


cosi = ggdendrogram(cos_clust)+
  labs(
    x = 'Months',
    y = 'Height',
    subtitle = 'Cosine Similarity Distance Method',
    title = 'Dendogram of Monthly Average Water Quality Data')+
  theme(plot.title = element_text(size=17, face="bold", 
                                  margin = margin(10, 0, 10, 0),hjust =.5),
        plot.subtitle = element_text(hjust =.5))
