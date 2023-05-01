# sqlalchemy-challenge

Sean Guzman

 Rutgers Data Sciences Bootcamp, Module 10 Challenge (01 May 2023)

 This module challenge is divided into two parts:
 * Analyze and Explore the Climate Data in Hawaii via Jupyter Notebook
 * Design a Climate App in Python/Flask API

 **Initial Analysis and Exploration of Climate Data in Hawaii** (SurfsUp/climate_starter.ipynb)

 We have an SQLite database containing climate data for Hawaii where we use SQLAlchemy to connect this database to our Jupyter Notebook.  We retrieve the following data:
 * Precipitation Analysis of the past year from the most recent date in the database
 * Station Analysis to calculate the total number of stations, and find the most active one based on obversation counts
 * TOBS Analysis to query TOBS data at the most active station for the past year from the most recent date

  **Creation and Design of Climate App** (SurfsUp/app.py)

  Using the data and information we gathered from our Jupyter Notebook, we create a webpage using Python and Flask API to display this information, and provide routes for the user to visit.
  * Homepage ( / ), homepage which lists all available routes
  * Precipitation ( /api/v1.0/precipitation ), query which lists results from our Precipitation Analysis
  * Stations ( /api/v1.0/stations ), query which lists all stations from our database
  * Temperation Obversation ( /api/v1.0/tobs ), query which lists data from our TOBS Analysis
  * Start Date ( /api/v1.0/<start> ), query which lists minimum, average, and maximum temperatures from a specified start date
  * Start to End Date ( /api/v1.0/<start>/<end> ), query which lists minimum, average, and maximum temperatures from a specified start date to end date.


