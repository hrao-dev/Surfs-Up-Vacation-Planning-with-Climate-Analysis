#  Surfs Up!

An application to assist in vacation trip planning in Hawaii with climate analysis using Python (Pandas, Matplotlib), SQLAlchemy (ORM Queries) and Flask. It looks at specific trip dates to model the climate temperature normals and precipitation based on historical weather data in Hawaii from 08-23-2017 to 08-23-2017

<img src="https://github.com/the-Coding-Boot-Camp-at-UT/UT-MCC-DATA-PT-01-2020-U-C/blob/master/homework-instructions/10-Advanced-Data-Storage-and-Retrieval/Instructions/Images/surfs-up.png" alt="Surfs up">

## Step 1 - Climate Analysis and Exploration

A start date of 2018-03-03 and end date of 2018-03-12 are chosen (approximately 10 days in total) for the trip.
SQLAlchemy is used to connect to the sqlite database and reflect the tables into classes and  a reference to those classes called Station and Measurement is saved.

### Precipitation Analysis
A query is designed to retrieve the last 12 months of precipitation data and the results are plotted with 
Pandas.
<img src="https://github.com/hrao-dev/sqlalchemy-challenge/blob/master/Images/Barplot.png" alt="Bar plot">

### Station Analysis
  * The dataset is then queried to determine the total number of avaiable  stations and the most active stations. 
  * Of those,the most active station or the station with the highest number of observations is determined. 
  * A query is  then designed to retrieve the last 12 months of temperature observation data (TOBS) for this station and the results are plotted as a histogram.
<img src="https://github.com/hrao-dev/sqlalchemy-challenge/blob/master/Images/Histogram.png" alt="Histogram">

### Temperature Analysis I
Hawaii is reputed to enjoy mild weather all year. 

The average temperature in June at all stations across all available years in the dataset was identified and compared with the average tempertature in December at all stations across all available years and a t-test was used to determine whether the difference in the means, is statistically significant. 

The larger t-score of 31.355 and a small p value indicates that there is more difference between the two groups or that the average temperatures in June and December in Hawaii are statistically different.

### Temperature Analysis II
The minimum, average and maximum temperatures for the trip are calculated using the previous years temperature data for those same dates. A bar chart is plotted with the average temperature for the y value and the peak-to-peak (tmax-tmin) value as the y error bar (yerr).

(Assuming the trip was planned from "2018-03-03" to "2018-03-12", matching dates from the previous year are "2017-03-03" and "2017-03-12")

<img src="https://github.com/hrao-dev/sqlalchemy-challenge/blob/master/Images/Barplot_error_bars.png" alt="Bar Plot with Error Bars">

#### Daily Rainfall Average
The total amount of rainfall per weather station for the trip dates is calculated using the previous year's matching date and list the station, name, latitude, longitude, and elevation.

#### Daily Normals
 Normals are the averages for the minimum, average, and maximum temperatures. The daily normals for each day of the trip date range are determined and an area chart is plotted for the daily normals using Pandas.

(Assuming the trip was from "2018-03-03" to "2018-03-12", matching dates from the previous year are "2017-03-03" and "2017-03-12")

<img src="https://github.com/hrao-dev/sqlalchemy-challenge/blob/master/Images/Areaplot.png" alt="Area Plot">

## Step 2 - Climate App
A Flask API is designed based on the queries developed as part of the initial analysis above and the following routes are created.

### Routes
  * <b> / </b>  
    * Home page that lists all the routes that are available

  * <b> /api/v1.0/precipitation </b> 
    * Returns a JSON list of all the dates and the corresponding precipitation values

  * <b> /api/v1.0/stations </b> 
    * Returns a JSON list of stations from the dataset
    
  * <b> /api/v1.0/tobs </b> 
    * Returns a JSON list of temperature observations (TOBS) for the previous year for the most active station

  * <b> /api/v1.0/<start> </b> 
    * Returns a JSON list of the minimum, average and the maximum temperatures for all dates greater than and equal to the start date

  * <b> /api/v1.0/<start>/<end> </b> 
    * Returns a JSON list of the minimum, average and the maximum temperatures for a given date range.
