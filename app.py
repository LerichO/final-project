# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask, render_template, request, redirect, session
from flask_pymongo import PyMongo
from datetime import datetime
import model
import os
 
# -- Initialization section --
app = Flask(__name__)

app.config["YELP_API_KEY"] = os.getenv("YELP_API_KEY")
app.config["GMAPS_KEY"] = os.getenv("GMAPS_KEY")
mongo_password = os.getenv('PASSWORD')
app.secret_key = os.getenv('SECRET_KEY')
app.config['MONGO_DBNAME'] = 'databse'
app.config['MONGO_URI'] = f'mongodb+srv://admin:{mongo_password}@cluster0.dveg5.mongodb.net/small-services-finder?retryWrites=true&w=majority'
mongo = PyMongo(app)
# -- Routes section --


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", time=datetime.now())


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        users = mongo.db.users  # creates a users database in mongoDB if none exist already

        # stores form data into user dictionary
        user = {
            "username": request.form["user_name"],
            "password": request.form["password"]
        }

        # check for existing user exists
        exisiting_user = users.find_one({"username": user["username"]})
        # condition for if user exists
        if exisiting_user is None:
            # adds user into mongo
            users.insert(user)
            # tell the browser session who the user is
            session["username"] = request.form["user_name"]
            return "user has been created"
        else:
            return "That username is taken"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        users = mongo.db.users  # creates a users database in mongoDB if none exist already

        # stores form data into user dictionary
        user = {
            "username": request.form["user_name"],
            "password": request.form["password"]
        }

        # check for existing user exists
        exisiting_user = users.find_one({"username": user["username"]})
        # condition for if user exists
        if exisiting_user is None:
            return "That username does not exist, try signing up an account instead."
        else:
            error = ""
            # check if passwords match
            if user['password'] == exisiting_user['password']:
                session['username'] = user['username']
                return redirect("/")
            else:
                error = "That's not the correct password"
                return render_template('login.html', error=error)
            session["username"] = request.form["user_name"]
            return render_template("index.html")


@app.route("/logout")
def logout():
    # removes session
    session.clear()
    return render_template("index.html")


@app.route("/results", methods=["GET", "POST"])
def results():
    api_key = app.config["YELP_API_KEY"]
    gmapskey = app.config["GMAPS_KEY"]
    user_response_city = request.form["citystate"]
    user_response_service = request.form["service"]

    businesses = model.search(user_response_service, user_response_city, api_key)
    # -- ^^^^^less code used than referencing model.bussiness_list seperately
    # print(businesses) # enable wehen needed for debugging purposes --

    # -- elements of businesses can now render specific values of keys on html --
    return render_template("results.html", businesses=businesses, gmapskey = gmapskey)
