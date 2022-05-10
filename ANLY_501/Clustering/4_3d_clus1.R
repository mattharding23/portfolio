# k = 4 seems like an optimal number for k
set.seed(102)

k = 4 
clus = kmeans(dat, centers = k)
dat$cluster = clus$cluster


axx <- list(
  title = "Temperature (F)"
)

axy <- list(
  title = "Salinity (ppt)"
)

axz <- list(
  title = "pH"
)
fig = plot_ly(x = dat$num_eotb.T_Fahr, y = dat$num_eotb.Salinity_ppt, z = dat$num_eotb.pH)
fig = fig %>%  
  add_markers(color = dat$cluster, size=.01) %>%
  layout(title = '3D Cluster Plot of Temperature, Salinity, and pH',
         scene = list(
           xaxis=axx,
           yaxis=axy, 
           zaxis=axz))
fig