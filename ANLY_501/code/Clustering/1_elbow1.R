# Data was too large to run Fviz so manually ran elbow method
set.seed(102)
wss = (nrow(num_eotb)-1)*sum(apply(num_eotb,2,var))
for(i in 2:15){
  wss[i] = sum(kmeans(num_eotb,centers=i)$withinss)
}
ggplot()+
  geom_point(aes(x = 1:15, y = wss, color = 'red'))+
  geom_line(aes(x = 1:15, y = wss))+
  labs(
    x = 'k',
    y = 'Sum of Squares',
    title = 'Elbow Plot for k clusters of the Water Quality Data Set')+
  theme(plot.title = element_text(size=17, face="bold", 
                                  margin = margin(10, 0, 10, 0),hjust =.5),
        legend.position = "none")+
  scale_x_continuous(breaks = 2:15)