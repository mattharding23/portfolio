p = ggplot()
p = p+  geom_point(data = dat[1:725000,], aes(y = Salinity_ppt[1:725000],x = DateTime[1:725000], color = 'darkred',alpha = 0.05))
p = p +  labs(
  x = 'Date',
  y = 'Salinity (ppt)',
  title = 'Salinity Over Time (2007 - 2011)'
)
p = p +  theme(plot.title = element_text(size=17, face="bold",
                                         margin = margin(10, 0, 10, 0),hjust =.5),
               legend.position = "none",
               axis.text.x = element_text(angle = 90, vjust = 0.5))
p = p +  scale_x_datetime(date_breaks = "3 months", date_labels = "%m %Y")
