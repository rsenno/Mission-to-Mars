# ## Import the tools
# Use Flask to render a template, redirecting to another url, and creating a URL
from flask import Flask, render_template, redirect, url_for
# Use PyMongo to interact with our Mongo database
from flask_pymongo import PyMongo
# Use the scraping code 
import scraping

# Set up Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
# Tell Python that our app will connect to Mongo using a URI, 
# a uniform resource identifier similar to a URL
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Define the route for the HTML page
@app.route("/")
# Tell Flask what to display when we're looking at the home page, 
# index.html (index.html is the default HTML file that we'll use to display the content we've scraped). 
# This means that when we visit our web app's HTML page, we will see the home page
def index():
    # Use PyMongo to find the "mars" collection in our database, 
    # which we will create when we convert our Jupyter scraping code to Python Script. 
    # We will also assign that path to the mars variable for use later.
    mars = mongo.db.mars.find_one()
    # Tell Flask to return an HTML template using an index.html file. 
    # We'll create this file after we build the Flask routes.
    return render_template("index.html", mars=mars)

# Add the next route and function. 
# @app.route(“/scrape”) defines the route that Flask will be using. 
# This route, “/scrape”, will run the function that we create just beneath it.
@app.route("/scrape")
def scrape():
    # Assign a new variable that points to our Mongo database.
    mars = mongo.db.mars
    # Reference the scrape_all function in the scraping.py file exported from Jupyter Notebook.
    # What scraping.py file?!
    mars_data = scraping.scrape_all()
    # Update the mars db. {} is an empty JSON. upsert creates db if it doesn't exist and updates it. 
    mars.update({}, mars_data, upsert=True)
    return redirect('/', code=302)

# Tell Flask to run the above code. 
# The conditional tells python that if the code is being imported, don't run it.
if __name__ == "__main__":
   app.run()