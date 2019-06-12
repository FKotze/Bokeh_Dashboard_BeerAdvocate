# Pandas for data management
import pandas as pd

# os methods for manipulating paths
from os.path import dirname, join

# Bokeh basics 
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs


# Each tab is drawn by one script
from scripts.attention import attention_tab
from scripts.styles_table import table_tab
from scripts.gmap_map import map_tab
from scripts.ratings import ratings_tab

# Using included state data from Bokeh for map
from bokeh.sampledata.us_states import data as states

# Read data into dataframes
beers = pd.read_csv(join(dirname(__file__), 'data', 'beers.csv'), 
												index_col=0).dropna()
reviews = pd.read_csv(join(dirname(__file__), 'data', 'reviews.csv'), 
												index_col=0).dropna()
# Formatted Flight Delay Data for map
gmap_data = pd.read_csv(join(dirname(__file__), 'data', 'profiles.csv'),
												index_col=0)

# Create each of the tabs
tab4 = attention_tab(beers)
tab3 = table_tab(reviews)
tab2 = map_tab(gmap_data)
tab1 = ratings_tab(beers)

# Put all the tabs into one application
tabs = Tabs(tabs = [tab1, tab2, tab3, tab4])

# Put the tabs in the current document for display
curdoc().add_root(tabs)


