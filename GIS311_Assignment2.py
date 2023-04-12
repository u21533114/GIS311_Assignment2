import math
import pandas as pd
import streamlit as st
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
#NB: 1 map and two charts are needed


"""
# South African Flight Data Analysis
This data was aquired from [OpenFlights](https://openflights.org/data.html)
"""

airlines = pd.read_csv('airlines.dat', header = None)
airports = pd.read_csv('airports.dat', header = None)
countries = pd.read_csv('countries.dat', header = None)
planes = pd.read_csv('planes.dat', header = None)
routes = pd.read_csv('routes.dat', header = None)

#create map showing major airports in SA
#filter dataset
airports.columns = ['0', 'Name', 'City', 'Country', 'IATA Code', '5', 'Latitude', 'Longitude', '8', '9', '10', '11', '12', '13']
sa_airports = airports[airports['Country'] == 'South Africa']
sa_airports = sa_airports.drop(6618)
iata_codes = ['JNB', 'CPT', 'DUR', 'PLZ', 'ELS', 'GRJ', 'BFN', 'HLA']
major_sa_airports = sa_airports[sa_airports['IATA Code'].isin(iata_codes)]
pnt = gpd.GeoDataFrame(major_sa_airports, geometry = gpd.points_from_xy(major_sa_airports['Longitude'], major_sa_airports['Latitude']))
pnt = pnt.set_crs('EPSG:4326')
#plot map
ax = pnt.plot(figsize=(10, 6), alpha=0.5, color='red', marker='s', markersize=50)
ax.set_title('Major Airports in South Africa', fontsize=16)
ax.set_xlabel('Longitude', fontsize=12)
ax.set_ylabel('Latitude', fontsize=12)
for i, row in major_sa_airports.iterrows():
    plt.annotate(row['Name'], xy=(row['Longitude'], row['Latitude']), xytext=(5, 5), textcoords='offset points', fontsize=8, fontweight='bold')
ctx.add_basemap(ax, crs=pnt.crs.to_string(), source=ctx.providers.Stamen.TonerLite)
