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
    user_response_city = request.form["city"]
    user_response_service = request.form["service"]
    model.search(user_response_service, user_response_city, api_key )
    businesses = model.businesses
    return render_template("results.html", names = businesses['name'], location =businesses['location'] )

