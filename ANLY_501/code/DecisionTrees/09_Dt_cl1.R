dt_cl = rpart(train_set$Chlorophyll ~ .,
              data=train_set,
              method = 'class',
              control=rpart.control(minsplit=2, 
                                    minbucket=1,
                                    cp = .0125)
              
)
#summary(dt_cl)


## Visual for dt_cl

fancyRpartPlot(dt_cl)
png('dt_cl.png',width=1000, height=600)
fancyRpartPlot(dt_cl)
dev.off()