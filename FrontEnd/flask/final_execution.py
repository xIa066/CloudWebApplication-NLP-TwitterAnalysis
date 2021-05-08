#!/usr/bin/env python
# coding: utf-8

# ## Importing Libraries

# In[1]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')

import pandas as pd      
import numpy as np       
import seaborn as sns   
import matplotlib.pyplot as plt 
pd.set_option('display.max_rows', None)  
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
import warnings     
warnings.filterwarnings('ignore')
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import re
from datetime import date
import plotly.express as px
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import csv
import sys
import time
import typing
import matplotlib.pyplot as plt
import nltk
import typing
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# ## Twitter Account Setup

# consumer_key = 'mJTR0SDWEUuoFEHlWJEl7kIdY'
# consumer_secret_key = 'Qmd1mwcNP2csyrNNRp3YvEvQg0JUn3KbeUNAgIBk7jw9f3kQke'
# access_token = '1299380381158977538-5SnP9wIfkWGQnq0xvd1JR7A8u8JooI'
# access_token_secret = 'Rtj381olRgtl0Awm41tkoKIGrzI9dbX9z48uevBSlq2tj'
# 
# authenticate = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
# authenticate.set_access_token(access_token, access_token_secret)
# api = tweepy.API(authenticate, wait_on_rate_limit=True)
# places = api.geo_search(query="Australia", granularity="country")
# place_id = places[0].id

# In[2]:


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


# ## Tweet Extraction Function

# In[3]:


def toDataFrame(tweets,hashtag):

    DataSet = pd.DataFrame()

    DataSet['tweetText'] = [tweet.text for tweet in tweets]
    DataSet['_id'] = [str(tweet.id) for tweet in tweets]
    DataSet['userLocation'] = [tweet.user.location for tweet in tweets]
    DataSet['Coordinates'] = [np.average(tweet._json['place']['bounding_box']['coordinates'][0], axis=0) for tweet in tweets]
    DataSet['userID'] = [tweet.user.id for tweet in tweets]
    DataSet['userScreen'] = [tweet.user.screen_name for tweet in tweets]
    tweets_place= []
    for tweet in tweets:
        if tweet.place:
            tweets_place.append(tweet.place.full_name)
        else:
            tweets_place.append('null')
    DataSet['TweetPlace'] = [i for i in tweets_place]
    return DataSet


# ## Hashtag List

# In[4]:


list_hashtags = ['#Morrison','#climatechange','#Labor','#BlamingLabor','#NewsPoll',
                 '#ScottyMustGo','#ScottyDoesNothing','#SelfishAlbo','#scottyfromarketing'
                 ,'#ScottyFromPhotoOps','#LNPfail','#EnoughIsEnough','#ScoMo','#Albo2022',
                 '#liberal','#ScottyFromMarketing','#policyfail','#ScottyFromCoverUps' ,'#NotMyPM' ,'#March4Justice',
                 '#AlboForPM','#AFPraids','#ShameonLiberals', '#SelfishAlbo','#auspoll', 
                 '#auspol', '#COVID19', '#AusVotes2019', '#ausvotes','#onyourside', '#LeadershipFail'
                ]
labor_hashtags = ['#ScottyFromCoverUps', '#ScottyDoesNothing' ,'#NotMyPM' ,'#Labor',
                 '#March4Justice', '#EnoughIsEnough' ,'#scottyfromarketing', '#ScottyFromPhotoOps'
                 ,'#AlboForPM', '#Albo2022','#AFPraids','#ShameonLiberals']
liberal_hashtags = ['#NewsPoll', '#BlamingLabor', '#climatechange', '#Morrison','#BlamingLabor', '#SelfishAlbo',
                    '#ScoMo']


# ## Twitter Function Calling

# In[5]:


def df_neutral(api,place_id,log):
    # import hashtags
    list_hashtags = log['NEUTRAL_HASHTAGS'].dropna()
    list_hashtags= list(list_hashtags)
    
    df_neutral = pd.DataFrame()
    if (not api):
        print ("Can't Authenticate")
        sys.exit(-1)
    else:
        for tag in list_hashtags:
            cursor = tweepy.Cursor(api.search, q= tag+" ; place:%s" % place_id,lang='en')
            cursor1 = tweepy.Cursor(api.search, q= tag+" ; place:%s" % place_id,lang='en')
            results=[]
            for item in cursor.items():
                results.append(item)

            DataSet_mini = toDataFrame(results,tag)
            df_neutral= df_neutral.append(DataSet_mini)
            return df_neutral


