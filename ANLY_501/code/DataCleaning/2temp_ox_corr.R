ggplot(data = dataset )+
  geom_point(aes(T_Fahr,DO_mg.L)) +
    labs(
    x = 'Temperature (F)',
    y = 'Dissolved Oxygen (mg/L)',
    subtitle = 'Temperature vs Dissolved Oxygen',
    title = 'Correlation Plot'
  )+
  theme(plot.title = element_text(size=17, face="bold",
    margin = margin(10, 0, 10, 0),hjust =.5),
    plot.subtitle = element_text(hjust =.5))
