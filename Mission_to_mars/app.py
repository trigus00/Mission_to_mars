from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mars_scrape


# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index(): 

    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars_title =mars['titles'], mars_paragraph=mars['paragraph'],mars_image = mars['Mars_Image'],mars_tweet=mars['twitter'],mars_facts = mars['facts'],mars_hemesphere = mars['hemispheres'])

   
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    
    mars_article = mars_scrape.mars_article()
    mars_photo = mars_scrape.mars_image()
    mars_social = mars_scrape.mars_twitter()
    mars_info = mars_scrape.mars_facts()
    mars_hemisphere = mars_scrape.mars_hemespheres()
    
    mars.update({}, mars_article, upsert=True)
    mars.update({}, mars_photo, upsert=True)
    mars.update({}, mars_social, upsert=True)
    mars.update({},mars_info, upsert=True)
    mars.update({}, mars_hemisphere, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
