from db_insert import *
import json

def main():

    counter=0
    while True:
        counter=counter+1
        print(counter)
        #db = connect_server()
        a=api_connect()
        neutral_1=fun_neu_fetch(a[0],a[2])
        neutral_2=clean_neutral(neutral_1)
        neutral_3=neutral_joining(neutral_2)
        neutral=neutral_range(neutral_3)
        neutral['tweetCreated'] = pd.to_datetime(neutral['tweetCreated']).dt.strftime("%Y-%m-%d-%H-%M")
        data_neutral = neutral.to_json(orient='records')
        data_n = json.loads(data_neutral)
        abc=insert_data(data_n)

        labor_1 = fun_lab_fetch(a[0], a[2])
        labor_2 = clean_labor(labor_1)
        labor_3 = labor_joining(labor_2)
        labor = labor_range(labor_3)
        labor['tweetCreated'] = pd.to_datetime(labor['tweetCreated']).dt.strftime("%Y-%m-%d-%H-%M")
        data_labor = labor.to_json(orient='records')
        data_lab = json.loads(data_labor)
        abc_1=insert_data(data_lab)

        liberal_1 = fun_libl_fetch(a[0], a[2])
        liberal_2 = clean_liberal(liberal_1)
        liberal_3 = liberal_joining(liberal_2)
        liberal = liberal_range(liberal_3)
        liberal['tweetCreated'] = pd.to_datetime(liberal['tweetCreated']).dt.strftime("%Y-%m-%d-%H-%M")
        data_liberal = liberal.to_json(orient='records')
        data_lib = json.loads(data_liberal)
        abc_2= insert_data(data_lib)
    #print(neutral)
        print("before sleep")
        time.sleep(900)
        print("After sleep")
if __name__ == "__main__":
    main()