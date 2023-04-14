import math
import pandas as pd
import streamlit as st
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
import altair as alt
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
###

# Create GeoDataFrame
gdf = gpd.GeoDataFrame(
    major_sa_airports, geometry=gpd.points_from_xy(major_sa_airports.Longitude, major_sa_airports.Latitude), crs='EPSG:4326')

# Create scatter plot
scatter = alt.Chart(gdf).mark_point(size=100, filled=True, color='red', opacity=0.5).encode(
    x=alt.X('Longitude', title='Longitude'),
    y=alt.Y('Latitude', title='Latitude'),
    tooltip=['Name']
).properties(
    title='Major Airports in South Africa',
    width=600,
    height=400
)

# Add airport labels
text = alt.Chart(gdf).mark_text(dx=10, dy=0, fontWeight='bold').encode(
    x='Longitude',
    y='Latitude',
    text='Name'
)

chart = scatter + text

# Add basemap
background = alt.Chart(gdf).mark_geoshape(
    stroke='black',
    strokeWidth=0.5
).encode(
    color=alt.value('white'),
    opacity=alt.value(0.1)
).properties(
    width=600,
    height=400
)

st.altair_chart(chart + background + 
                alt.layer(
                    ctx.providers.OpenStreetMap.Mapnik().tiles,
                    ctx.providers.OpenStreetMap.Mapnik().labels
                ), use_container_width=True)


#update routes table
routes.columns = ['0', '1', 'Source IATA', '3', 'Destination IATA', '5', '6', '7', '8']
iata_codes = ['JNB', 'CPT', 'DUR', 'PLZ', 'ELS', 'GRJ', 'BFN', 'HLA']
major_sa_routes = routes[routes['Source IATA'].isin(iata_codes) | routes['Destination IATA'].isin(iata_codes)]
city_dict = {'JNB': 'Johannesburg', 
             'CPT': 'Cape Town', 
             'DUR': 'Durban', 
             'PLZ': 'Port Elizabeth', 
             'ELS': 'East London', 
             'GRJ': 'George', 
             'BFN': 'Bloemfontein', 
             'HLA': 'Lanseria'}
major_sa_routes['Source City'] = major_sa_routes['Source IATA'].apply(lambda x: city_dict.get(x, 'Foreign'))
major_sa_routes['Destination City'] = major_sa_routes['Destination IATA'].apply(lambda x: city_dict.get(x, 'Foreign'))

# count values
source_counts = major_sa_routes['Source City'].value_counts()
dest_counts = major_sa_routes['Destination City'].value_counts()
total_counts = source_counts + dest_counts
total_counts.drop('Foreign', inplace=True)

# plot bar chart
total_counts = total_counts.reset_index()
total_counts.columns = ['City', 'Count']
total_counts['Airport'] = ['OR Tambo International Airport', 'Cape Town International Airport','King Shaka International Airport', 'Port Elizabeth Airport','East London Airport', 'George Airport', 'Bram Fischer Airport','Lanseria Airport']

chart = alt.Chart(total_counts).mark_bar().encode(
    x=alt.X('City:N', axis=alt.Axis(title='City', labelAngle=0)),
    y=alt.Y('Count:Q', axis=alt.Axis(title='Count')),
    tooltip=[alt.Tooltip('City:N', title='City'), alt.Tooltip('Airport:N', title='Airport'), alt.Tooltip('Count:Q', title='Count')]
).properties(
    title='Number of airline destinations from each city',
    width=600,
    height=400
)
st.altair_chart(chart)
