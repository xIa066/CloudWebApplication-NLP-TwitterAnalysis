


from flask import Flask
import couchdb
from connection_details import *


# intialisation
app = Flask(__name__)


# connect to couchdb server
def connect_server():
    try:
        server = couchdb.Server("http://%s:%s@%s:%s/" % (USERNAME,PASSWORD,NODE,PORT))
    except:
        print("please connect to the VPN ")
    return server

# identify required database
def get_db(db_name,server):
    if db_name in server:
        db = server[db_name]
        return db
    else:
        print('Database not found!')

# configuration
server=connect_server()
db=get_db(DATABASE_HISTORY,server)
        
# retrive views from db
def get_view(view_name,db,toGroup):
    outfile = dict()
    for tweet in db.view(f'keyViews/{view_name}',group=toGroup):
        outfile[str(tweet.key)]=tweet.value
    return outfile

# route to compoundScore view, return a dictionary
@app.route('/compoundScore',methods = ['GET'])
def getCompoundScore():
    try:
        data = get_view('compoundScore', db, True)
    except:
        server = connect_server()
        get_db(DATABASE_HISTORY, server)
        data = get_view('compoundScore', db, True)
    return data


@app.route('/neutralScore',methods = ['GET'])
def getNeutralScore():
    try:
        data = get_view('neutralScore',db,True)
    except:
        server = connect_server()
        get_db(DATABASE_HISTORY, server)
        data = get_view('neutralScore',db,True)
    return data

@app.route('/positiveScore',methods = ['GET'])
def getPositiveScore():
    try:
        data = get_view('positiveScore',db,True)
    except:
        server = connect_server()
        get_db(DATABASE_HISTORY, server)
        data = get_view('positiveScore',db,True)
    return data


@app.route('/negativeScore',methods = ['GET'])
def getNegativeScore():
    try:
        data = get_view('negativeScore',db,True)
    except:
        server = connect_server()
        get_db(DATABASE_HISTORY, server)
        data = get_view('negativeScore',db,True)
    return data

@app.route('/location',methods=['GET'])
def getLocation():
    try:
        data = get_view('location',db,False)
    except:
        server = connect_server()
        get_db(DATABASE_HISTORY, server)
        data = get_view('location',db,False)
    return data

@app.route('/textdoc',methods=['GET'])
def getLocationWords():
    try:
        data = get_view('textdoc',db,False)
    except:
        server = connect_server()
        get_db(DATABASE_HISTORY, server)
        data = get_view('location',db,False)
    return data


if __name__ == '__main__':
    #app.run(debug=True)                       # debug mode
    app.run(host='0.0.0.0', port=8000)        # deployment mode
    #app.run()

