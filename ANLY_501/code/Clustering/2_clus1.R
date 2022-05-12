
#  5, and 8 appear to be optimal number of clusters for dataset.
set.seed(102)
k = 5

# Now kmeans clustering 
clus = kmeans(num_eotb, centers = k)




dat_clus = clus %>%
  fviz_cluster(data = num_eotb, show.clust.cent = TRUE,geom = 'point', pointsize = .1,ellipse = TRUE) + 
  theme(plot.title = element_text(size=17, 
                                  face="bold",
                                  margin = margin(10, 0, 10, 0),
                                  hjust =.5),
        panel.grid.minor.x = element_blank()) +
  
  labs( title = 'Clusters of 2019 Water Quality Data Subset')