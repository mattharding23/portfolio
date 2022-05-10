set.seed(102)

dat = data.frame(num_eotb$Turb_NTU,num_eotb$DO_pctSat,num_eotb$pH)
wss = (nrow(dat)-1)*sum(apply(dat,2,var))
for(i in 2:10)  wss[i] <- sum(kmeans(dat,
                                     centers=i)$withinss)
ggplot()+
  geom_point(aes(x = 1:10, y = wss, color = 'red'))+
  geom_line(aes(x = 1:10, y = wss))+
  labs(
    x = 'k',
    y = 'Sum of Squares',
    title = 'Elbow Plot for k clusters of the Temperature, Salinity, and pH Variables')+
  theme(plot.title = element_text(size=17, face="bold", 
                                  margin = margin(10, 0, 10, 0),hjust =.5),
        legend.position = "none")+
  scale_x_continuous(breaks = 2:10)