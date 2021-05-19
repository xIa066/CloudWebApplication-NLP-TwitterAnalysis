import couchdb
from flask import Flask, render_template, request, session
import json

app = Flask(__name__)
app.secret_key = 'random string'

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

#remove a particular database
def remove_db(db_name,server):
    if db_name in server:
        del server[db_name]
        return f"Database {db_name} has been deleted sucessfully."
    else:
        print('Database not found!')
        
server=connect_server('admin','admin')
db=get_db('data',server)

# retrive views from db
def get_view(view_name,db,to_group):
    outfile = {}
    for tweet in db.view(f'keyViews/{view_name}',group=to_group):
        # print(tweet.key,tweet.value)
        outfile[str(tweet.key)]=tweet.value
    return outfile

# home page
@app.route('/')
def index():
    return render_template('main.html')

# map page
@app.route('/map')
def display_map():
    return render_template('map.html')

# for retrieving map data
@app.route('/map_data/<map_type>')
def fetch_map_data(map_type):
    outfile = {}
    if map_type == 'loc':
        outfile = get_view('location', db, False)
    elif map_type == 'sentiment':
        pass
    return outfile

# graph page
@app.route('/graph')
def graph():
        return render_template('graph.html')

# for retrieving graph data
@app.route('/graph_data/<view>')
def fetch_graph_data(view):
    if view != "none":
        data = get_view(view, db, True)
        # graph_html = create_graph(view)
        return data
    else:
        return "none"

# word cloud page
@app.route('/word_cloud')
def word_cloud():
    return render_template('word_cloud.html')

if __name__ == "__main__":
    app.run()