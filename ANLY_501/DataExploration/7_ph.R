ggplot(dat, aes(x = pH,)) +
  geom_histogram(bins = 50, fill = 'dodgerblue') +       
  theme(plot.title = element_text(size=17, face="bold",
                                  margin = margin(10, 0, 10, 0),hjust =.5),
        axis.text.y = element_blank(),
        axis.ticks.y = element_blank())+
  labs(                                         
    x = "pH",
    y = "Frequency",
    title = "pH at Different Stations") +
  facet_wrap(~Station, scales = "free_y", ncol = 1) 