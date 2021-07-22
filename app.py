# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask, render_template, request
from datetime import datetime
from model import search
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
    message = search(user_response_service,user_response_city, api_key )
    return render_template("results.html", message = message)

