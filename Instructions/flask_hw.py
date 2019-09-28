import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
from datetime import datetime
from datetime import timedelta

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def home():
    print("Home Page")
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/{{start}}<br/>"
        f"/api/v1.0/{{start}}/{{end}}"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    
    session.close()
    
    precip_all = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        precip_all.append(precip_dict)
        
    return jsonify(precip_all)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
           
    session.close()
       
    stations_all = []
    for station in results:
        stations_dict = {}
        stations_dict["station"] = station
        stations_all.append(stations_dict)
        
    return jsonify(stations_all)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    latestdate = session.query(func.max(Measurement.date)).scalar()
    latestdate = dt.datetime.strptime(latestdate, '%Y-%m-%d')
    yearago = latestdate - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date == yearago).all()  
           
    session.close()
    tobs_all = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_all.append(tobs_dict)
        
    return jsonify(tobs_all)

@app.route("/api/v1.0/<start>")           
def route_start(start):
    session = Session(engine)
    startdate = datetime.strptime(start, '%Y-%m-%d')
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= startdate).all()
    session.close()
    
    start_all = []
    for min, max, avg in results:
        start_dict = {}
        start_dict["mintemp"] = min
        start_dict["maxtemp"] = max
        start_dict["avgtemp"] = avg
        start_all.append(start_dict)
           
    return jsonify(start_all)

@app.route("/api/v1.0/<start>/<end>")
def route_start_end(start, end):
    session = Session(engine)
    startdate = datetime.strptime(start, '%Y-%m-%d')
    enddate = datetime.strptime(end, '%Y-%m-%d')
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date <= enddate, Measurement.date >= startdate).all()
    session.close()
    
    startend_all = []
    for min, max, avg in results:
        startend_dict = {}
        startend_dict["mintemp"] = min
        startend_dict["maxtemp"] = max
        startend_dict["avgtemp"] = avg
        startend_all.append(startend_dict)
           
    return jsonify(startend_all)

if __name__ == '__main__':
    app.run(debug=True)
    
    