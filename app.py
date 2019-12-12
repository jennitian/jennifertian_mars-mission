from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping

#flask name
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
   #new variable for mongo db
   mars = mongo.db.mars
   #new variable to scrape data
   mars_data = scrape_mars.scrape_all()
   #updating mars_data db in mongo
   mars.update({}, mars_data, upsert=True)
   return "Scraping Successful!"

if __name__ == "__main__":
   app.run()