# pandas and numpy for data manipulation
import pandas as pd
import numpy as np

from scipy.stats import gaussian_kde

from bokeh.plotting import figure
from bokeh.models import (CategoricalColorMapper, HoverTool, 
						  ColumnDataSource, Panel, 
						  FuncTickFormatter, SingleIntervalTicker, LinearAxis)
from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider, 
								  Tabs, CheckboxButtonGroup, 
								  TableColumn, DataTable, Select, Div)
from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import Category20_16

def attention_tab(beers):
	
	# Dataset for density plot based on Genres and range of ratings
	# and bandwidth for density estimation
	def make_dataset(
		genre_list, 
		range_start, 
		range_end, 
		bandwidth
		):

		xs = []
		ys = []
		colors = []
		labels = []

		for i, genre in enumerate(genre_list):
			subset = beers[beers['style_genre'] == genre]
			subset = subset[subset['ratings'].between(range_start, 
														range_end)]

			kde = gaussian_kde(subset['ratings'], bw_method=bandwidth)
			
			# Evenly space x values
			x = np.linspace(range_start, range_end, 6500)
			# Evaluate pdf at every value of x
			y = kde.pdf(x)

			# Append the values to plot
			xs.append(list(x))
			ys.append(list(y))

			# Append the colors and label
			colors.append(genre_colors[i])
			labels.append(genre)

		new_src = ColumnDataSource(data={'x': xs, 'y': ys, 
								   'color': colors, 'label': labels})

		return new_src

	def make_plot(src):
		p = figure(plot_width = 700, plot_height = 650,
				   title = 'Distribution of Beer Genre Attention',
				   x_axis_label = 'Attention of Genre (Number of Ratings of Beer)', y_axis_label = 'Density')


		p.multi_line('x', 'y', color = 'color', legend = 'label', 
					 line_width = 3,
					 source = src)

		# Hover tool with next line policy
		hover = HoverTool(tooltips=[('Genre', '@label'), 
									('Ratings', '$x'),
									('Density', '$y')],
						  line_policy = 'next')

		# Add the hover tool and styling
		p.add_tools(hover)

		p = p_style(p)

		return p
	
	def update(attr, old, new):
		# List of genres to plot
		genres_to_plot = [genre_selection.labels[i] for i in 
							genre_selection.active]
		
		# If no bandwidth is selected, use the default value
		if bandwidth_choose.active == []:
			bandwidth = None
		# If the bandwidth select is activated, use the specified bandwith
		else:
			bandwidth = bandwidth_select.value
			
		
		new_src = make_dataset(genres_to_plot,
									range_start = range_select.value[0],
									range_end = range_select.value[1],
									bandwidth = bandwidth)
		
		src.data.update(new_src.data)
		
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
	
	# genres and colors
	available_genres = list(set(beers['style_genre']))
	available_genres.sort()

	genre_colors = Category20_16
	genre_colors.sort()

	# Genres to plot
	genre_selection = CheckboxGroup(labels=available_genres, 
									   active = [0, 1])
	genre_selection.on_change('active', update)
	
	range_select = RangeSlider(start = 0, end = 500, value = (0, 200),
							   step = 50, title = 'Range of Attention (Number of Ratings)')
	range_select.on_change('value', update)
	
	# intial genres and data source
	initial_genres = [genre_selection.labels[i] for 
						i in genre_selection.active]
	
	# Bandwidth of kernel
	bandwidth_select = Slider(start = 0.1, end = 5, 
							  step = 0.1, value = 2,
							  title = 'Bandwidth for Density Plot')
	bandwidth_select.on_change('value', update)
	
	# Whether to set the bandwidth or have it done automatically
	bandwidth_choose = CheckboxButtonGroup(
		labels=['Choose Bandwidth (Else Auto)'], active = [])
	bandwidth_choose.on_change('active', update)

	# Make the density data source
	src = make_dataset(initial_genres, 
						range_start = range_select.value[0],
						range_end = range_select.value[1],
						bandwidth = bandwidth_select.value) 
	
	sidetext = Div(
		text="""Please use the filters below to adjust the <b>Attention Density Plot</b> as needed.""",
		width=250, height=50)

	# Make the density plot
	p = make_plot(src)
	
	# Add style to the plot
	p = p_style(p)
	
	# Put controls in a single element
	controls = WidgetBox(sidetext, genre_selection, range_select, 
						 bandwidth_select, bandwidth_choose)
	
	# Create a row layout
	layout = row(controls, p)
	
	# Make a tab with the layout 
	tab = Panel(child=layout, title = 'Distribution of Beer Genre Attention')

	return tab