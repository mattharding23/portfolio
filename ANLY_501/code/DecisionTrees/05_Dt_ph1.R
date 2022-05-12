dt_ph = rpart(train_set$pH ~ .,
              data=train_set,
              method = 'class',
              control=rpart.control(minsplit=2, 
                                    minbucket=1) 
              #cp=0.00725)
)
#summary(dt_ph)

## Visual for dt_ph
fancyRpartPlot(dt_ph)
png('dt_ph.png',width=1000, height=600)
fancyRpartPlot(dt_ph)
dev.off()