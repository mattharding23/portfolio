# k = 6 seems like an optimal number for k
set.seed(102)
k = 4
clus = kmeans(dat, centers = k, nstart = 25)
dat$cluster = clus$cluster


axx <- list(
  title = "Turbidity (NTU))"
)

axy <- list(
  title = "Dissolved Oxygen (% Saturation)"
)

axz <- list(
  title = "pH"
)
fig = plot_ly(x = dat$num_eotb.Turb_NTU, y = dat$num_eotb.DO_pctSat, z = dat$num_eotb.pH)
fig = fig %>%  
  add_markers(color = dat$cluster, size=.01) %>%
  layout(title = '3D Cluster Plot of Turbidity, Dissolved Oxygen, and pH',
         scene = list(
           xaxis=axx,
           yaxis=axy, 
           zaxis=axz))
fig