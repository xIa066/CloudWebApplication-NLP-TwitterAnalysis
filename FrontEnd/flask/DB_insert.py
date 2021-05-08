#!/usr/bin/env python
# coding: utf-8

# In[13]:


import couchdb
from connection_details import *
import ijson
import json
import importlib
from time2relax import CouchDB

def create_connection():
    couch = couchdb.Server('http://{}:{}@{}:{}/'.format(USERNAME,PASSWORD,HOST,PORT))
    return couch

def create_database(couch,database_name):
    try:
        db = couch.create(database_name)

    except:
        db=couch[database_name]
    return db

# add 'support' field to each item(i.e tweet) in the json file(converted to dict) based on the json file it belongs to 
# (e.g. tweets in labor.json will have support = 'labor')
def load_data(support,data):
    db = CouchDB('http://{}:{}@{}:{}/{}'.format(USERNAME,PASSWORD,HOST,PORT,'data1'))
    for tweet in data:
        if support == 'neutral':
            tweet['support'] = 'neutral'
        elif support == 'labor':
            tweet['support'] = 'labor'
        elif support == 'liberal':
            tweet['support'] = 'liberal'
    # push processed dictonary to the database in bulk
    db.bulk_docs(data) 

# called by App.py 
def insert_DB(support,file):
    # convert resulted json file to dictionary
    data = json.loads(file)
    #https://www.geeksforgeeks.org/append-to-json-file-using-python/
    load_data(support,data)


# In[ ]:




