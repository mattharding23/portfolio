##Using information gain
dt_ox2 = rpart(train_set$Dis_Oxygen ~ .,
               data=train_set,
               method = 'class',
               control=rpart.control(minsplit=2, 
                                     minbucket=1)
)
#summary(dt_ox2)



## Visual for dt_ox2


fancyRpartPlot(dt_ox2)
png('dt_ox2.png',width=1000, height=600)
fancyRpartPlot(dt_ox2)
dev.off()