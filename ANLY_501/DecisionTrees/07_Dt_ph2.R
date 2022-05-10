dt_ph2 = rpart(train_set$pH ~ .,
               data=train_set,
               method = 'class',
               control=rpart.control(minsplit=2, 
                                     minbucket=1) 
               #cp=0.00725)
)
summary(dt_ph2)


## Visual for dt_ph2 (independent of station variable)

fancyRpartPlot(dt_ph2)
png('dt_ph2.png',width=1000, height=600)
fancyRpartPlot(dt_ph2)
dev.off()