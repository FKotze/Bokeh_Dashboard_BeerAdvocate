# pandas and numpy for data manipulation
import pandas as pd
import numpy as np

from bokeh.plotting import figure

from bokeh.models import (CategoricalColorMapper, HoverTool, 
						  ColumnDataSource, Panel, 
						  FuncTickFormatter, SingleIntervalTicker, 
						  LinearAxis, BoxAnnotation,
						  Legend, LegendItem,
						  OpenURL, TapTool)

from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider, 
								  Tabs, CheckboxButtonGroup, 
								  TableColumn, DataTable, Select, Div)

from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16, RdYlGn


def ratings_tab(beers):
	
	#set colors based on where a beer is a hidden gem (purple) if not then (blue)
	beers["color"] = np.where((beers["ratings"] < 200) & (beers["score"] >4.0), "#9467bd" , "#3182bd")
	# make beers with less than 10 reviews fainter
	beers["alpha"] = np.where(beers["ratings"] > 10, 1, 0.5)

	# use BA quality scale to create background colour gradient from word class to awful
	#worldclass = BoxAnnotation(bottom=4.5, top=5.0, fill_color='#1a9850', fill_alpha=0.2)
	#outstanding = BoxAnnotation(bottom=4.0, top=4.5, fill_color='#91cf60', fill_alpha=0.2)
	#good = BoxAnnotation(bottom=3.5, top=4, fill_color='#d9ef8b', fill_alpha=0.2)	
	#okay = BoxAnnotation(bottom=3.0, top=3.5, fill_color='#fee08b', fill_alpha=0.2)
	#poor = BoxAnnotation(bottom=2, top=3, fill_color='#fc8d59', fill_alpha=0.2)
	#awful = BoxAnnotation(bottom=0, top=2, fill_color='#d73027', fill_alpha=0.2)

	worldclass = BoxAnnotation(left=4.5, right=5.0, fill_color='#1a9850', fill_alpha=0.2)
	outstanding = BoxAnnotation(left=4.0, right=4.5, fill_color='#91cf60', fill_alpha=0.2)
	good = BoxAnnotation(left=3.5, right=4, fill_color='#d9ef8b', fill_alpha=0.2)	
	okay = BoxAnnotation(left=3.0, right=3.5, fill_color='#fee08b', fill_alpha=0.2)
	poor = BoxAnnotation(left=2, right=3, fill_color='#fc8d59', fill_alpha=0.2)
	awful = BoxAnnotation(left=0, right=2, fill_color='#d73027', fill_alpha=0.2)

	# as data currently has no name for each place, create a new column in dataframe
	# for the place id as a string - can be replaced with actual name in future
	beers['place_name'] = beers['place'].astype(str)

	# create list for selection drop downs including an all selection option
	style_genres = list(sorted(set(beers['style_genre'])))
	style_names = list(sorted(set(beers['style_name'])))
	place_names = list(sorted(set(beers['place_name'])))
	a_ll = ['All']
	genres = a_ll + style_genres
	styles = a_ll + style_names
	places = a_ll + place_names

	# create the map for axis
	axis_map = {
			'Total Number of Ratings': 'ratings',
			'Average Score': 'score',
			}

	# create input controls
	ratings = Slider(title="Minimum number of ratings", value=150, start=0, end=7000, step=25)
	score = Slider(title="Minimum score of beers", start=0, end=5, value=2.5, step=0.5)
	genre = Select(title="Genre", value="All", options=genres)
	style = Select(title="Style", value="All", options=styles)
	place = Select(title="Place", value="All", options=places)
	sidetext = Div(
		text="""Please use the filters below to adjust the <b>Beer Performance Portfolio</b> as needed.
		If no beers are visibile please reduce the minimum number of beers filter.
		Purple dots are identified as <b>'hidden gems'</b>. 
		Background colour based on BA beer <a href="https://www.beeradvocate.com/community/threads/beeradvocate-ratings-explained.184726/">quality indicator</a>.
		If you would like to visit the specific beer webpage on BA please click on the dot. """,
		width=250, height=150)

	# define the axis
	x_axis = Select(title="X Axis", options=sorted(axis_map.keys()), value="Average Score")
	y_axis = Select(title="Y Axis", options=sorted(axis_map.keys()), value="Total Number of Ratings")

	#create source from the columndatasource for bokeh
	source = ColumnDataSource(data=dict(x=[], y=[], color=[], beer=[], genre=[], style=[], place=[], alpha=[], beerid=[]))

	#define what will be shown when hovering over a point in the scatter
	TOOLTIPS=[
	("Beer", "@beer"),
	("Score of Beer", "@score"),
	("Beer Style", "@style"),
	("Beer Genre", "@genre")
	]

	# creatte the figure and type of scatter
	p = figure(plot_height=650, plot_width=700, title="", toolbar_location='right', tools=['wheel_zoom','tap','lasso_select','pan'], tooltips=TOOLTIPS)
	p.circle(x="x", y="y", source=source, size=9, color="color", line_color=None, fill_alpha="alpha")

	# add the background color to plot to identify the beer on the BA quality scale
	p.add_layout(worldclass)
	p.add_layout(outstanding)
	p.add_layout(good)
	p.add_layout(okay)
	p.add_layout(poor)
	p.add_layout(awful)
	
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

		return p

	#create function to change the plot depending on what the users filters
	def select_beers():
		genre_val = genre.value
		style_val = style.value
		place_val = place.value

		selected = beers[
		(beers.ratings >= ratings.value) &
		(beers.score >= score.value)
		]
		if (genre_val != "All"):
			selected = selected[selected.style_genre.str.contains(genre_val)==True]
		if (style_val != "All"):
			selected = selected[selected.style_name.str.contains(style_val)==True]
		if (place_val != "All"):
			selected = selected[selected.place_name.str.contains(place_val)==True]

		return selected

	# how to update the plot when a filter is chosen
	def update():
		df = select_beers()
		x_name = axis_map[x_axis.value]
		y_name = axis_map[y_axis.value]

		p.xaxis.axis_label = x_axis.value
		p.yaxis.axis_label = y_axis.value
		p.title.text = "Beer Performance Portfolio (%d Beers Selected)" % len(df)
		source.data = dict(
			x=df[x_name],
			y=df[y_name],
			color=df["color"],
			beer=df["name"],
			beerid=df["beer"],
			style=df["style_name"],
			genre=df["style_genre"],
			place=df["place_name"],
			alpha=df["alpha"],
			score=df["score"],
			)

	# define the filter controls and how to change when selected
	controls = [score, ratings, genre, style, place]
	for control in controls:
		control.on_change('value', lambda attr, old, new: update())

	# fix the scale_width
	sizing_mode = 'fixed'  

	#definte the layout and aspects to include in plot
	inputs = WidgetBox(sidetext, *controls, sizing_mode=sizing_mode)
	layout = row(inputs, p)

	# initial load of the data
	update()

	#apply the style defined to the plot
	p = p_style(p)

	# add url for the beer to open a new page of that beer 'tapped'
	beerurl = "https://www.beeradvocate.com/beer/profile/@place/@beerid/"
	taptool = p.select(type=TapTool)
	taptool.callback = OpenURL(url=beerurl)

	tab = Panel(child = layout, title = 'Beer Performance Portolfio')

	return tab