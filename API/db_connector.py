import couchdb
from connection_details import *
import os
import json
def create_connection():
    couch = couchdb.Server('http://{}:{}@{}:{}/'.format(USERNAME,PASSWORD,HOST,PORT))
    return couch

from time2relax import CouchDB
db = CouchDB('http://{}:{}@{}:{}/{}'.format(USERNAME,PASSWORD,HOST,PORT,'test'))



def create_database(couch,database_name):
    try:
        db = couch.create(database_name)

    except:
        db=couch[database_name]
    return db


with open(os.path.join("./data", 'tinyTwitter.json')) as f:
    data=json.load(f)
db.bulk_docs(data['rows'])

# server=create_connection()
# db=create_database(server,'test')
# db.save(data['rows'][2]['doc'],batch='ok')
# print(data['rows'][0]['doc'])
