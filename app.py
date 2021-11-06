from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)
app.config['Mongo_URI'] = 'mongdb://localhost:27017/mars_app'
mongo = PyMongo(app)

@app.route('/')
def index():
    # Find one record of data from the mongo database
    mars_data = mongo.db.collection.find_one()
    print(mars_data)
    # Return template and data
    return render_template('index.html', mars = mars_data)

@app.route ('/scrape')

def scraper():
    planet_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert = True
    mongo.db.collection.update({}, planet_data, upsert = True)

    # Redirect back to home page
    retuen redirect ('/')

if __name__ == '__main__':
    app.run(debug = True)