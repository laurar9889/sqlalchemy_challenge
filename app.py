# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine



#################################################
# Database Setup
#################################################
#Create an engine for the hawaii.sqlite database
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)

# reflect an existing database into ORM classes
Base = automap_base()
Base.prepare(autoload_with = engine)

# reflect the tables
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(bin=engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/api/v1.0/hawaii")
def hawaii():
    """Return the justice league data as json"""
    return jsonify()

@app.route("/")
def welcome():
    return(
        f"Welcome to the Hawaii weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        
    )
    