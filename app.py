# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask, render_template, request
from datetime import datetime
import model
import os

# -- Initialization section --
app = Flask(__name__)

app.config["API_KEY"] = os.getenv("API_KEY")
 
# -- Routes section --
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", time = datetime.now())

@app.route("/results", methods = ["GET", "POST"])
def results():
    api_key = app.config["API_KEY"]
    user_response_city = request.form["city-state"]
    user_response_service = request.form["service"]

    businesses = model.search(user_response_service, user_response_city, api_key ) 
    # -- ^^^^^less code used than referencing model.bussiness_list seperately
    # print(businesses) # enable wehen needed for debugging purposes --

    # -- elements of businesses can now render specific values of keys on html --
    return render_template("results.html", businesses = businesses)

