#from collections import namedtuple
#import altair as alt
import math
import pandas as pd
import streamlit as st
import numpy as np
#airlines is a table
#airports has co-ordinates and no header row
#countries is a table
#planes is a table with no header row
#routes is weird and has no header row
#NB: 1 map and two charts are needed
pip install --upgrade streamlit
st.markdown(
    """
    <style>
    .reportview-container {
        padding-top: 0px;
        padding-bottom: 0px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.write('<style>body { background-color: red; }</style>', unsafe_allow_html=True)


"""
# Flight Data Anaylsis \U00002708
This data was aquired from [OpenFlights](https://openflights.org/data.html)
"""

airlines = pd.read_csv('airlines.dat', header = None)
airlines
airports = pd.read_csv('airports.dat', header = None)
airports
countries = pd.read_csv('countries.dat', header = None)
countries
planes = pd.read_csv('planes.dat', header = None)
planes
routes = pd.read_csv('routes.dat', header = None)
routes