# In[6]:


def df_liberal(api,place_id,log):
    # import hashtags
    list_hashtags = log['LIBERAL_HASHTAGS'].dropna()
    liberal_hashtags = list(list_hashtags)
    
    df_liberal = pd.DataFrame()
    if (not api):
        print ("Can't Authenticate")
        sys.exit(-1)
    else:
        for tag in liberal_hashtags:
            cursor = tweepy.Cursor(api.search, q= tag+" ; place:%s" % place_id,lang='en')
            results=[]
            for item in cursor.items():
                results.append(item)

            DataSet_mini = toDataFrame(results,tag)
            df_liberal= df_liberal.append(DataSet_mini)
            return df_liberal


# In[7]:


def df_labor(api,place_id,log):
    list_hashtags = log['LABOR_HASHTAGS'].dropna()
    labor_hashtags= list(list_hashtags)
    
    df_labor = pd.DataFrame()
    if (not api):
        print ("Can't Authenticate")
        sys.exit(-1)
    else:
        for tag in labor_hashtags:
            cursor = tweepy.Cursor(api.search, q= tag+" ; place:%s" % place_id,lang='en')
            results=[]
            for item in cursor.items():
                results.append(item)

            DataSet_mini = toDataFrame(results,tag)
            df_labor= df_labor.append(DataSet_mini)
            return df_labor


# df_neutral = pd.read_csv("neutral_tweet_extracted.csv")
# df_labor = pd.read_csv("labor_tweet_extracted.csv")
# df_liberal = pd.read_csv("liberal_tweet_extracted.csv")

# ## Importing Local Dataset, Cleaning and Filtering

# In[8]:


def gen_result():
    df_local = pd.read_csv('data6378341312468407048.csv')
    df_local = df_local[['fraser_annings_conservative_national_party_ordinary_votes',' socialist_alliance_ordinary_votes',
                  ' labor_ordinary_votes', ' the_greens_ordinary_votes', ' national_party_ordinary_votes',
                 ' liberal_ordinary_votes', ' united_australia_party_ordinary_votes',
                  ' katters_australian_party_kap_ordinary_votes',
                ' latitude', ' longitude', ' division_id', ' division_name', ' polling_place_name', ' state']]
    df_local.isna().sum()/df_local.shape[0]*100<69
    df_local.drop([' socialist_alliance_ordinary_votes', ' national_party_ordinary_votes', 
               ' katters_australian_party_kap_ordinary_votes'],
              axis=1, inplace=True)
    vote_result_division_wise = df_local.groupby(' division_name')[['fraser_annings_conservative_national_party_ordinary_votes',
              ' labor_ordinary_votes', ' the_greens_ordinary_votes',
             ' liberal_ordinary_votes', ' united_australia_party_ordinary_votes']].sum()
    lat_lon = df_local.groupby(' division_name')[[' latitude',' longitude']].agg(np.median)
    result = lat_lon.join(vote_result_division_wise, how='outer')
    result = result.loc[['Brisbane', 'Canberra', 'Adelaide', 'Melbourne', 'Newcastle', 'Perth', 'Sydney', 'North Sydney'], :]
    result = result.reset_index()
    result.columns = ['Division Name', 'Latitude', 'Longitude',
       'Conservative National Party',
       'Labor Party', 'Greens Party',
       'Liberal Party', 'United Australia Party']
    result.head(20)
    return result


# df_local.drop([' socialist_alliance_ordinary_votes', ' national_party_ordinary_votes', 
#                ' katters_australian_party_kap_ordinary_votes'],
#               axis=1, inplace=True)

# vote_result_division_wise = df_local.groupby(' division_name')[['fraser_annings_conservative_national_party_ordinary_votes',
#               ' labor_ordinary_votes', ' the_greens_ordinary_votes',
#              ' liberal_ordinary_votes', ' united_australia_party_ordinary_votes']].sum()
# lat_lon = df_local.groupby(' division_name')[[' latitude',' longitude']].agg(np.median)
# result = lat_lon.join(vote_result_division_wise, how='outer')
# result = result.loc[['Brisbane', 'Canberra', 'Adelaide', 'Melbourne', 'Newcastle', 'Perth', 'Sydney', 'North Sydney'], :]
# result = result.reset_index()
# result.columns = ['Division Name', 'Latitude', 'Longitude',
#        'Conservative National Party',
#        'Labor Party', 'Greens Party',
#        'Liberal Party', 'United Australia Party']
# result.head(20)

