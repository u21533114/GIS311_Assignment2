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
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
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

