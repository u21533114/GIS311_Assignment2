#add python code here
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

"""
# Flight Data Anaylsis \U00002708
This data was aquired from [OpenFlights](https://openflights.org/data.html)
"""

airlines = pd.read_csv('airlines.dat')
airlines
airports = pd.read_csv('airports.dat')
airports
countries = pd.read_csv('countries.dat')
countries
planes = pd.read_csv('planes.dat')
planes
routes = pd.read_csv('routes.dat')
routes
