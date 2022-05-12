png('par_coord_conf.png',width=1000, height=600)

plot(eotb_rules_conf[1:15], 
     method="paracoord", 
     control=list(alpha=.9, reorder=TRUE), 
     main = 'Parallel Coordinates Plot for Top 15 Confidence Items')

dev.off()