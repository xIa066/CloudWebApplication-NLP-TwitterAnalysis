#!/usr/bin/env python
# coding: utf-8

# In[42]:


from flask import Flask
import couchdb


# In[43]:


# intialisation
app = Flask(__name__)

# connect to couchdb server
def connect_server(user,password):
    server = couchdb.Server("http://%s:%s@172.26.131.32:5984/" % (user,password))
    return server

# identify required database
def get_db(db_name,server):
    if db_name in server:
        db = server[db_name]
        return db
    else:
        print('Database not found!')
        
# retrive views from db
def get_view(view_name,db):
    outfile = dict()
    for tweet in db.view(f'keyViews/{view_name}',group=True):
        outfile[str(tweet.key)]=tweet.value
    return outfile

# route to compoundScore view, return a dictionary
@app.route('/compoundScore',methods = ['GET'])
def getCompoundScore():
    return get_view('compoundScore',db)

@app.route('/neutralScore',methods = ['GET'])
def getNeutralScore():
    return get_view('neutralScore',db)

@app.route('/positiveScore',methods = ['GET'])
def getPositiveScore():
    return get_view('positiveScore',db)

@app.route('/negativeScore',methods = ['GET'])
def getNegativeScore():
    return get_view('negativeScore',db)


# In[44]:


# configuration
server=connect_server('admin','admin')
db=get_db('data1',server)


# In[45]:


if __name__ == '__main__':
    #app.run(debug=True)                       # debug mode
    # app.run(host='0.0.0.0', port=5000)        # deployment mode
    app.run()

