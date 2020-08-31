from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] = "mongodb://localhost:27017/mongo_app"
# mongo = PyMongo(app)

# Or set inline
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route("/")
def index():
    mars_info = mongo.db.marsFacts.find_one()
    print(mars_info)
    return render_template("index.html", mars_info=mars_info)


@app.route("/scrape")
def scraper():
    marsFacts = mongo.db.marsFacts
    mars_data = scrape_mars.scrape()
    marsFacts.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
