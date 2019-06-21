from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/nasa_app")

@app.route("/")
def index():
    db_data = mongo.db.mars_data.find_one()

    # Return template and data
    return render_template("index.html", mars_data = db_data)


@app.route("/scrape")
def scrape():
    # drops collection for duplicates
    mongo.db.mars_data.drop()

    # Run scrape_all
    mars_data = scrape_mars.scrape_all()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
