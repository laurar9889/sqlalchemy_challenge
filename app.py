# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import numpy as np
# import datetime as dt
from datetime import datetime, timedelta


#################################################
# Database Setup
#################################################
#Create an engine for the hawaii.sqlite database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into ORM classes
Base = automap_base()
Base.prepare(autoload_with=engine)

# reflect the tables
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

#1. Create the routes available for the user to follow
@app.route("/")
def welcome():
    """Homepage: List all available api routes"""
    return(
        f"Welcome to the Hawaii weather API. Available routes below:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    
    )

#Draft the code for each app:
#2. Query to define next step when getting into precipitation URL
@app.route("/api/v1.0/precipitation")
def precipitation():
     # Create our session (link) from Python to the DB
    session = Session(engine)
    #Use the same script used in climate_starter to retrieve last 12 months info
    max_date = session.query(func.max(Measurement.date)).scalar()
    last_year_date = datetime.strptime(max_date, '%Y-%m-%d') - timedelta(days=366)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>=last_year_date).all()
    
    session.close()

    # Create a dictionary from the row data and append to a list of all precipitation results
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)
    #Return a JSON representation of the dictionary
    return jsonify(all_prcp)


#3. Query to define next step when getting into stations URL:
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))
    #Return a JSON representation of the dictionary
    return jsonify(all_names)

#4. Query to define next step when getting into temperature(tobs) URL:
@app.route("/api/v1.0/tobs")
def tobs():
     # Create our session (link) from Python to the DB
    session = Session(engine)

    max_date = session.query(func.max(Measurement.date)).scalar()
    last_year_date = datetime.strptime(max_date, '%Y-%m-%d') - timedelta(days=366)
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date>=last_year_date).filter(Measurement.station == 'USC00519281').all()
    
    session.close()

    # Create a dictionary from the row data and append to a list of all_tobs
    all_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)
    #Return a JSON representation of the dictionary
    return jsonify(all_tobs)

#5.A Query to define next step when getting into start date URL and the user puts a specific date:
#Design this query as dynamic input (<>) so that the user can change the date.
@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    #Use the code used in climate_started jupyter notebook to find out min, max, ave temperature of a certain date
    start_date_results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()

    session.close()

    # Convert list of tuples into normal list
    all_start_date = list(np.ravel(start_date_results))
    #Return a JSON representation of the dictionary
    return jsonify(all_start_date)

#5.B Query to define next step when getting into start/end date URL and the user puts a specific end date:
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    #Use the code used in climate_started jupyter notebook to find out min, max, ave of a certain date
    start_end_date_results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    session.close()

    # Convert list of tuples into normal list
    all_start_end_date_results = list(np.ravel(start_end_date_results))
    #Return a JSON representation of the dictionary
    return jsonify(all_start_end_date_results)

#Use the debugger to continuously work on the file while getting results of potential errors.
if __name__ == '__main__':
    app.run(debug=True)