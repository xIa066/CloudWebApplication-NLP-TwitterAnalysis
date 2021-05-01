import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly

import nltk
from nltk.corpus import stopwords
import typing
import re

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

df_neutral_1 = pd.read_csv("./static/neutral_tweet_extracted.csv")
df_labor_1 = pd.read_csv("./static/labor_tweet_extracted.csv")
df_liberal_1 = pd.read_csv("./static/liberal_tweet_extracted.csv")


def remove_links(text):
    # Remove any hyperlinks that may be in the text starting with http
    import re
    return re.sub(r"http\S+", "", text)


def style_text(text: str):
    # Convert to lowercase
    return text.lower()


def remove_words(text_data: str, list_of_words_to_remove: typing.List):
    # Remove all words as specified in a custom list of words
    return [item for item in text_data if item not in list_of_words_to_remove]


def collapse_list_to_string(string_list):
    # This is to join back together the text data into a single string
    return ' '.join(string_list)


def remove_apostrophes(text):
    # Remove any apostrophes as these are irrelavent in our word cloud
    text = text.replace("'", "")
    text = text.replace('"', "")
    text = text.replace('`', "")
    text = re.sub(r'@\S+', "", text)
    text = re.sub(r'#\S+', "", text)
    return text


sid_analyzer = SentimentIntensityAnalyzer()


def get_sentiment(text: str, analyser, desired_type: str = 'pos'):
    # Get sentiment from text
    sentiment_score = analyser.polarity_scores(text)
    return sentiment_score[desired_type]

