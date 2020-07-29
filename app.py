# import common dependencies
import datetime as dt
import numpy as np
import pandas as pd

#SqlAlchemy import for database instance
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import Flask dependency
from flask import Flask, jsonify

# Set up the database
engine = create_engine("sqlite:///hawaii.sqlite")
# Reflect the database
Base = automap_base()
Base.prepare(engine, reflect=True)
# Save references to each table in a variable
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create a session link from Python to database
session = Session(engine)

# Define the app for the Flask application
# Create a Flask application called “app”
app = Flask(__name__)

# Set up the Flask routes
# Add the main/root
@app.route("/")
# Add the routing information for each of the other routes
# Welcome route
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
	filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

# Stations route
# convert "unraveled" results into a list (list of lists becomes one flat list)
# stations=stations code formats the list into JSON. 
@app.route("/api/v1.0/stations")
def stations():
    results =  session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Temperature Observations (tobs) route
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 9, 23) - dt.timedelta(days=365)
    results =  session.query(Measurement.tobs).\
     filter(Measurement.station == 'USC00519281').\
     filter(Measurement.station >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Temperature Statistics route
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)]
    if not end:
        results = session.query(*sel).\
         filter(Measurement.date <= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
    else:
        results = session.query(*sel).\
         filter(Measurement.date >= start).\
         filter(Measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps=temps)