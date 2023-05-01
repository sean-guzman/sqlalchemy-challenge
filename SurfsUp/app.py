import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

 # Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Function to retrieve start and end dates from data
def dates():
    
    start_date = session.query(func.min(Measurement.date)).first()
    end_date = session.query(func.max(Measurement.date)).first()   
    session.close()
    
    return (start_date, end_date)

#################################################
# Flask Routes
#################################################

# Homepage, listing all routes
@app.route("/")
def welcome():
    
    # Retrieve start and end dates
    start_date, end_date = dates()
    
    """List all available api routes."""
    
    return (
        f'Surfs Up! And weclome to the Hawaiian climate API!<br/><br/>'
        f'Available Routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/{start_date[0]}<br/>'
        f'/api/v1.0/{start_date[0]}/{end_date[0]}<br/><br/>'
        f'** Dates must be between {start_date[0]} and {end_date[0]} in YYYY-MM-DD format.<br/>'
        
    )

# Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():

    # Retrieve date and precipitation values for past year
    date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precip_results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= date).all()
    session.close()
        
    # Create list for json results
    precip_results_json = []
    
    for date, precip in precip_results:
        date = date
        precip = precip
        
        # Add date and precipitation to dictionary
        result_dict = {date : precip
                    }
        
        # Then add to json results
        precip_results_json.append(result_dict)
           
    # Return results in json format
    return jsonify(precip_results_json)

# Stations route
@app.route("/api/v1.0/stations")
def station():
    
    # Retrieve all stations in database
    stations_results = session.query(Station.station, Station.name).all()
    session.close()
        
    # Create list for json results
    stations_results_json = []
    
    for station, name in stations_results:
        station = station
        name = name
        
        # Add date and precipitation to dictionary
        result_dict = {"Station": station,
                    "Name": name
                    }
        
        # Then add to json results
        stations_results_json.append(result_dict)
    
    # Return results in json format
    return jsonify(stations_results_json)

# Tobs route
@app.route("/api/v1.0/tobs")
def tobs():

    # Retrieve data in json format for most active station for the past year
    date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs_results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= date).all()
    
    # Close session afterwards
    session.close()
    
    # Create list for json results
    tobs_results_json = []
    
    for date, temperature in tobs_results:
        date = date
        temperature = temperature
        
        # Add date and precipitation to dictionary
        result_dict = {"Date": date,
                    "Temperature": temperature
                    }
        
        # Then add to json results
        tobs_results_json.append(result_dict)
   
    # Return results in json format
    return jsonify(tobs_results_json)

# Start Date route
@app.route('/api/v1.0/<start>')
def start_date(start):
    
    # Retrieve start and end dates
    start_date, end_date = dates()
    
    # Create list with query for minimum, average, and maximum temperatures
    sel = [func.min(Measurement.tobs),
           func.avg(Measurement.tobs),
           func.max(Measurement.tobs)
    ]
    
    # Save query results on given start date and close session after
    results = session.query(*sel).filter(Measurement.date >= start).all()
    session.close()
    
    # Convert results into dictionary
    results_json = [
        {"Minimum Temperature": results[0][0]},
        {"Average Temperature": results[0][1]},
        {"Maximum Temperature": results[0][2]}
    ]
    
    # Return results in json format under condition
    if start <= end_date[0]:
        
        return jsonify(results_json)
    else:
        return (f'Error: Please enter valid date between {start_date[0]} and {end_date[0]} in YYYY-MM-DD format.')

# Start to End Date route
@app.route('/api/v1.0/<start>/<end>')
def start_end_date(start, end):

    # Retrieve start and end dates
    start_date, end_date = dates()
    
    # Create list with query for minimum, average, and maximum temperatures
    sel = [func.min(Measurement.tobs),
           func.avg(Measurement.tobs),
           func.max(Measurement.tobs)
    ]
    
    # Save query results on given start date and close session after
    results = session.query(*sel).filter(Measurement.date.between(start, end)).all()
    session.close()
    
    # Convert results into dictionary
    results_json = [
        {"Minimum Temperature": results[0][0]},
        {"Average Temperature": results[0][1]},
        {"Maximum Temperature": results[0][2]}
    ]
   
    # Return results in json format under condition
    if (start >= start_date[0]) and (start <= end_date[0]) and (end >= start_date[0]) and (end <= end_date[0]) and (start < end):
        return jsonify(results_json)
    else:
        return (f'Error: Please enter valid date between {start_date[0]} and {end_date[0]} and in YYYY-MM-DD format.')
    
    
# Main
if __name__ == "__main__":
    app.run(debug=True)