def haversine_np(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    All args must be of equal length.

    """
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2

    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c
    return km


# Get Sentiment scores
def get_sentiment_scores(df, data_column):
    df['{} Positive Sentiment Score'.format(data_column)] = df[data_column].astype(str).apply(
        lambda x: get_sentiment(x, sid_analyzer, 'pos'))
    df['{} Negative Sentiment Score'.format(data_column)] = df[data_column].astype(str).apply(
        lambda x: get_sentiment(x, sid_analyzer, 'neg'))
    df['{} Neutral Sentiment Score'.format(data_column)] = df[data_column].astype(str).apply(
        lambda x: get_sentiment(x, sid_analyzer, 'neu'))
    df['{} Compound Sentiment Score'.format(data_column)] = df[data_column].astype(str).apply(
        lambda x: get_sentiment(x, sid_analyzer, 'compound'))
    return df

w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
lemmatizer = nltk.stem.WordNetLemmatizer()

def lemmatize_text(text):
    return [lemmatizer.lemmatize(w) for w in w_tokenizer.tokenize(text)]

def plot_wordcloud(series,output_filename='wordcloud'):
    from wordcloud import WordCloud
    wordcloud = WordCloud(width=1600, height=800).generate(' '.join(series.astype(str)))
    wordcloud.to_file('./static/'+output_filename + '.png')

def plot_wordcloud_top_n(df,number_of_reviews,score_column,data_column,output_filename):
    sliced_df = df.nlargest(number_of_reviews,score_column)
    plot_wordcloud(sliced_df[data_column],output_filename)

def df_clean(df_local,filter_disatnce):
    df_local = df_local[['fraser_annings_conservative_national_party_ordinary_votes',
                         ' labor_ordinary_votes', ' the_greens_ordinary_votes', ' liberal_ordinary_votes',
                         ' united_australia_party_ordinary_votes', ' latitude', ' longitude',
                         ' division_id', ' division_name', ' polling_place_name', ' state']]

    vote_result_division_wise = df_local.groupby(' division_name')[
        ['fraser_annings_conservative_national_party_ordinary_votes',
         ' labor_ordinary_votes', ' the_greens_ordinary_votes',
         ' liberal_ordinary_votes', ' united_australia_party_ordinary_votes']].sum()
    lat_lon = df_local.groupby(' division_name')[[' latitude', ' longitude']].agg(np.median)
    result = lat_lon.join(vote_result_division_wise, how='outer')
    result = result.loc[
             ['Brisbane', 'Canberra', 'Adelaide', 'Melbourne', 'Newcastle', 'Perth', 'Sydney', 'North Sydney'], :]
    result = result.reset_index()
    result.columns = ['Division Name', 'Latitude', 'Longitude',
                      'Conservative National Party',
                      'Labor Party', 'Greens Party',
                      'Liberal Party', 'United Australia Party']

    stopcorpus = stopwords.words('english')

    df_neutral_1['cleaned_text'] = df_neutral_1['tweetText'].astype(str).apply(remove_links)
    df_labor_1['cleaned_text'] = df_labor_1['tweetText'].astype(str).apply(remove_links)
    df_liberal_1['cleaned_text'] = df_liberal_1['tweetText'].astype(str).apply(remove_links)

    df_neutral_1['cleaned_text'] = df_neutral_1['cleaned_text'].astype(str).apply(style_text)
    df_labor_1['cleaned_text'] = df_labor_1['cleaned_text'].astype(str).apply(style_text)
    df_liberal_1['cleaned_text'] = df_liberal_1['cleaned_text'].astype(str).apply(style_text)

    df_neutral_1['cleaned_text'] = df_neutral_1['cleaned_text'].astype(str).apply(
        lambda x: remove_words(x.split(), stopcorpus))
    df_labor_1['cleaned_text'] = df_labor_1['cleaned_text'].astype(str).apply(lambda x: remove_words(x.split(), stopcorpus))
    df_liberal_1['cleaned_text'] = df_liberal_1['cleaned_text'].astype(str).apply(
        lambda x: remove_words(x.split(), stopcorpus))

    df_neutral_1['cleaned_text'] = df_neutral_1['cleaned_text'].apply(collapse_list_to_string)
    df_labor_1['cleaned_text'] = df_labor_1['cleaned_text'].apply(collapse_list_to_string)
    df_liberal_1['cleaned_text'] = df_liberal_1['cleaned_text'].apply(collapse_list_to_string)

    df_neutral_1['cleaned_text'] = df_neutral_1['cleaned_text'].apply(remove_apostrophes)
    df_labor_1['cleaned_text'] = df_labor_1['cleaned_text'].apply(remove_apostrophes)
    df_liberal_1['cleaned_text'] = df_liberal_1['cleaned_text'].apply(remove_apostrophes)

    df_neutral_1['clean_lemmatized'] = df_neutral_1['cleaned_text'].astype(str).apply(lemmatize_text)
    df_labor_1['clean_lemmatized'] = df_labor_1['cleaned_text'].astype(str).apply(lemmatize_text)
    df_liberal_1['clean_lemmatized'] = df_liberal_1['cleaned_text'].astype(str).apply(lemmatize_text)

    df_neutral_1['clean_lemmatized'] = df_neutral_1['clean_lemmatized'].apply(collapse_list_to_string)
    df_liberal_1['clean_lemmatized'] = df_liberal_1['clean_lemmatized'].apply(collapse_list_to_string)
    df_labor_1['clean_lemmatized'] = df_labor_1['clean_lemmatized'].apply(collapse_list_to_string)

    df_neutral = get_sentiment_scores(df_neutral_1, 'clean_lemmatized')
    df_liberal = get_sentiment_scores(df_liberal_1, 'clean_lemmatized')
    df_labor = get_sentiment_scores(df_labor_1, 'clean_lemmatized')
    result.to_csv("./static/local_csv_updated.csv", index=False)

    result['temp'] = 1
    df_labor['temp'] = 1
    df_liberal['temp'] = 1
    df_neutral['temp'] = 1
    df_labor = pd.merge(result, df_labor, on='temp')
    df_liberal = pd.merge(result, df_liberal, on='temp')
    df_neutral = pd.merge(result, df_neutral, on='temp')

    df_neutral['longitude_x'] = df_neutral['Coordinates'].apply(str).str.strip('[]').str.split('-', expand=True)[0]
    df_neutral['latitude_x'] = '-' + df_neutral['Coordinates'].apply(str).str.strip('[]').str.split('-', expand=True)[1]

    df_labor['longitude_x'] = df_labor['Coordinates'].apply(str).str.strip('[]').str.split('-', expand=True)[0]
    df_labor['latitude_x'] = '-' + df_labor['Coordinates'].apply(str).str.strip('[]').str.split('-', expand=True)[1]

    df_liberal['longitude_x'] = df_liberal['Coordinates'].apply(str).str.strip('[]').str.split('-', expand=True)[0]
    df_liberal['latitude_x'] = '-' + df_liberal['Coordinates'].apply(str).str.strip('[]').str.split('-', expand=True)[1]

    cols = ['longitude_x', 'latitude_x']

    df_neutral[cols] = df_neutral[cols].apply(pd.to_numeric, errors='coerce')
    df_labor[cols] = df_labor[cols].apply(pd.to_numeric, errors='coerce')
    df_liberal[cols] = df_liberal[cols].apply(pd.to_numeric, errors='coerce')

    df_neutral['distance'] = haversine_np(df_neutral['longitude_x'], df_neutral['latitude_x'],
                                          df_neutral['Longitude'], df_neutral['Latitude'])
    df_labor['distance'] = haversine_np(df_labor['longitude_x'], df_labor['latitude_x'],
                                        df_labor['Longitude'], df_labor['Latitude'])
    df_liberal['distance'] = haversine_np(df_liberal['longitude_x'], df_liberal['latitude_x'],
                                          df_liberal['Longitude'], df_liberal['Latitude'])

    df_neutral = df_neutral[df_neutral.distance < filter_disatnce]
    df_labor = df_labor[df_labor.distance < filter_disatnce]
    df_liberal = df_liberal[df_liberal.distance < filter_disatnce]

    df_neutral = df_neutral.sort_values('distance').drop_duplicates('cleaned_text').reset_index(drop=True)
    df_labor = df_labor.sort_values('distance').drop_duplicates('cleaned_text').reset_index(drop=True)
    df_liberal = df_liberal.sort_values('distance').drop_duplicates('cleaned_text').reset_index(drop=True)

    plot_wordcloud(df_neutral['clean_lemmatized'], 'overall-wordcloud-df_neutral')
    plot_wordcloud_top_n(df_neutral, 500, 'clean_lemmatized Positive Sentiment Score', 'clean_lemmatized',
                         'positive-wordcloud-df_neutral')
    plot_wordcloud_top_n(df_neutral, 500, 'clean_lemmatized Negative Sentiment Score', 'clean_lemmatized',
                         'negative-wordcloud-df_neutral')
    plot_wordcloud_top_n(df_neutral, 500, 'clean_lemmatized Neutral Sentiment Score', 'clean_lemmatized',
                         'neutral-wordcloud-df_neutral')

    plot_wordcloud(df_labor['clean_lemmatized'], 'overall-wordcloud-df_labor')
    plot_wordcloud_top_n(df_labor, 500, 'clean_lemmatized Negative Sentiment Score', 'clean_lemmatized',
                         'positive-wordcloud-df_labor')
    plot_wordcloud_top_n(df_labor, 500, 'clean_lemmatized Negative Sentiment Score', 'clean_lemmatized',
                         'negative-wordcloud-df_labor')
    plot_wordcloud_top_n(df_labor, 500, 'clean_lemmatized Negative Sentiment Score', 'clean_lemmatized',
                         'neutral-wordcloud-df_labor')
    plot_wordcloud(df_liberal['clean_lemmatized'], 'overall-wordcloud-df_liberal')
    plot_wordcloud_top_n(df_liberal, 500, 'clean_lemmatized Negative Sentiment Score', 'clean_lemmatized',
                         'positive-wordcloud-df_liberal')
    plot_wordcloud_top_n(df_liberal, 500, 'clean_lemmatized Negative Sentiment Score', 'clean_lemmatized',
                         'negative-wordcloud-df_liberal')
    plot_wordcloud_top_n(df_liberal, 500, 'clean_lemmatized Neutral Sentiment Score', 'clean_lemmatized',
                         'neutral-wordcloud-df_liberal')

    result2 = result.copy()
    a = result2.reset_index()[['Division Name', 'Conservative National Party', 'Latitude', 'Longitude']]
    a.columns = ['Division Name', 'Votes', 'Latitude', 'Longitude']
    a['Party Name'] = 'Conservative National Party'
    b = result2.reset_index()[['Division Name', 'Labor Party', 'Latitude', 'Longitude']]
    b.columns = ['Division Name', 'Votes', 'Latitude', 'Longitude']
    b['Party Name'] = 'Labor Party'
    c = result2.reset_index()[['Division Name', 'Greens Party', 'Latitude', 'Longitude']]
    c.columns = ['Division Name', 'Votes', 'Latitude', 'Longitude']
    c['Party Name'] = 'Greens Party'
    d = result2.reset_index()[['Division Name', 'Liberal Party', 'Latitude', 'Longitude']]
    d.columns = ['Division Name', 'Votes', 'Latitude', 'Longitude']
    d['Party Name'] = 'Liberal Party'
    e = result2.reset_index()[['Division Name', 'United Australia Party', 'Latitude', 'Longitude']]
    e.columns = ['Division Name', 'Votes', 'Latitude', 'Longitude']
    e['Party Name'] = 'United Australia Party'
    finall = a.append(b.append(c.append(d.append(e))))

    plt.figure(figsize=[20, 10])
    sns.barplot(x='Division Name', y='Votes', hue='Party Name', data=finall)
    plt.xlabel('City')
    plt.title('Vote Graph of different Political Parties')
    plt.savefig('./static/Vote Graph of different Political Parties.png', bbox_inches='tight')

    sns.distplot(df_neutral['clean_lemmatized Positive Sentiment Score'], label='Neutral', hist=False)
    sns.distplot(df_labor['clean_lemmatized Positive Sentiment Score'], label='Labor Party', hist=False)
    sns.distplot(df_liberal['clean_lemmatized Positive Sentiment Score'], label='Liberal Party', hist=False)
    plt.title('Positive Sentiment Score')
    plt.legend()
    plt.savefig('./static/Positive Sentiment Score.png', bbox_inches='tight')

    sns.distplot(df_neutral['clean_lemmatized Negative Sentiment Score'], label='Neutral', hist=False)
    sns.distplot(df_labor['clean_lemmatized Negative Sentiment Score'], label='Labor Party', hist=False)
    sns.distplot(df_liberal['clean_lemmatized Negative Sentiment Score'], label='Liberal Party', hist=False)
    plt.legend()
    plt.title('Negative Sentiment Score')
    plt.savefig('./static/Negative Sentiment Score.png', bbox_inches='tight')

    sns.distplot(df_neutral['clean_lemmatized Neutral Sentiment Score'], label='Neutral', hist=False)
    sns.distplot(df_labor['clean_lemmatized Neutral Sentiment Score'], label='Labor Party', hist=False)
    sns.distplot(df_liberal['clean_lemmatized Neutral Sentiment Score'], label='Liberal Party', hist=False)
    plt.legend()
    plt.title('Neutral Sentiment Score')
    plt.savefig('./static/Neutral Sentiment Score.png', bbox_inches='tight')

    sns.distplot(df_neutral['clean_lemmatized Compound Sentiment Score'], label='Neutral', hist=False)
    sns.distplot(df_labor['clean_lemmatized Compound Sentiment Score'], label='Labor Party', hist=False)
    sns.distplot(df_liberal['clean_lemmatized Compound Sentiment Score'], label='Liberal Party', hist=False)
    plt.legend()
    plt.title('Compound Sentiment Score')
    plt.savefig('./static/Compound Sentiment Score.png', bbox_inches='tight')

    fig = px.scatter_mapbox(finall, lat="Latitude", lon="Longitude",
                            size='Votes', size_max=40, zoom=4,
                            hover_name='Division Name', hover_data=['Division Name'], color='Party Name')
    fig.update_layout(mapbox_style='stamen-terrain')

    fig.write_html("./static/plotly_mapbox_scatter.html")


    return result
