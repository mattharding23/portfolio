ggplot() +
  geom_histogram(aes(x = dataset$Salinity_ppt),bins = 10)+
  labs(
    x = 'Salinity (ppt)',
    y = 'Count',
    title = 'Histogram of Salinity Values'
  )+
  theme(plot.title = element_text(size=17, face="bold",
                                  margin = margin(10, 0, 10, 0),hjust =.5))