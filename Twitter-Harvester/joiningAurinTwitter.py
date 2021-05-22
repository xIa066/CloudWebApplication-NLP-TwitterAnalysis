from aurin import *
from twitter import *

result['temp']=1
def df_aurin_joining(df_tobejoined):
    df_tobejoined['temp'] = 1
    df_tobejoined = pd.merge(result, df_tobejoined, on='temp')
    df_tobejoined['longitude_x'] = df_tobejoined['Coordinates'].apply(str).str.strip('[]').str.split('-', expand=True)[0]
    df_tobejoined['latitude_x'] = '-' + df_tobejoined['Coordinates'].apply(str).str.strip('[]').str.split('-', expand=True)[1]
    return df_tobejoined



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

cols = ['longitude_x','latitude_x']

def joined_df_aurin_range(df_range):
    df_range[cols] = df_range[cols].apply(pd.to_numeric, errors='coerce')
    df_range['distance'] = haversine_np(df_range['longitude_x'], df_range['latitude_x'],
                                          df_range['Longitude'], df_range['Latitude'])
    df_range = df_range[df_range.distance < 100]
    df_range = df_range.sort_values('distance').drop_duplicates('cleaned_text').reset_index(drop=True)
    df_range.drop(['Division Name', 'Latitude', 'Longitude', 'temp', 'userLocation', 'longitude_x',
                     'latitude_x', 'distance'], axis=1, inplace=True)
    return df_range




