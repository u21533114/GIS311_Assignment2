#add python code here
#from collections import namedtuple
#import altair as alt
import math
import pandas as pd
import streamlit as st
import numpy as np
#airlines is a table
#airports has co-ordinates
#countries is a table
#planes is a table
#routes is weird

"""
# Flight Data Anaylsis \U00002708
This data was aquired from [OpenFlights](https://openflights.org/data.html)
"""

t = pd.read_csv('airlines.dat')
t
r = pd.read_csv('airports.dat')
r
q = pd.read_csv('countries.dat')
q
w = pd.read_csv('planes.dat')
w
e = pd.read_csv('routes.dat')
e
