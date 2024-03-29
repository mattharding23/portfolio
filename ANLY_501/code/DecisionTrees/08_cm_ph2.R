conf_matrix <- function(df.true, df.pred, title = "", true.lab ="True Class", pred.lab ="Predicted Class",
                        high.col = 'green3', low.col = 'white') {
  #convert input vector to factors, and ensure they have the same levels
  df.true <- as.factor(df.true)
  df.pred <- factor(df.pred, levels = levels(df.true))
  
  #generate confusion matrix, and confusion matrix as a pecentage of each true class (to be used for color) 
  df.cm <- table(True = df.true, Pred = df.pred)
  df.cm.col <- df.cm / rowSums(df.cm)
  
  #convert confusion matrices to tables, and binding them together
  df.table <- reshape2::melt(df.cm)
  df.table.col <- reshape2::melt(df.cm.col)
  df.table <- left_join(df.table, df.table.col, by =c("True", "Pred"))
  
  #calculate accuracy and class accuracy
  acc.vector <- c(diag(df.cm)) / c(rowSums(df.cm))
  class.acc <- data.frame(Pred = "Class Acc.", True = names(acc.vector), value = acc.vector)
  acc <- sum(diag(df.cm)) / sum(df.cm)
  
  #plot
  ggplot() +
    geom_tile(aes(x=Pred, y=True, fill=value.y),
              data=df.table, size=0.2, color=grey(0.5)) +
    geom_tile(aes(x=Pred, y=True),
              data=df.table[df.table$True==df.table$Pred, ], size=1, color="black", fill = 'transparent') +
    scale_x_discrete(position = "top",  limits = c(levels(df.table$Pred), "Class Acc.")) +
    scale_y_discrete(limits = rev(unique(levels(df.table$Pred)))) +
    labs(x=pred.lab, y=true.lab, fill=NULL,
         title= paste0(title, "\nAccuracy ", round(100*acc, 1), "%")) +
    geom_text(aes(x=Pred, y=True, label=value.x),
              data=df.table, size=4, colour="black") +
    geom_text(data = class.acc, aes(Pred, True, label = paste0(round(100*value), "%"))) +
    scale_fill_gradient(low=low.col, high=high.col, labels = scales::percent,
                        limits = c(0,1), breaks = c(0,0.5,1)) +
    guides(scale = "none") +
    theme_bw() +
    theme(panel.border = element_blank(), legend.position = "bottom",
          axis.text = element_text(color='black'), axis.ticks = element_blank(),
          panel.grid = element_blank(), axis.text.x.top = element_text(angle = 30, vjust = 0, hjust = 0)) +
    coord_fixed()
  
} 


# Function to create confusion matrix visual & table of stats
run_cm = function(dt,test,test_lab,pos = 1,tit = 'Statistics for Confusion Matrix',subt = NULL){
  # Make DT prediction
  dt_pre = predict(dt,test,type = 'class')
  
  # Create Confusion Matrix
  if(pos == 1){
    cm = confusionMatrix(dt_pre,test_lab, positive = 'true')
    
    # Convert statistics to DF & pull out desired statistics
    stats = as.data.frame(t(as.matrix(cm$byClass)))
    stats = stats[c(1,2,5,7),]}
  
  
  else{
    cm = confusionMatrix(dt_pre,test_lab)
    
    # Convert statistics to DF & pull out desired statistics
    stats = as.data.frame(cm$byClass[c(1,2,5,7)])
    colnames(stats) = ' '}
  
  
  
  # Create table with gt package
  stats_tb = gt(stats,rownames_to_stub = T)
  stats_tb = stats_tb %>%
    
    # Create title & Subtitle
    tab_header(
      title = tit,
      subtitle = subt)
  
  
  
  # Save table as variable
  cm_stats = stats_tb
  
  # Create confusion matrix visual and save as variable
  cm_viz = conf_matrix(test_lab,dt_pre)
  
  # Return CM visual & stats as a list
  return(list(cm_viz,cm_stats))
}

# Get confusion matrix visual & stats for dt_ph2
(dt_ph_viz2 = run_cm(dt_ph2,
                     test_set,
                     test_labs,
                     pos = 0,
                     subt = "For Predicting pH"))