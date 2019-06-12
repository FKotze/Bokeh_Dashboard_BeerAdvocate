# pandas and numpy for data manipulation
import pandas as pd
import numpy as np

from bokeh.plotting import figure, gmap
from bokeh.models import (CategoricalColorMapper, HoverTool, 
						  ColumnDataSource, Panel, 
						  FuncTickFormatter, SingleIntervalTicker, 
						  LinearAxis, GMapOptions,
						  OpenURL, TapTool)
from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider, 
								  Tabs, CheckboxButtonGroup, 
								  TableColumn, DataTable, Select, Div
								  )
from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16

def map_tab(gmap_data):

	# rememove duplicate beers and styles for each profile
	gmap_data = gmap_data.drop_duplicates(['profile']).reset_index(drop=True)


	map_options = GMapOptions(lat=54.204997, lng=-4.540580, map_type="roadmap", zoom=6)
	# For GMaps to function, Google requires you obtain and enable an API key:
	#
	#     https://developers.google.com/maps/documentation/javascript/get-api-key
	#
	# Replace the value below with your personal API key:

	p = gmap("PERSONAL API KEY HERE", 
		map_options, title="Places in the United Kingdom", plot_width=700, 
		plot_height=650, tools=['wheel_zoom','tap','lasso_select','pan']
		)

	src = ColumnDataSource(data=dict(
		latitude = gmap_data['latitude'].tolist(),
		longitude = gmap_data['longitude'].tolist(),
		postcode = gmap_data['zip_code'].tolist(),
		phone = gmap_data['phone'].tolist(),
		placeid = gmap_data['profile'].tolist(),
		topbeer = gmap_data['name'].tolist(),
		beerstyle = gmap_data['style_name'].tolist(),
		genre = gmap_data['style_genre'].tolist()
		)
	)

	TOOLTIPS = [
	("Place ID", "@placeid"),
	("Phone", "@phone"),
	("Postcode", "@postcode"),
	('Top Beer','@topbeer'),
	('Beer Style','@beerstyle'),
	('Genre', '@genre')
	]

	p.circle(x="longitude", 
		y="latitude", 
		size=5, fill_color="orange", 
		fill_alpha=0.8, source=src,
		)

	p.add_tools(HoverTool(tooltips=TOOLTIPS))

	#create style function to use - use p_style as style is referenced in data
	def p_style(p):
		# Title 
		p.title.align = 'center'
		p.title.text_font_size = '20pt'
		p.title.text_font = 'serif'

		# Axis titles
		p.xaxis.axis_label_text_font_size = '14pt'
		p.xaxis.axis_label_text_font_style = 'bold'
		p.yaxis.axis_label_text_font_size = '14pt'
		p.yaxis.axis_label_text_font_style = 'bold'

		# Tick labels
		p.xaxis.major_label_text_font_size = '12pt'
		p.yaxis.major_label_text_font_size = '12pt'

		p.axis.visible = False

		return p
	
	# add url for the beer to open a new page of that beer 'tapped'
	beerurl = "https://www.beeradvocate.com/beer/profile/@placeid/"
	taptool = p.select(type=TapTool)
	taptool.callback = OpenURL(url=beerurl)
	
	# text help user use tools
	sidetext = Div(
		text="""Please use the tools to the right to adjust the <b>Map of Places</b> as needed.
		There is a zoom and drag funtion.
		If you would like to visit a Place page on BA please click on any point.
		""",
		width=200, height=200)

	#apply the style defined to the plot
	p = p_style(p)

	# Layout setup
	layout = row(sidetext, p)
	tab = Panel(child = layout, title = 'UK Map of Places')

	return tab