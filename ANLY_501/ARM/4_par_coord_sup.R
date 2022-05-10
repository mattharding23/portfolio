png('par_coord_sup.png',width=1000, height=600)
plot(eotb_rules_sup[1:15], method="paracoord", control=list(alpha=0.8, reorder=TRUE), main = 'Parallel Coordinates Plot for Top 15 Support Items')
dev.off()