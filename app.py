# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask, render_template, request, redirect, session, json
from flask_pymongo import PyMongo
from datetime import datetime
import model
import math
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
final_list = []
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
            "password": request.form["password"],
            "saves": []
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

@app.route("/account", methods=["GET","POST"])
def account():
        users = mongo.db.users
        saves = []
        user = users.find_one({"username": session["username"]})
        if user["saves"] is None:
            saves = ["Nothing"]
        else:
            saves = user["saves"]
        return render_template("account.html", saves = saves)

@app.route("/save/<business_id>")
def save(business_id):
    global final_list
    query = {"username": session["username"]}
    users = mongo.db.users
    user_businesses_save = {}
    print("business id: " + business_id)
    user = users.find_one({"username": session["username"]})
    for x in final_list:
        if x["id"] == business_id:
            print("FOUND MATCH: " + x["id"])
            user_businesses_save = x
            break
    save_exists = False
    print("user save is: " + str(user_businesses_save["name"]))
    if len(user["saves"]) < 1:
        print(user_businesses_save["name"] + " has been saved")
        user["saves"].append(user_businesses_save)
        value = {"$set": {"saves": user["saves"]}}
        users.update_one(query, value)
    else:
        for save in user["saves"]:
            if user_businesses_save["id"] == save["id"]:
                print("EXISTING save is: " + str(save))
                save_exists = True
                return "save already exists"
        if save_exists is False:
            print(user_businesses_save["name"] + " has been saved")
            user["saves"].append(user_businesses_save)
            value = {"$set": {"saves": user["saves"]}}
            users.update_one(query, value)
                
    return redirect("/results") 

@app.route("/logout")
def logout():
    # removes session
    session.clear()
    return render_template("index.html")


@app.route("/results", methods=["GET", "POST"])
def results():
    if request.method == "GET":
        global businesses
        global final_list
        api_key = app.config["YELP_API_KEY"]
        gmapskey = app.config["GMAPS_KEY"]
        user_response_city = request.form["citystate"]
        user_response_service = request.form["service"]
        businesses = model.search(user_response_service,
                                  user_response_city, api_key)
        final_list = businesses
        # -- ^^^^^less code used than referencing model.bussiness_list seperately
        # print(businesses) # enable wehen needed for debugging purposes --
        # lat = []
        # long = []
        # for x in range(len(businesses)):
        #     lat.append(businesses[x]["coordinates"]["latitude"])
        # for x in range(len(businesses)):
        #     long.append(businesses[x]["coordinates"]["longitude"])
        lat = businesses[1]["coordinates"]["latitude"]
        lng = businesses[1]["coordinates"]["longitude"]

        gmapsLocations = []
        for x in range(len(model.business_list)):
            gmapsLocations.append(
                {"lat": businesses[x]["coordinates"]["latitude"], "lng": businesses[x]["coordinates"]["longitude"]})
        gmapsLocations = json.dumps(gmapsLocations)
        businesses_names = []
        for x in range(len(model.business_list)):
            businesses_names.append(businesses[x]["name"])
        businesses_names = json.dumps(businesses_names)

        businesses_address = []
        for x in range(len(model.business_list)):
            businesses_address.append(businesses[x]["location"]["display_address"])
        businesses_address = json.dumps(businesses_address)

        businesses_images = []
        for x in range(len(model.business_list)):
            businesses_images.append(businesses[x]["image_url"])
        businesses_images = json.dumps(businesses_images)
        # -- elements of businesses can now render specific values of keys on html --

        img_ref = []
        rating_debug = []

        for business in businesses:
            rating = float(business["rating"])
            img_name = "regular_"
            if rating >= 1:
                if rating % 1 > 0.25 and rating % 1 <= 0.75:
                    img_name += str(math.trunc(rating))
                    img_name += "_half"
                elif rating % 1 > 0.75:
                    img_name += str(math.trunc(rating + 1))
                else:
                    img_name += str(math.trunc(rating))
                img_name += ".png"
            else:
                img_name = "regular_0.png"
            img_ref.append(img_name)
            rating_debug.append(rating)

        # print(img_ref)
        # print(rating_debug)

        # -- elements of businesses can now render specific values of keys on html --
        return render_template("results.html", businesses=businesses, gmapskey=gmapskey, stars_img=img_ref, lat=lat, lng=lng, gmapsLocations=gmapsLocations, businesses_names=businesses_names, businesses_address=businesses_address, businesses_images=businesses_images)
