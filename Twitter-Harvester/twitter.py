import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
import warnings
warnings.filterwarnings('ignore')
import tweepy
import sys
import nltk
from nltk.corpus import stopwords
import typing
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from aurin import *
from twitter_credentials import *
nltk.download()
#Twitter Account Setup
def api_connect():
    consumer_key = API_KEY
    consumer_secret_key = API_SECRET_KEY
    access_token = ACCESS_TOKEN
    access_token_secret = ACCESS_TOKEN_SECRET
    con_bol=False
    while(con_bol==False):
        try:
            authenticate = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
            authenticate.set_access_token(access_token, access_token_secret)
            api = tweepy.API(authenticate, wait_on_rate_limit=True)
            places = api.geo_search(query="Australia", granularity="country")
            place_id = places[0].id
            conn = 'Authentication OK'
            #print("successful")
            con_bol=True
        except:
            api = None
            place_id = None
            conn = "Error during authentication"
            con_bol=False
    return api, conn, place_id

#Tweet Extraction Function
def toDataFrame(tweets,hashtag):

    DataSet = pd.DataFrame()

    DataSet['tweetText'] = [tweet.text for tweet in tweets]
    DataSet['tweetCreated'] = [tweet.created_at for tweet in tweets]
    DataSet['userLocation'] = [tweet.user.location for tweet in tweets]
    DataSet['id'] = [tweet.id for tweet in tweets]
    DataSet['Coordinates'] = [np.average(tweet._json['place']['bounding_box']['coordinates'][0], axis=0) for tweet in tweets]
    tweets_place= []
    for tweet in tweets:
        if tweet.place:
            tweets_place.append(tweet.place.full_name)
        else:
            tweets_place.append('null')
    DataSet['TweetPlace'] = [i for i in tweets_place]
    return DataSet

##Reading hashtag file and dividing into 3 datasets namely-Neutral, Liberal & Labor
df = pd.read_csv("./hashtags/hashtags.csv")
NEUTRAL_HASHTAGS = df['NEUTRAL_HASHTAGS']
LABOR_HASHTAGS = df['LABOR_HASHTAGS']
LIBERAL_HASHTAGS = df['LIBERAL_HASHTAGS']

def fun_neu_fetch(api,place_id):
    list_hashtags =NEUTRAL_HASHTAGS.dropna()
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
    #df_neutral.to_csv("./tweets/neutral_tweet_extracted.csv",index=False)
    return df_neutral

def fun_lab_fetch(api, place_id):
    list_hashtags = LABOR_HASHTAGS.dropna()
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
    #df_labor.to_csv("./tweets/labor_tweet_extracted.csv",index=False)
    return df_labor

def fun_libl_fetch(api, place_id):
    list_hashtags = LIBERAL_HASHTAGS.dropna()
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
    #df_liberal.to_csv("./tweets/liberal_tweet_extracted.csv",index=False)
    return df_liberal

#Text Cleaning Function
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

#Cleaning Twitter Text Data
stopcorpus = stopwords.words('english')

#Sentiment Scores
sid_analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text:str, analyser,desired_type:str='pos'):
    # Get sentiment from text
    sentiment_score = analyser.polarity_scores(text)
    return sentiment_score[desired_type]

# Get Sentiment scores
#row by row analysis using lambda function
def get_sentiment_scores(df,data_column):
    df[ '{} Positive Sentiment Score'.format(data_column)] = df[data_column].astype(str).apply(lambda x: get_sentiment(x,sid_analyzer,'pos'))
    df['{} Negative Sentiment Score'.format(data_column)] = df[data_column].astype(str).apply(lambda x: get_sentiment(x,sid_analyzer,'neg'))
    df['{} Neutral Sentiment Score'.format(data_column)] = df[data_column].astype(str).apply(lambda x: get_sentiment(x,sid_analyzer,'neu'))
    df['{} Compound Sentiment Score'.format(data_column)] = df[data_column].astype(str).apply(lambda x: get_sentiment(x,sid_analyzer,'compound'))
    return df
w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
lemmatizer = nltk.stem.WordNetLemmatizer()

def lemmatize_text(text):
    return [lemmatizer.lemmatize(w) for w in w_tokenizer.tokenize(text)]

def clean_tweets(df_tobecleaned):
    df_tobecleaned['cleaned_text'] = df_tobecleaned['tweetText'].astype(str).apply(remove_links)
    df_tobecleaned['cleaned_text'] = df_tobecleaned['cleaned_text'].astype(str).apply(style_text)
    df_tobecleaned['cleaned_text'] = df_tobecleaned['cleaned_text'].astype(str).apply(lambda x: remove_words(x.split(),stopcorpus))
    df_tobecleaned['cleaned_text'] = df_tobecleaned['cleaned_text'].apply(collapse_list_to_string)
    df_tobecleaned['cleaned_text'] = df_tobecleaned['cleaned_text'].apply(remove_apostrophes)
    df_tobecleaned['clean_lemmatized'] = df_tobecleaned['cleaned_text'].astype(str).apply(lemmatize_text)
    df_tobecleaned = get_sentiment_scores(df_tobecleaned, 'clean_lemmatized')
    df_tobecleaned['clean_lemmatized'] = df_tobecleaned['clean_lemmatized'].apply(collapse_list_to_string)
    return df_tobecleaned