# ## Text Cleaning Function

# In[9]:


def remove_links(text):
    # Remove any hyperlinks that may be in the text starting with http
    import re
    return re.sub(r"http\S+", "", text)

def style_text(text:str):
    # Convert to lowercase
    return text.lower()

def remove_words(text_data:str,list_of_words_to_remove: typing.List):
    # Remove all words as specified in a custom list of words
    return [item for item in text_data if item not in list_of_words_to_remove]

def collapse_list_to_string(string_list):
    # This is to join back together the text data into a single string
    return ' '.join(string_list)

def remove_apostrophes(text):
    # Remove any apostrophes as these are irrelavent in our word cloud
    text = text.replace("'", "")
    text = text.replace('"', "")
    text = text.replace('`', "")
    text = re.sub(r'@\S+', "",text)
    text = re.sub(r'#\S+',"",text)
    return text


# ## Cleaning Twitter Text Data

# In[10]:


def clean_data(df_neutral,df_labor,df_liberal):
    nltk.download('stopwords')
    stopcorpus = stopwords.words('english')

    df_neutral['cleaned_text'] = df_neutral['tweetText'].astype(str).apply(remove_links)
    df_labor['cleaned_text'] = df_labor['tweetText'].astype(str).apply(remove_links)
    df_liberal['cleaned_text'] = df_liberal['tweetText'].astype(str).apply(remove_links)

    df_neutral['cleaned_text'] = df_neutral['cleaned_text'].astype(str).apply(style_text)
    df_labor['cleaned_text'] = df_labor['cleaned_text'].astype(str).apply(style_text)
    df_liberal['cleaned_text'] = df_liberal['cleaned_text'].astype(str).apply(style_text)

    df_neutral['cleaned_text'] = df_neutral['cleaned_text'].astype(str).apply(lambda x: remove_words(x.split(),stopcorpus))
    df_labor['cleaned_text'] = df_labor['cleaned_text'].astype(str).apply(lambda x: remove_words(x.split(),stopcorpus))
    df_liberal['cleaned_text'] = df_liberal['cleaned_text'].astype(str).apply(lambda x: remove_words(x.split(),stopcorpus))


    df_neutral['cleaned_text'] = df_neutral['cleaned_text'].apply(collapse_list_to_string)
    df_labor['cleaned_text'] = df_labor['cleaned_text'].apply(collapse_list_to_string)
    df_liberal['cleaned_text'] = df_liberal['cleaned_text'].apply(collapse_list_to_string)

    df_neutral['cleaned_text'] = df_neutral['cleaned_text'].apply(remove_apostrophes)
    df_labor['cleaned_text'] = df_labor['cleaned_text'].apply(remove_apostrophes)
    df_liberal['cleaned_text'] = df_liberal['cleaned_text'].apply(remove_apostrophes)


# ## Sentiment Scores

# In[11]:


def get_sentiment(text:str,desired_type:str='pos'):
    # Get sentiment from text
    sentiment_score = SentimentIntensityAnalyzer().polarity_scores(text)
    return sentiment_score[desired_type]

# Get Sentiment scores
def get_sentiment_scores(df,data_column):
    df[ '{} Positive Sentiment Score'.format(data_column)] = df[data_column].astype(str).apply(lambda x: get_sentiment(x,'pos'))
    df['{} Negative Sentiment Score'.format(data_column)] = df[data_column].astype(str).apply(lambda x: get_sentiment(x,'neg'))
    df['{} Neutral Sentiment Score'.format(data_column)] = df[data_column].astype(str).apply(lambda x: get_sentiment(x,'neu'))
    df['{} Compound Sentiment Score'.format(data_column)] = df[data_column].astype(str).apply(lambda x: get_sentiment(x,'compound'))
    return df


# In[12]:


#nltk.download('wordnet')
def lemmatize_text(text):
    w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
    lemmatizer = nltk.stem.WordNetLemmatizer()
    return [lemmatizer.lemmatize(w) for w in w_tokenizer.tokenize(text)]

def apply_lemm(df_neutral,df_liberal,df_labor):
    df_neutral['clean_lemmatized'] = df_neutral['cleaned_text'].astype(str).apply(lemmatize_text)
    df_labor['clean_lemmatized'] = df_labor['cleaned_text'].astype(str).apply(lemmatize_text)
    df_liberal['clean_lemmatized'] = df_liberal['cleaned_text'].astype(str).apply(lemmatize_text)

    df_neutral['clean_lemmatized'] = df_neutral['clean_lemmatized'].apply(collapse_list_to_string)
    df_liberal['clean_lemmatized'] = df_liberal['clean_lemmatized'].apply(collapse_list_to_string)
    df_labor['clean_lemmatized'] = df_labor['clean_lemmatized'].apply(collapse_list_to_string)


