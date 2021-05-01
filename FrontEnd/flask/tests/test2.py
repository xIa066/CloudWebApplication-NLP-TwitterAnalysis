from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
   return render_template("index.html")

if __name__ == '__main__':
   app.run(debug = True)

   # 400 − for Bad Request
   #
   # 401 − for Unauthenticated
   #
   # 403 − for Forbidden
   #
   # 404 − for Not Found
   #
   # 406 − for Not Acceptable
   #
   # 415 − for Unsupported Media Type
   #
   # 429 − Too Many   Requests