import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import re
from datetime import date

consumer_key =""
consumer_secret_key =""
access_token =""
access_token_secret =""

authenticate = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
authenticate.set_access_token(access_token, access_token_secret)
api = tweepy.API(authenticate, wait_on_rate_limit=True)

places = api.geo_search(query="Australia", granularity="country")
place_id = places[0].id
place_id

def tweet_scrap(words,numtweet):

    db = pd.DataFrame(columns=['username', 'description','created_at', 'location', 'following','followers', 'totaltweets', 'retweetcount', 'text', 'hashtags'])

    tweets = tweepy.Cursor(api.search, q=words+"; place:%s" % place_id, lang="en", since=date(2015,1,1)
                           , tweet_mode='extended').items(numtweet)

    list_tweets = [tweet for tweet in tweets]

    for tweet in list_tweets:
        username = tweet.user.screen_name
        description = tweet.user.description
        created_at = tweet.user.created_at
        location = tweet.user.location
        following = tweet.user.friends_count
        followers = tweet.user.followers_count
        totaltweets = tweet.user.statuses_count
        retweetcount = tweet.retweet_count
        hashtags = tweet.entities['hashtags']

# Retweets can be distinguished by a retweeted_status attribute
# in case it is an invalid reference, except block will be executed
        try:
            text = tweet.retweeted_status.full_text
        except AttributeError:
            text = tweet.full_text
        hashtext = list()
        for j in range(0, len(hashtags)):
            hashtext.append(hashtags[j]['text'])

        # Here we are appending all the extracted information in the DataFrame
        ith_tweet = [username, description, created_at, location, following,
                     followers, totaltweets, retweetcount, text, hashtext]
        db.loc[len(db)] = ith_tweet
        # filename = 'scraped_tweets.csv'
        # db.to_csv(filename)
    return db
df1 = tweet_scrap('elections', 10000)