# apply_lemm()
# df_neutral = get_sentiment_scores(df_neutral,'clean_lemmatized')
# df_liberal = get_sentiment_scores(df_liberal,'clean_lemmatized')
# df_labor = get_sentiment_scores(df_labor,'clean_lemmatized')

# In[13]:


def temp(df_neutral,df_liberal,df_labor,result):
    result['temp']=1
    df_labor['temp']=1
    df_liberal['temp']=1
    df_neutral['temp']=1
    df_labor = pd.merge(result,df_labor,on='temp')
    df_liberal = pd.merge(result,df_liberal,on='temp')
    df_neutral = pd.merge(result,df_neutral,on='temp')


# ## Joining on the basis of coordinates and filtering under 20 km

# In[14]:


def add_info(df_neutral,df_liberal,df_labor):
    # https://stackoverflow.com/questions/43143176/for-loop-filter-on-pandas-dataframe-not-working
    dfs = [df_neutral,df_liberal,df_labor]
    cols = ['longitude_x','latitude_x']
    for i in range(len(dfs)):
        try:
            dfs[i]['longitude_x'] = dfs[i]['Coordinates'].apply(str).str.strip('[]').str.split('-', expand=True)[0]
            dfs[i]['latitude_x'] = '-'+dfs[i]['Coordinates'].apply(str).str.strip('[]').str.split('-', expand=True)[1]
            dfs[i][cols] = dfs[i][cols].apply(pd.to_numeric, errors='coerce')
            dfs[i]['distance'] = haversine_np(dfs[i]['longitude_x'],dfs[i]['latitude_x'],
                                          dfs[i]['Longitude'],dfs[i]['Latitude'])
            dfs[i] = dfs[i][dfs[i].distance < 20]
            dfs[i] = dfs[i].sort_values('distance').drop_duplicates('cleaned_text').reset_index(drop=True)
        except Exception:
            pass
    # try
    
    


# In[15]:


def haversine_np(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    All args must be of equal length.    

    """
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2

    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c
    return km


# In[16]:


def finalise(df_neutral,df_liberal,df_labor):
    cols = ['longitude_x','latitude_x']

    df_neutral[cols] = df_neutral[cols].apply(pd.to_numeric, errors='coerce')
    df_labor[cols] = df_labor[cols].apply(pd.to_numeric, errors='coerce')
    df_liberal[cols] = df_liberal[cols].apply(pd.to_numeric, errors='coerce')

    df_neutral['distance'] = haversine_np(df_neutral['longitude_x'],df_neutral['latitude_x'],
                                          df_neutral['Longitude'],df_neutral['Latitude'])
    df_labor['distance'] = haversine_np(df_labor['longitude_x'],df_labor['latitude_x'],
                                          df_labor['Longitude'],df_labor['Latitude'])
    df_liberal['distance'] = haversine_np(df_liberal['longitude_x'],df_liberal['latitude_x'],
                                          df_liberal['Longitude'],df_liberal['Latitude'])
    
    df_neutral = df_neutral[df_neutral.distance < 20]
    df_labor = df_labor[df_labor.distance < 20]
    df_liberal = df_liberal[df_liberal.distance < 20]
    
    df_neutral = df_neutral.sort_values('distance').drop_duplicates('cleaned_text').reset_index(drop=True)
    df_labor = df_labor.sort_values('distance').drop_duplicates('cleaned_text').reset_index(drop=True)
    df_liberal = df_liberal.sort_values('distance').drop_duplicates('cleaned_text').reset_index(drop=True)
    


# df_neutral = df_neutral[df_neutral.distance < 20]
# df_labor = df_labor[df_labor.distance < 20]
# df_liberal = df_liberal[df_liberal.distance < 20]

# df_neutral = df_neutral.sort_values('distance').drop_duplicates('cleaned_text').reset_index(drop=True)
# df_labor = df_labor.sort_values('distance').drop_duplicates('cleaned_text').reset_index(drop=True)
# df_liberal = df_liberal.sort_values('distance').drop_duplicates('cleaned_text').reset_index(drop=True)

# df_neutral.to_json("neutral.json",orient='records')
# df_labor.to_json("labor.json",orient='records')
# df_liberal.to_json("liberal.json",orient='records')
