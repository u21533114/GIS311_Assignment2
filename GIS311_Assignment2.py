import math
import pandas as pd
import streamlit as st
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import altair as alt
import folium
from streamlit_folium import folium_static
#NB: 1 map and two charts are needed

st.write('# South African flight data analysis')
st.write('This data was acquired from [OpenFlights](https://openflights.org/data.html)')
st.write('Should Lanseria Airport focus on its expansion plans?')
st.write('____________________________________________________________________________')
st.write('## Major airports in South Africa')


#import data
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

#create map
def create_map():
    map_sa = folium.Map(location=[-28.4793, 24.6727], zoom_start=5)
    for i, row in pnt.iterrows():
        folium.Marker(location=[row['Latitude'], row['Longitude']], tooltip=row['Name']).add_to(map_sa)
    return map_sa
map_sa = create_map()
folium_static(map_sa)

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

# make cities selectable
city_options = ['All'] + list(total_counts['City'])
selected_cities = st.multiselect('Filter cities', city_options, default=['All'])

if 'All' in selected_cities:
    chart_data = total_counts
else:
    chart_data = total_counts[total_counts['City'].isin(selected_cities)]

chart = alt.Chart(chart_data).mark_bar().encode(
    x=alt.X('City:N', axis=alt.Axis(title='City', labelAngle=0)),
    y=alt.Y('Count:Q', axis=alt.Axis(title='Count')),
    tooltip=[alt.Tooltip('City:N', title='City'), alt.Tooltip('Airport:N', title='Airport'), alt.Tooltip('Count:Q', title='Count')]
).properties(
    title='Number of airline destinations from each city',
    width=600,
    height=400
)
st.altair_chart(chart)

#map cities to provinces
province_dict = {
    'Johannesburg': 'Gauteng',
    'Lanseria': 'Gauteng',
    'Durban': 'Kwa-Zulu Natal',
    'Port Elizabeth': 'Eastern Cape',
    'East London': 'Eastern Cape',
    'Cape Town': 'Western Cape',
    'Bloemfontein': 'Free State',
    'George': 'Western Cape'
}

#create list of provinces for each city
provinces = [province_dict.get(city, 'Unknown') for city in total_counts['City']]

#add the 'province' column to the dataframe
total_counts['Province'] = provinces

#group the total_counts dataframe by province and sum the counts
province_counts = total_counts.groupby('Province')['Count'].sum().reset_index()
province_counts = province_counts.sort_values('Count', ascending=False)
province_counts['Percentage'] = round(province_counts['Count']/province_counts['Count'].sum()*100, 2)

#create pie chart with altair
pie_chart = alt.Chart(province_counts).mark_arc().encode(
    theta='Percentage:Q',
    color=alt.Color('Province:N', legend=alt.Legend(title='Provinces'), sort=alt.EncodingSortField(field='Count', op='sum', order='descending')),
    tooltip=['Province:N', 'Percentage:Q']
).properties(
    width=600,
    height=400,
    title={
        'text': 'Total routes by province',
        'subtitle': 'Distribution of airline routes by province',
        'fontSize': 22,
        'subtitleFontSize': 16,
        'subtitleColor': 'gray'
    }
)

#display pie chart in Streamlit
st.altair_chart(pie_chart)

#explain Lanseria
text = """
As can be seen in the pie chart, Gauteng makes up over 65% of all airline routes available in South Africa.
The vast majority of these routes are provided by the OR Tambo International Airport,
with only a small number of routes available from Lanseria Airport - which is planning to reach 40 million passengers by 2050 (Lanseria, 2023).
With such a high volume of routes coming from Gauteng,
it makes sense for these routes to be distributed more evenly between OR Tambo International Airport and Lanseria Airport.
_________________________________________________________________________________________________________________________
"""
st.markdown(text)
st.write('Reference: (Lanseria, 2023) accessed from https://lanseria.co.za/corporate/airport-development/ on 15/04/2023')
st.write('Created by Brett Harzon (u21533114) for GIS 311 at the University of Pretoria.')
