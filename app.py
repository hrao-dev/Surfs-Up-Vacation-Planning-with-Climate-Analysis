import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, distinct

from flask import Flask, jsonify
from datetime import datetime



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"<h2>Welcome to Hawaii Weather and Precipitation Analysis API!!</h2>"
        f"<img src='https://thebigphotos.com/wp-content/uploads/2018/07/wailea-hawaii.jpg'" 
        f"<br/><br/><h3>Available Routes:</h3>"
        f"<ul>"
        f"<li><a href='http://127.0.0.1:5000/api/v1.0/precipitation'>Precipitation data</a></br>"
        f"<i>Usage: Append /api/v1.0/precipitation to the URL </i></li><br/>"
        f"<li><a href='http://127.0.0.1:5000/api/v1.0/stations'>Stations in the dataset</a><br/>"
        f"<i>Usage: Append /api/v1.0/stations to the URL </i></li><br/>"
        f"<li><a href='http://127.0.0.1:5000/api/v1.0/tobs'>Temperature observations of the most active station for the previous year </a><br/>"
        f"<i>Usage: Append /api/v1.0/tobs to the URL </i></li><br/>"
        f"<li><a href='http://127.0.0.1:5000/api/v1.0/2012-02-28'>Minimum, average and maximum temperatures for a given start date</a><br/>"
        f"<i>Usage: Append a start date to URL such as 2015-01-01 </i></li><br/>"
        f"<li><a href='http://127.0.0.1:5000/api/v1.0/2012-02-28/2012-03-05'>Minimum, average and maximum temperatures for a given date range</a></li>"
        f"<i>Usage: Append start and end dates to URL such as 2015-01-01/2015-01-10 </i></li><br/>"
        f"</ul>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all the dates and the corresponding precipitation values"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

# Create a dictionary from the row data and append to a list 
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations"""
    # Query all stations
    results = session.query(distinct(Station.station)).all()
    results_1 = session.query(Station.station, Station.name).group_by(Station.station).all()
    session.close()

# Convert list of tuples into normal list
    #stations = list(np.ravel(results))
    #return jsonify(stations)

    all_stations = []
    for station, name in results_1:
        stations_dict = {}
        stations_dict["name"] = name
        stations_dict["station"] = station
        all_stations.append(stations_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperature observations (TOBS) for the previous year for the most active station"""
    # Query most active station
    most_active_station = (session.query(Measurement.station)
                          .group_by(Measurement.station)
                          .order_by(func.count(Measurement.station).desc())).first()
    most_active_station = str(most_active_station)
    most_active_station = most_active_station.replace("('","")
    most_active_station = most_active_station.replace("',)","")

    # Query the start and end dates for the duration
    lastdate = (session.query(Measurement.date)
                .order_by(Measurement.id.desc())).first()
    lastdate = str(lastdate)
    lastdate = lastdate.replace("('","")
    lastdate = lastdate.replace("',)","")
    last_date = datetime.strptime(lastdate, "%Y-%m-%d")
    last_date = datetime.date(last_date)
    print("Last Date: ", last_date)

    start_date = last_date - dt.timedelta(days=365)
    print("Start Date: ", start_date)

    # Query dates and temperature observations of the most active station for the last year of data
    temp_results = (session.query(Measurement.date, Measurement.tobs)
                                    .filter(Measurement.date >= start_date)
                                    .filter(Measurement.date <= last_date)
                                    .filter_by(station=most_active_station)).all()
 
    session.close()

    # Create a dictionary from the row data and append to a list 
    active_station_temps = []
    for date, tobs in temp_results:
        active_station_dict = {}
        active_station_dict["date"] = date
        active_station_dict["tobs"] = tobs
        active_station_temps.append(active_station_dict)

    return jsonify(most_active_station,active_station_temps)

@app.route("/api/v1.0/<start>")
def temp_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of the minimum temperature, the average temperature, and the max temperature for a given start date"""
    # Query most active station

    start_dt = datetime.strptime(start, "%Y-%m-%d")
    print("Start Date: ", start_dt)

    # Query minimum,average and maximum temperature for a given start date
    temps = (session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs))
                           .filter(Measurement.date >= start_dt)).all()

    print(temps)
 
    session.close()

    # Create a dictionary from the row data and append to a list 
    temp_stats = []
    for temp in temps:
        temps_dict = {}
        temps_dict["Min.Temp"] = round(temps[0][0],2)
        temps_dict["Avg.Temp"] = round(temps[0][1],2)
        temps_dict["Max.Temp"] = round(temps[0][2],2)
        temp_stats.append(temps_dict)

    return jsonify(temps_dict)

@app.route("/api/v1.0/<start>/<end>")
def temp_date_range(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of the minimum temperature, the average temperature, and the max temperature for a given start date"""
    # Query most active station

    start_dt = datetime.strptime(start, "%Y-%m-%d")
    start_dt = datetime.date(start_dt)
    end_dt = datetime.strptime(end, "%Y-%m-%d")
    end_dt = datetime.date(end_dt)
    print("Start Date: ", start_dt)
    print("End Date: ", end_dt)

    # Query minimum,average and maximum temperature for a given start date
    temps = (session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs))
                           .filter(Measurement.date >= start_dt)
                           .filter(Measurement.date <= end_dt)).all()

    print(temps)
 
    session.close()

    #Convert list of tuples into normal list
    #temp_stats = list(np.ravel(temps))

    # Create a dictionary from the row data and append to a list 
    temp_stats = []
    for temp in temps:
        temps_dict = {}
        temps_dict["Min.Temp"] = round(temps[0][0],2)
        temps_dict["Avg.Temp"] = round(temps[0][1],2)
        temps_dict["Max.Temp"] = round(temps[0][2],2)
        temp_stats.append(temps_dict)

    return jsonify(temps_dict)

    #return jsonify(temp_stats)
    

if __name__ == '__main__':
    app.run(debug=True)
