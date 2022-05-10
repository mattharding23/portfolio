
# Twitter ---------------------------------------------------------------------
library(rtweet)
library(twitteR)
library(ROAuth)
library(jsonlite)

## Twitter Keys
consumer_key = '3EuROHEpPcp45Gl7kU86X9JfT'
consumer_secret = '81jx9G70Neb7xbThikeKMb0nRYn7OZYuLkAVZTgByvZPeaWfJo'
access_token = '1410722016081108994-LP9HQ1kqveMY0cAN55OvY98gfCZh8W'
access_secret = '2Hgy2Qyymw01vh1ODyvSI1y3OqpTDKmTBpiMlWpAjGo42'


## Setup
# URLs
requestURL='https://api.twitter.com/oauth/request_token'
accessURL='https://api.twitter.com/oauth/access_token'
authURL='https://api.twitter.com/oauth/authorize'

# Twitter authorization
setup_twitter_oauth(consumer_key,consumer_secret,access_token,access_secret)

# Get tweets
search1<-twitteR::searchTwitter("#ChesapeakeBay",n=100, since="2021-06-01")

#Create Data frame
search_DF2 <- twListToDF(search1)
search_DF2$text[1]

# Save data frame to csv
file_name = 'CB_tweets.csv'
myfile = file(file_name)
write.csv(search_DF2,"CB_tweets.csv", row.names = FALSE)
close(myfile)
