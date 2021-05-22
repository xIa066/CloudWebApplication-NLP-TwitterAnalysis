from db_insert import *
import nltk
from twitter import *
from joiningAurinTwitter import *
import time
import json
def main():

    counter=0
    while True:
        counter=counter+1
        print(counter)
        twitter_connect=api_connect()
        neutral=fun_neu_fetch(twitter_connect[0],twitter_connect[2])
        neutral=clean_tweets(neutral)
        neutral=df_aurin_joining(neutral)
        neutral=joined_df_aurin_range(neutral)
        neutral['tweetCreated'] = pd.to_datetime(neutral['tweetCreated']).dt.strftime("%Y-%m-%d-%H-%M")
        data_neutral = neutral.to_json(orient='records')
        data_n = json.loads(data_neutral)
        neutral_insert=insert_data(data_n)

        labor = fun_lab_fetch(twitter_connect[0], twitter_connect[2])
        labor = clean_tweets(labor)
        labor = df_aurin_joining(labor)
        labor = joined_df_aurin_range(labor)
        labor['tweetCreated'] = pd.to_datetime(labor['tweetCreated']).dt.strftime("%Y-%m-%d-%H-%M")
        data_labor = labor.to_json(orient='records')
        data_lab = json.loads(data_labor)
        labor_insert=insert_data(data_lab)

        liberal = fun_libl_fetch(twitter_connect[0], twitter_connect[2])
        liberal = clean_tweets(liberal)
        liberal = df_aurin_joining(liberal)
        liberal = joined_df_aurin_range(liberal)
        liberal['tweetCreated'] = pd.to_datetime(liberal['tweetCreated']).dt.strftime("%Y-%m-%d-%H-%M")
        data_liberal = liberal.to_json(orient='records')
        data_lib = json.loads(data_liberal)
        liberal_insert= insert_data(data_lib)
    #print(neutral)
        print("before sleep")
        time.sleep(900)
        print("After sleep")
if __name__ == "__main__":
    main()