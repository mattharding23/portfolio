
# Twitter ---------------------------------------------------------------------
library(rtweet)
library(twitteR)
library(ROAuth)
library(jsonlite)
library(dotenv)

load_dot_env()

## Twitter Keys
consumer_key = TWITTER_CONSUMER_KEY
consumer_secret = TWITTER_CONSUMER_SECRET
access_token = TWITTER_ACCESS_TOKEN
access_secret = TWITTER_ACCESS_SECRET


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
