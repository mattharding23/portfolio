dat$cond = 'Neutral'
dat$cond[dat$pH < 6.5] = 'Acidic'
dat$cond[dat$pH > 7.5] = 'Basic'
ggplot(data = dat) +
  geom_point(aes(x = pH, y = DO_pctSat, color = cond),size = .1)+
  geom_hline(yintercept=70, linetype="solid", color = "black",size=1.5)+
  geom_text(aes(8, 70, label = 'Dangerous Oxygen Line', vjust = - 1))+
  scale_color_manual(values = c("red3","green3", "grey"))+
  theme(plot.title = element_text(size=17, face="bold",
                                  margin = margin(10, 0, 10, 0),hjust =.5),
        panel.grid.major = element_blank(), 
        panel.grid.minor = element_blank(),
        panel.background = element_blank())+
  labs(
    x = 'pH',
    y = 'Dissolved Oxygen',
    title = 'Relationship Between pH and Dissolved Oxygen')

