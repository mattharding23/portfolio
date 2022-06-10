import praw
import pandas as pd
reddit = praw.Reddit(client_id='', client_secret='', user_agent='WebScraping') #Please enter your id and secret keys before running code.

tf_posts = []
cc_posts = []
tf_subreddit = reddit.subreddit('trackandfield') #selecting track and field sub reddit
cc_subreddit = reddit.subreddit('CrossCountry') #selecting cross country sub reddit
for post in tf_subreddit.hot(limit=500):
    tf_posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
tf_posts = pd.DataFrame(tf_posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])

for post in cc_subreddit.hot(limit=500):
    cc_posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
cc_posts = pd.DataFrame(cc_posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])

all_posts = tf_posts.append(cc_posts)
all_posts