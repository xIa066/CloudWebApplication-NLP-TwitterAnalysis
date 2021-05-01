import pandas as pd
import numpy as np
import tweepy
import sys
def api_connect(log):
    consumer_key = log['API_KEY']
    consumer_secret_key = log['API_SECRET_KEY']
    access_token = log['ACCESS_TOKEN']
    access_token_secret = log['ACCESS_TOKEN_SECRET']
    try:
        authenticate = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
        authenticate.set_access_token(access_token, access_token_secret)
        api = tweepy.API(authenticate, wait_on_rate_limit=True)
        api.verify_credentials()
        places = api.geo_search(query=log['COUNTRY'], granularity="country")
        place_id = places[0].id
        conn = 'Authentication OK'
    except:
        api =None
        place_id= None
        conn = "Error during authentication"
    return api, conn, place_id


def toDataFrame(tweets,hashtag):

    DataSet = pd.DataFrame()

    DataSet['tweetText'] = [tweet.text for tweet in tweets]
    DataSet['tweetCreated'] = [tweet.created_at for tweet in tweets]
    DataSet['userLocation'] = [tweet.user.location for tweet in tweets]
    DataSet['Coordinates'] = [np.average(tweet._json['place']['bounding_box']['coordinates'][0], axis=0) for tweet in tweets]
    tweets_place= []
    for tweet in tweets:
        if tweet.place:
            tweets_place.append(tweet.place.full_name)
        else:
            tweets_place.append('null')
    DataSet['TweetPlace'] = [i for i in tweets_place]
    return DataSet

def fun_neu_fetch(api, place_id, log):
    list_hashtags = log['NEUTRAL_HASHTAGS'].dropna()
    list_hashtags= list(list_hashtags)

    df_neutral = pd.DataFrame()
    if (not api):
        print ("Can't Authenticate")
        sys.exit(-1)
    else:
        for tag in list_hashtags:
            print(tag)
            cursor = tweepy.Cursor(api.search, q= tag+" ; place:%s" % place_id,lang='en')
            results=[]
            for item in cursor.items():
                results.append(item)

            DataSet_mini = toDataFrame(results,tag)
            df_neutral= df_neutral.append(DataSet_mini)
    df_neutral.to_csv("./static/neutral_tweet_extracted.csv",index=False)
    return df_neutral

def fun_lab_fetch(api, place_id, log):
    list_hashtags = log['LABOR_HASHTAGS'].dropna()
    list_hashtags= list(list_hashtags)
    df_labor = pd.DataFrame()
    if (not api):
        print ("Can't Authenticate")
        sys.exit(-1)
    else:
        for tag in list_hashtags:
            print(tag)
            cursor = tweepy.Cursor(api.search, q= tag+" ; place:%s" % place_id,lang='en')
            results=[]
            for item in cursor.items():
                results.append(item)

            DataSet_mini = toDataFrame(results,tag)
            df_labor= df_labor.append(DataSet_mini)
    df_labor.to_csv("./static/labor_tweet_extracted.csv",index=False)
    return df_labor

def fun_libl_fetch(api, place_id, log):
    list_hashtags = log['LIBERAL_HASHTAGS'].dropna()
    list_hashtags= list(list_hashtags)
    df_liberal = pd.DataFrame()
    if (not api):
        print ("Can't Authenticate")
        sys.exit(-1)
    else:
        for tag in list_hashtags:
            print(tag)
            cursor = tweepy.Cursor(api.search, q= tag+" ; place:%s" % place_id,lang='en')
            results=[]
            for item in cursor.items():
                results.append(item)

            DataSet_mini = toDataFrame(results,tag)
            df_liberal= df_liberal.append(DataSet_mini)
    df_liberal.to_csv("./static/liberal_tweet_extracted.csv",index=False)
    return df_liberal