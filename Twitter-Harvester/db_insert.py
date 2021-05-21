import couchdb
from connection_details import *
import glob
import os
from glob import glob
import json
#warnings.filterwarnings('ignore')
import importlib
from time2relax import CouchDB
from twitter import *
from aurin import *
from joiningAurinTwitter import *
from main import*

def connect_server():
    try:
        server = CouchDB('http://{}:{}@{}:{}/{}'.format(USERNAME, PASSWORD, HOST, PORT, database_history))
        print('sucessful')
    except:
        print("please connect to the VPN ")
    return server

def insert_data(data):
    db = connect_server()
    for tweet in data:
        tweet['_id'] = str(tweet['id'])
        tweet['tweetText'] = tweet['tweetText']
        tweet['tweetCreated'] = tweet['tweetCreated']
        tweet['userLocation'] = tweet['TweetPlace']
        tweet['Coordinates'] = tweet['Coordinates']
        tweet["clean_lemmatized Positive Sentiment Score"] = float(tweet["clean_lemmatized Positive Sentiment Score"])
        tweet["clean_lemmatized Negative Sentiment Score"] = float(tweet["clean_lemmatized Negative Sentiment Score"])
        tweet["clean_lemmatized Neutral Sentiment Score"] = float(tweet["clean_lemmatized Neutral Sentiment Score"])
        tweet["clean_lemmatized Compound Sentiment Score"] = float(tweet["clean_lemmatized Compound Sentiment Score"])

    db.bulk_docs(data)


