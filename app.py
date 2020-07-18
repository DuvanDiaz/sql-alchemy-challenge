import numpy as np
import datetime as dt
import sqlalchemy   
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import flask, jsonify


###################################################
# Setup
###################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect = True)

###################################################

Measurement = Base.classes.Measurement
Station = Base.classes.station

session = Session(engine)

###################################################
# Flask Setup
###################################################

app = Flask(__name__)

###################################################
# Flask Setup: Routes
###################################################

@app.route("/")
def Hola():
    """List all avaliable API routes."""
    return(
        f"Available Routes:<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"List of Stations: /api/v1.0/dtations<br/>"
        f"Temperature for one year: /api/v1.0/tobs<br/>"
        f"Temperature stat from the start date(yyyy-mm-dd): /api/v1.0/yyyy-mm-dd<br/>"
        f"Temperature stat from start to end dates(yyyy-mm-dd): /api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
    )

@app.route('/api/v1.0/<start>')
def starter(start):
    session = Session(engine)
    qr = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()

    totaltobs = []
    for min,avg,max in qr:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        totaltobs.append(tobs_dict)
        
    return jsonify(totaltobs)

@app.route('/api/v1.0/<start>/<end>')
def starter_end(start,end):
    session = Session(engine)
    qr = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement)).filter(Measurement.date >= start).filter(Measurement.date <= stop).all()
    session.close()

    totaltobs = []
    for min,avg,max in qr:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        totaltobs.append(tobs_dict)

    return jsonify(totaltobs)

@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
    most_active_s = [Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation]
    qr = session.query(*most_active_s).all()
    session.close()

    stations = []
    for station, name, lat, lon, el, in qr:
        stations_dict = {}
        stations_dict["Station"] = station
        stations_dict["Name"] = name
        stations_dict["Lat"] = lat
        stations_dict["Lon"] = lon
        stations_dict["Elevation"] = el
        stations.append(stations_dict)

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    previous_year = dt.date(2017,8,23) - dt.timedelta(days = 365)
    year_stats = session.query(Measurement.tobs).filter(Measurement.date >= previous_year, Measurement.station == "USC00519281").order_by(Measurement.tobs).all()
    yr_stat = []
    for total_yr in year_stats:
        yrstat = {}
        yrstat["tobs"] = total_yr.tobs
        yr_stat.append(yrstat)
    
    return jsonify(yr_stat)

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    prcp_stats = [Measurement.date, Measurement.prcp]
    qr = session.query(*prcp_stats).all()
    session.close()

    precipitation = []
    for date, prcp in qr:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        precipitation.append(prcp_dict)

    return jsonify(precipitation)


if __name__ == "__main__":
    app.run(debug = True)
     


    
