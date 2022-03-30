from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_data")

#Populate the homepage
@app.route("/")
def home():
    query = mongo.db.collection.find_one()

    Latest_title = query['Latest_title']
    Latest_desc = query['Latest_desc']
    Featured_image = query['Featured_image']
    Mars_stats_table = query['Mars_stats_table']
    hd_images = query['hd_images']
    cerberus_img = hd_images[0]['img_url']
    schiaparelli_img = hd_images[1]['img_url']
    syrtis_img = hd_images[2]['img_url']
    valles_img = hd_images[3]['img_url']

    return render_template("index.html", Latest_title = Latest_title, Latest_desc = Latest_desc, Featured_image = Featured_image, Mars_stats_table = Mars_stats_table, cerberus_img = cerberus_img, schiaparelli_img = schiaparelli_img, syrtis_img = syrtis_img, valles_img = valles_img)

#Connect the scrape function from scrape_mars
@app.route("/scrape")
def scrape():
    #run the scrape
    mars_scrape = scrape_mars.scrape()

    #insert the record into MongoDB
    mongo.db.collection.update_one({},{"$set":mars_scrape}, upsert=True)

    #return to home
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)