dat$cond = 'Neutral'
dat$cond[dat$pH < 6.5] = 'Acidic'
dat$cond[dat$pH > 7.5] = 'Basic'

p = ggplot()+
  geom_point(data = dat[1:750000,], aes(y = pH[1:750000],x = DateTime[1:750000], color = cond))+
  labs(
    x = 'Date',
    y = 'pH',
    title = 'pH Over Time (2007 - 2011)'
  )+
  theme(plot.title = element_text(size=17, face="bold",
                                  margin = margin(10, 0, 10, 0),hjust =.5),
        axis.text.x = element_text(angle = 90, vjust = 0.5),
        panel.grid.major = element_blank(), 
        panel.grid.minor = element_blank(),
        panel.background = element_blank())+
  scale_x_datetime(date_breaks = "3 months", date_labels = "%m %Y")+
  scale_color_manual(values = c("red3", "green3","grey"))


p