dt_ox1 = rpart(train_set$Dis_Oxygen ~ .,
               data=train_set,
               method = 'class',
               control=rpart.control(minsplit=2, 
                                     minbucket=1) 
               #cp=0.015)
)
#summary(dt_ox1)


## Visual for dt_ox1

fancyRpartPlot(dt_ox1)
png('dt_ox1.png',width=1000, height=600)
fancyRpartPlot(dt_ox1)
dev.off()