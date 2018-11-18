# Dependencies
# Import Dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
from flask import Flask, jsonify
import datetime as dt
import numpy as np

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to the invoices and invoice_items tables
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
         "Welcome. I'm sorry for whoever has to grade this <br/>" 
         "Avalable Routes:<br/>"
         "/api/v1.0/precipitation<br/>"
         "- Dates and precipitation observations from last year<br/><br/>"
         "/api/v1.0/stations<br/>"
         "- List of weather stations from the dataset<br/><br/>"
         "/api/v1.0/tobs <br/>"
         "- List of temperature observations (tobs) from the previous year <br/> <br/>"
         "/api/v1.0/start and /api/v1.0/start/end <br/>"
         "- Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range<br>"
    )
    
@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date <= '2017-08-23').\
        filter(Measurement.date >= '2016-08-23').all()

    # Convert the query results into a dictionary using date as the key and precipitation as the value
    all_prcp = []
    for result in results:
        prcp_dict = {}
        prcp_dict["date"] = result[0]
        prcp_dict["prcp"] = result[1]
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)
    
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()   
    stations_list = list(np.ravel(results))
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(Measurement.date, Measurement.tobs).\
        group_by(Measurement.date).\
        filter(Measurement.date <= '2017-08-23').\
        filter(Measurement.date >= '2016-08-23').all()
    tobs_list = list(np.ravel(results))
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start_end(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
        results= session.query(*sel).filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
    results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temps2 = list(np.ravel(results))
    return jsonify(temps2)

if __name__ == '__main__':
    app.run(debug=True)