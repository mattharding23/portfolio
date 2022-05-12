d <- melt(dat[,-c(1:4,11)])
ggplot(d,aes(x = value)) + 
  facet_wrap(~variable,scales = "free_x") + 
  geom_boxplot()
ggsave('var_box_plots.png')