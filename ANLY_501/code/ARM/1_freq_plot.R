eotb_trans = read.transactions("eotb_grouped.csv",
                               sep =",", 
                               format("basket"),
                               rm.duplicates = TRUE)

png(file="freq_plot.png",width = 1000,height = 600)
freq_plot = itemFrequencyPlot(eotb_trans, 
                              topN=15,  
                              cex.names=1.5, 
                              cex.axis = 1.5,
                              cex.lab = 1.5,
                              main = "Item Relative Frequency Plot", 
                              col = "navy")
dev.off()