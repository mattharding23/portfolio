dataset = read.csv('EOTB_Cleaned.csv')
dat = dataset
dat$Legend = 'Sufficient Oxygen'
dat$Legend[dat$DO_pctSat < 70 & dat$pH < 7] = 'Low Oxygen, Acidic'
dat$Legend[dat$DO_pctSat < 70 & dat$pH > 7] = 'Low Oxygen, Basic'
dat$month_name[dat$month_col == 1] = 'January'
dat$month_name[dat$month_col == 2] = 'February'
dat$month_name[dat$month_col == 3] = 'March'
dat$month_name[dat$month_col == 4] = 'April'
dat$month_name[dat$month_col == 5] = 'May'
dat$month_name[dat$month_col == 6] = 'June'
dat$month_name[dat$month_col == 7] = 'July'
dat$month_name[dat$month_col == 8] = 'August'
dat$month_name[dat$month_col == 9] = 'September'
dat$month_name[dat$month_col == 10] = 'October'
dat$month_name[dat$month_col == 11] = 'November'
dat$month_name[dat$month_col == 12] = 'December'



ggplot(data = dat) +
  geom_point(aes(x = fct_reorder(month_name,-month_col), y = pH, color = Legend), alpha = .25, size = 2)+
  geom_hline(yintercept=7, linetype="solid", color = "black",size=1.25)+
  geom_text(aes(12, 7, label = 'Basic', vjust = - 1.25),color = "blue3")+
  geom_text(aes(12, 7, label = 'Acidic', vjust = 1.5),color ="red3")+
  
  labs(                                         
    x = "",
    y = "pH",
    title = "Low Oxygen Events by Top Predictors")+
  scale_color_manual(values = c("red3","blue3", "grey"))+
  theme(plot.title = element_text(size=17, face="bold", 
                                  margin = margin(10, 0, 10, 0),hjust =.5),
        panel.grid.major = element_blank(), 
        panel.grid.minor = element_blank(),
        panel.background = element_blank(),
        axis.text.x = element_text(angle = 60, vjust = 0.5))
