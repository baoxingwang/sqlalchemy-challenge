import numpy as np
import os

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify

from sqlalchemy import create_engine, inspect, func

#create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start_date><br/>"
        f"/api/v1.0/<start>/<end>"
    )



@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of date and prcp"""
# Query all date and prcp
    session = Session(engine)
    results = session.query(Measurement.date,Measurement.prcp).all()

    # close the session to end the communication with the database
    session.close()

    # Convert list of tuples into normal dict
    date_prcp = dict(results)

    return jsonify(date_prcp)

@app.route("/api/v1.0/station")
def station():
    """Return a list of station"""
# Query all date and prcp
    session = Session(engine)
    results = session.query(Measurement.station).all()

    # close the session to end the communication with the database
    session.close()

    # Convert list of tuples into normal list
    station = list(np.ravel(results))

    return jsonify(station)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of tobs"""
# Query all date and prcp
    session = Session(engine)
    results = session.query(Measurement.tobs).\
        filter(Measurement.date >= '2016-08-23').all()

    # close the session to end the communication with the database
    session.close()

    # Convert list of tuples into normal list
    tobs = list(np.ravel(results))

    return jsonify(tobs)


@app.route("/api/v1.0/<start_date>")
def calc_temps(start_date):
    
# Query all date and prcp
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

    # close the session to end the communication with the database
    session.close()

    # Convert list of tuples into normal list
    tobs = results

    return calc_temps(start_date)




if __name__ == '__main__':
    app.run(debug=True)