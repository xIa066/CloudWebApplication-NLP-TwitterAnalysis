from flask import Flask, render_template
from functions import draw_graph, location_geojson, vote_geojson, draw_wordcloud
import json

app = Flask(__name__)
app.secret_key = 'random string'

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
    data = {}
    if map_type == "location":
        # raw_data = get_view('location', db, False)
        data = location_geojson()
    elif map_type.contains('vote'):
        data = vote_geojson()
    
    return data

# graph page
@app.route('/graph')
def graph():
        return render_template('graph.html')

# for retrieving graph data
@app.route('/graph_data/<view>')
def fetch_graph_html(view):
    if view != "none":
        # raw_data = get_view(view, db, True)
        fig_html = draw_graph(view)

        return fig_html
    else:
        return "none"

# word cloud page
@app.route('/word_cloud')
def word_cloud():
    return render_template('word_cloud.html')

# drawing word clouds
@app.route('/word_cloud_img/<category>')
def generate_word_cloud(category):
    response = draw_wordcloud(category)
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
    # app.run()
