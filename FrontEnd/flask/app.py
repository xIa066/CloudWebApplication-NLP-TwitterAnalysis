from flask import Flask, render_template, request, session
import pandas as pd


import twitter_functions

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


@app.route('/result',methods = ['POST', 'GET'])
def result():
    error = None
    if request.method == 'POST':
      result = request.form
      session["result"] = result
      api, conn, place_id = twitter_functions.api_connect(result)
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
    api, conn, place_id = twitter_functions.api_connect(result)
    if conn == "Error during authentication":
        error = "Error during authentication"
        return render_template('api_form.html', error=error)
    else:
        error = 'Data downloaded and saved in static folder'
        if request.method == 'POST':
            f = request.files['file']
            df = pd.read_csv(f.stream)
        df_neutral = twitter_functions.fun_neu_fetch(api, place_id, df)
        df_labor = twitter_functions.fun_lab_fetch(api, place_id, df)
        df_liberal = twitter_functions.fun_libl_fetch(api, place_id, df)
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


if __name__ == '__main__':
    # app.run(debug=True)                       # debug mode
    # app.run(host='0.0.0.0', port=5000)        # deployment mode
    app.run()