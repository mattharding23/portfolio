dt_cl2 = rpart(train_set$Chlorophyll ~ .,
               data=train_set,
               method = 'class',
               control=rpart.control(minsplit=2, 
                                     minbucket=1,
                                     cp = .0205)
               
)
summary(dt_cl2)

## Visual for dt_cl
fancyRpartPlot(dt_cl2)
png('dt_cl2.png',width=1000, height=600)
fancyRpartPlot(dt_cl2)
dev.off()