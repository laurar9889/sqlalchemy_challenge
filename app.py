# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base



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
@app.route("/")
def welcome():
    """Homepage: List all available api routes"""
    return(
        f"Welcome to the Hawaii weather API!. Availabe rountes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/temperature<br/>"
        f"/api/v1.0/ave temperature, min and max temperature"
    
    )

#Draft the code for each page:
@app.route("/api/v1.0/precipitation<br/>")
def precipitation():
     # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query all precipitation data for the last 12  months
    prcp_12month = session.query()
