#!/usr/bin/env python
# coding: utf-8

# In[13]:


import couchdb


# In[14]:


# connect to couchdb server
def connect_server(user,password):
    server = couchdb.Server("http://%s:%s@172.26.131.32:5984/" % (user,password))


# In[15]:


# identify required database
def find_db(db_name):
    if db_name in server:
        db = server[db_name]
    else:
        print('Database not found!')


# In[16]:


# retrive views from db
def get_view(view_name):
    for tweet in db.view(f'keyViews/{view_name}',group=True):
        print(tweet.key,tweet.value)


# In[17]:


# test
connect_server('admin','admin')
find_db('data1')
get_view('compoundScore')

