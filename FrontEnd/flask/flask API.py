#!/usr/bin/env python
# coding: utf-8

# In[7]:


from flask import Flask
import couchdb


# In[8]:


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
def get_view(view_name,db,toGroup):
    outfile = dict()
    for tweet in db.view(f'keyViews/{view_name}',group=toGroup):
        outfile[str(tweet.key)]=tweet.value
    return outfile

# route to compoundScore view, return a dictionary
@app.route('/compoundScore',methods = ['GET'])
def getCompoundScore():
    return get_view('compoundScore',db,True)

@app.route('/neutralScore',methods = ['GET'])
def getNeutralScore():
    return get_view('neutralScore',db,True)

@app.route('/positiveScore',methods = ['GET'])
def getPositiveScore():
    return get_view('positiveScore',db,True)

@app.route('/negativeScore',methods = ['GET'])
def getNegativeScore():
    return get_view('negativeScore',db,True)

@app.route('/location',methods=['GET'])
def getLocation():
    return get_view('location',db,False)


# In[9]:


# configuration
server=connect_server('admin','admin')
db=get_db('data1',server)


# In[10]:


if __name__ == '__main__':
    #app.run(debug=True)                       # debug mode
    # app.run(host='0.0.0.0', port=5000)        # deployment mode
    app.run()

