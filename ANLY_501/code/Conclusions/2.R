#dataset = read.csv('EOTB_Cleaned.csv')
dataset$cond = 'Not Low Oxygen'
dataset$cond[dataset$DO_pctSat < 70] = 'Low Oxygen'
ggplot(data = dataset[dataset$month_col == c(6,7,8,9),]) +
  geom_histogram(aes(x = DO_pctSat, fill = cond,color = cond), bins = 100) +
  labs(                                         
    x = "Dissolved Oxygen Level",
    y = "Frequency",
    title = "Frequency of Low Oxygen Level Events") +
  scale_fill_manual(values = c("red", "green"))+
  scale_color_manual(values = c("red3", "green3"))+
  theme(plot.title = element_text(size=17, face="bold", 
                                  margin = margin(10, 0, 10, 0),hjust =.5),
        panel.grid.major = element_blank(), 
        panel.grid.minor = element_blank(),
        panel.background = element_blank())
ggsave('Do_hist_summer.png',dpi = 'retina')
summer = dataset[dataset$month_col == c(6,7,8,9),]
length(summer$cond[summer$cond == 'Low Oxygen'])/length(summer$cond)