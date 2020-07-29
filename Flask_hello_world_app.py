# import the Flask dependency
from flask import Flask

# create a new Flask app instance
app = Flask(__name__)

# Create a route
# Whenever you make a route in Flask, 
# you put the code you want in that specific route below @app.route()
@app.route('/')
def hello_world():
    return "Hello World"

