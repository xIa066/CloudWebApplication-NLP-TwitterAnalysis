from aurin import *
from twitter import *

result['temp']=1
def neutral_joining(df_neutral):
    df_neutral['temp'] = 1
    df_neutral = pd.merge(result, df_neutral, on='temp')
    df_neutral['longitude_x'] = df_neutral['Coordinates'].apply(str).str.strip('[]').str.split('-', expand=True)[0]
    df_neutral['latitude_x'] = '-' + df_neutral['Coordinates'].apply(str).str.strip('[]').str.split('-', expand=True)[1]
    return df_neutral

def labor_joining(df_labor):
    df_labor['temp']=1
    df_labor = pd.merge(result, df_labor, on='temp')
    df_labor['longitude_x'] = df_labor['Coordinates'].apply(str).str.strip('[]').str.split('-', expand=True)[0]
    df_labor['latitude_x'] = '-' + df_labor['Coordinates'].apply(str).str.strip('[]').str.split('-', expand=True)[1]
    return df_labor

def liberal_joining(df_liberal):
    df_liberal['temp']=1
    df_liberal = pd.merge(result, df_liberal, on='temp')
    df_liberal['longitude_x'] = df_liberal['Coordinates'].apply(str).str.strip('[]').str.split('-', expand=True)[0]
    df_liberal['latitude_x'] = '-' + df_liberal['Coordinates'].apply(str).str.strip('[]').str.split('-', expand=True)[1]
    return df_liberal

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

def neutral_range(df_neutral):
    df_neutral[cols] = df_neutral[cols].apply(pd.to_numeric, errors='coerce')
    df_neutral['distance'] = haversine_np(df_neutral['longitude_x'], df_neutral['latitude_x'],
                                          df_neutral['Longitude'], df_neutral['Latitude'])
    df_neutral = df_neutral[df_neutral.distance < 20]
    df_neutral = df_neutral.sort_values('distance').drop_duplicates('cleaned_text').reset_index(drop=True)
    df_neutral.drop(['Division Name', 'Latitude', 'Longitude', 'temp', 'userLocation', 'longitude_x',
                     'latitude_x', 'distance'], axis=1, inplace=True)
    return df_neutral

def labor_range(df_labor):
    df_labor[cols] = df_labor[cols].apply(pd.to_numeric, errors='coerce')
    df_labor['distance'] = haversine_np(df_labor['longitude_x'], df_labor['latitude_x'],
                                        df_labor['Longitude'], df_labor['Latitude'])
    df_labor = df_labor[df_labor.distance < 20]
    df_labor = df_labor.sort_values('distance').drop_duplicates('cleaned_text').reset_index(drop=True)
    df_labor.drop(['Division Name', 'Latitude', 'Longitude', 'temp', 'userLocation', 'longitude_x',
                     'latitude_x', 'distance'], axis=1, inplace=True)
    return df_labor

def liberal_range(df_liberal):
    df_liberal[cols] = df_liberal[cols].apply(pd.to_numeric, errors='coerce')
    df_liberal['distance'] = haversine_np(df_liberal['longitude_x'], df_liberal['latitude_x'],
                                          df_liberal['Longitude'], df_liberal['Latitude'])
    df_liberal = df_liberal[df_liberal.distance < 20]
    df_liberal = df_liberal.sort_values('distance').drop_duplicates('cleaned_text').reset_index(drop=True)
    df_liberal.drop(['Division Name', 'Latitude', 'Longitude', 'temp', 'userLocation', 'longitude_x',
                     'latitude_x', 'distance'], axis=1, inplace=True)
    return df_liberal
