#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Remeber to export juypter notebook to .py file for importing custom module
from flask import Flask, render_template, request, session
import pandas as pd

# custom modules
import DB_insert as DB
import final_execution

app = Flask(__name__)
app.secret_key = 'random string'


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/5-yr-analysis')
def fvyr_html():
    return "5yr data analysis"


@app.route('/recent-analysis')
def rece_html():
    return render_template('recent-data-analysis.html')

@app.route('/set-api')
def api_cr():
    error = None
    return render_template('api_form.html', error = error)


# In[2]:


@app.route('/result',methods = ['POST', 'GET'])
def result():
    error = None
    if request.method == 'POST':
      result = request.form
      session["result"] = result
      #api, conn, place_id = twitter_functions.api_connect(result)
      api, conn, place_id = final_execution.api_connect(result)
      
      if conn == "Error during authentication":
          error = "Error during authentication"
          return render_template('api_form.html', error = error)
      else:
          error = 'You were successfully logged in'
          return render_template('result.html', error = error, result= result)

@app.route('/add-hashtag')
def add_hashtag():
    error = None
    return render_template('api_form2.html', error = error)

@app.route('/download_data',methods = ['POST', 'GET'])
def download_data():
    error = None
    result = session.get('result')
    #api, conn, place_id = twitter_functions.api_connect(result)
    api, conn, place_id = final_execution.api_connect(result)
    if conn == "Error during authentication":
        error = "Error during authentication"
        return render_template('api_form.html', error=error)
    else:
        error = 'Data downloaded and saved in static folder'
        
        # reserved variable for use later
        df = ''
        if request.method == 'POST':
            f = request.files['file']
            df = pd.read_csv(f.stream)
        
        # calling methods in final_execution.py to process data
        df_neutral = final_execution.df_neutral(api,place_id,df)
        df_labor = final_execution.df_labor(api,place_id,df)
        df_liberal = final_execution.df_liberal(api,place_id,df)
        
        result = final_execution.gen_result()
        final_execution.clean_data(df_neutral,df_labor,df_liberal)
        final_execution.apply_lemm(df_neutral,df_liberal,df_labor)
        
        df_neutral = final_execution.get_sentiment_scores(df_neutral,'clean_lemmatized')
        df_liberal = final_execution.get_sentiment_scores(df_liberal,'clean_lemmatized')
        df_labor = final_execution.get_sentiment_scores(df_labor,'clean_lemmatized')
        
        final_execution.temp(df_neutral,df_liberal,df_labor,result)
        final_execution.add_info(df_neutral,df_liberal,df_labor)
        
        # push the processed data to couchDB through the DB_insert module, which takes input of json file
        DB.insert_DB('liberal',df_liberal.to_json(orient='records'))
        DB.insert_DB('labor',df_labor.to_json(orient='records'))
        DB.insert_DB('neutral',df_neutral.to_json(orient='records'))
        
        # Links to the views on database
        # Please connect to the unimelb VPN to access the database
        #http://172.26.131.32:5984/data1/_design/keyViews/_view/compoundScore?group=true
        #http://172.26.131.32:5984/data1/_design/keyViews/_view/positiveScore?group=true
        #http://172.26.131.32:5984/data1/_design/keyViews/_view/negativeScore?group=true
        #http://172.26.131.32:5984/data1/_design/keyViews/_view/neutralScore?group=true
        
        result2 = {}
        return render_template('result.html', error=error, result=result2)


@app.route('/upload-csv')
def upload_csv():
    error = None
    return render_template('api_form3.html', error = error)

@app.route('/process_csv',methods = ['POST', 'GET'])
def process_csv():
    import csv_functions
    error = 'Data successfully processed'
    if request.method == 'POST':
        f = request.files['file']
        df = pd.read_csv(f.stream)
    df1 = csv_functions.df_clean(df,filter_disatnce = 20)
    result = {}
    return render_template('result.html', error=error, result=result)


# In[ ]:


if __name__ == '__main__':
    #app.run(debug=True)                       # debug mode
    # app.run(host='0.0.0.0', port=5000)        # deployment mode
    app.run()

