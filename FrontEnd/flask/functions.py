import pandas as pd
import ast
import json
import re
import requests
from plotly.io import to_html
import plotly.express as px
from wordcloud import WordCloud

URL = 'http://172.26.134.11:8000/'
cities = set(['melbourne', 'sydney', 'brisbane', 'canberra', 'perth', 'adelaide'])

####### graph drawing functions
# function for filtering noisy keys with keywords
def filter_key(data, city, year):
    count = 0
    total = 0
    for key,value in data.items():
        keyList = ast.literal_eval(key)
        # try if item has location key, otherwise skip
        try:
            # specify city and year
            if keyList[0]['location'].lower().find(city) != -1 and keyList[0]['date'] == year:
                count += value['count']
                total += value['sum']

        except KeyError:
            continue
    # returns a tuple of city and average score
    count = 1 if count < 1 else count # adjust if there are no tweets for a yr

    return (city,year,total/count)

# extract needed cities from raw data
def process_graph_data(view):
    get_data = requests.get(URL + view)
    raw_data = json.loads(get_data.text)

    years = list(range(2010,2020))

    processed_data = pd.DataFrame(columns = ['Year', 'City', 'Score'])
    
    for city in cities:
        for year in years:
            _, _, avg = filter_key(raw_data, city, year)
            processed_data = processed_data.append({'Year': year, 
                                                    'City': city.title(), 
                                                    'Score': avg},
                                                    ignore_index = True)

    return processed_data

# return the graph html
def draw_graph(view):
    processed_data = process_graph_data(view)

    view = view.replace('Score', '').title()

    fig = px.line(processed_data,
                    x = "Year",
                    y = "Score",
                    facet_col = "City",
                    color = "City",
                    facet_col_wrap = 2,
                    title = view + " Sentiment Score by city over time",
                    height = 1000)
    fig.update_yaxes(title_text = "Average Sentiment Score")

    fig_html = to_html(fig,
                        include_plotlyjs = False,
                        full_html = False)
    return fig_html

####### map drawing functions
# converts json with id and coords to geojson for tweet locs
def location_geojson():
    get_data = requests.get(URL + 'location')
    raw_data = json.loads(get_data.text)

    data = {"type": "FeatureCollection", "features" :[]}

    for k, v in raw_data.items():
        # need to add properties.id and geometry.coordinates
        try:
            coords = eval(v)
        except:
            coords = v

        if coords[0] < 113.33 or coords[0] > 153.57:
            continue
        if coords[1] < -43.63 or coords[1] > -10.67:
            continue

        temp_feature = {"type": "Feature", 
                        "geometry": {
                            "type": "Point"
                        }}

        temp_feature['properties'] = {'id': k}
        temp_feature['geometry']['coordinates'] = [coords[0], coords[1]]
        data['features'].append(temp_feature)

    return data

# converts json to geojson for aurin data
def vote_geojson():
    get_data = requests.get(URL + 'aurin')
    raw_data = json.loads(get_data.text)

    data = {"type": "FeatureCollection", "features":[]}

    for k, v in raw_data.items():
        temp_feature = {"type": "Feature", 
                        "geometry": {
                            "type": "Point"
                        }}

        coords = [v['lng'], v['lat']]

        temp_feature['properties'] = {'id': k, 'ALP': v['ALP'], 'LIB': v['LIB'], 'GRN': v['GRN']}
        temp_feature['geometry']['coordinates'] = coords
        data['features'].append(temp_feature)

    return data


###### wordcloud functions
def fetch_tweets(category):
    if category == "none":
        return "none"

    get_data = requests.get(URL + 'textdoc')
    raw_data = json.loads(get_data.text)

    if category == "all":
        data = pd.DataFrame.from_dict(raw_data, orient = 'index')
    elif category == "city":
        temp_data = []
        for k, v in raw_data.items():
            if any(city in v['location:'].lower() for city in cities):
                temp_data.append(v)
        data = pd.DataFrame(temp_data)

    data = data.rename(columns = {'location:': 'location'})
    return data

# draw graph for wordclouds
def draw_wordcloud(category):
    data = fetch_tweets(category)

    if category == 'all':
        wordcloud = WordCloud(width = 1600, height = 800)\
                    .generate(' '.join(data['text'].astype(str)))

        wordcloud.to_file('img/all.png')
    elif category == 'city':
        for city in cities:
            temp_data = data[data['location'].str.lower().str.contains(city)]
            wordcloud = WordCloud(width = 1600, height = 800)\
                        .generate(' '.join(temp_data['text'].astype(str)))
            wordcloud.to_file('static/images/{city}.png'.format(city = city))
    
    return category

if __name__ == '__main__':
    data = vote_geojson()