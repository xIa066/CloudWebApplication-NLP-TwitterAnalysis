import pandas as pd
import numpy as np
#Importing Local Dataset, Cleaning and Filtering
df_local = pd.read_csv('./data/data.csv')

##Fetching only the required columns from the Aurin dataset
df_local = df_local[['fraser_annings_conservative_national_party_ordinary_votes',' socialist_alliance_ordinary_votes',
              ' labor_ordinary_votes', ' the_greens_ordinary_votes', ' national_party_ordinary_votes',
             ' liberal_ordinary_votes', ' united_australia_party_ordinary_votes',
              ' katters_australian_party_kap_ordinary_votes',
            ' latitude', ' longitude', ' division_id', ' division_name', ' polling_place_name', ' state']]

df_local.isna().sum()/df_local.shape[0]*100<69

##Dropping the coulmns not required from the Aurin dataset
df_local.drop([' socialist_alliance_ordinary_votes', ' national_party_ordinary_votes',
               ' katters_australian_party_kap_ordinary_votes'],
              axis=1, inplace=True)

vote_result_division_wise = df_local.groupby(' division_name')[['fraser_annings_conservative_national_party_ordinary_votes',
              ' labor_ordinary_votes', ' the_greens_ordinary_votes',
             ' liberal_ordinary_votes', ' united_australia_party_ordinary_votes']].sum()

#Aggregating count of votes of below 8 different cities of Australia based on their lattitude &longitude
lat_lon = df_local.groupby(' division_name')[[' latitude',' longitude']].agg(np.median)
result = lat_lon.join(vote_result_division_wise, how='outer')
result = result.loc[['Brisbane', 'Canberra', 'Adelaide', 'Melbourne', 'Newcastle', 'Perth', 'Sydney', 'North Sydney'], :]
result = result.reset_index()
result.columns = ['Division Name', 'Latitude', 'Longitude',
       'Conservative National Party',
       'Labor Party', 'Greens Party',
       'Liberal Party', 'United Australia Party']

result.drop(['Conservative National Party',
       'Labor Party', 'Greens Party',
       'Liberal Party', 'United Australia Party'],axis=1, inplace=True)