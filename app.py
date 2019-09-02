from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scraper_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/Mars_app"
mongo = PyMongo(app)


@app.route("/")
def index():
    # Find one record of data from the mongo database
    destination_data = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", Mars=destination_data)


@app.route("/scrape")
def scraper():
    # Run the scrape function
    Mars_data = scraper_mars.scrape_data()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, Mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
