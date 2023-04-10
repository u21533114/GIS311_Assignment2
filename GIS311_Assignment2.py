#from collections import namedtuple
#import altair as alt
import math
import pandas as pd
import streamlit as st
import numpy as np
import geopandas as gpd
import shapely.geometry
#airlines is a table --> can use SQL to create an attribute join to countries table
#airports has co-ordinates --> can create points and plot these on a map; can also join to countries table
#countries is a table
#planes is a table --> can create a bar chart for types of planes
#routes is weird
#NB: 1 map and two charts are needed


"""
# Flight Data Anaylsis \U00002708
This data was aquired from [OpenFlights](https://openflights.org/data.html)
"""

airlines = pd.read_csv('airlines.dat', header = None)
airports = pd.read_csv('airports.dat', header = None)
countries = pd.read_csv('countries.dat', header = None)
planes = pd.read_csv('planes.dat', header = None)
routes = pd.read_csv('routes.dat', header = None)
airports.columns = ['0', '1', '2', '3', '4', '5', 'latitude', 'longitude', '8', '9', '10', '11', '12', '13']

#geometry = [Point(xy) for xy in zip(airports.6, airports.7)]
#crs = {'init': 'epsg:4326'} # set the coordinate reference system
#pnt = gpd.GeoDataFrame(airports, crs=crs, geometry=geometry)
