from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
   mars = mongo.db.mars.find_one() #pulls the data out of the database , stores it in the mars variable
   return render_template("index.html", mars=mars) #passing it back into the html & html displays it

@app.route("/scrape") #being called by the button from html
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all() #does the scraping and stores it into mars_data
   mars.update({}, mars_data, upsert=True) #updates mongodatabase
   return redirect('/', code=302) #redirects it back to line 11

if __name__ == "__main__":
    app.run()