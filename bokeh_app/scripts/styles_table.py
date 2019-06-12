# pandas and numpy for data manipulation
import pandas as pd
import numpy as np

from bokeh.models import ColumnDataSource, Panel
from bokeh.models.widgets import TableColumn, DataTable

def table_tab(reviews):

	# create new empty dataset to fill the information for Top Genre
	tg = pd.DataFrame()

	# get a list of allt he genres to enter to dataframe
	glist = list(set(reviews['style_genre']))
	tg['style_genre'] = glist

	# get total reviews by genre
	reviews.loc[:,'count'] = 1
	gr = reviews.groupby('style_genre', as_index=False)
	reviews_cnt = gr.aggregate(np.sum)
	gr = reviews.groupby('style_genre', as_index=False)['score']
	ss = gr.aggregate(np.mean)

	# add number of reviews by genre to tg dataframe

	tg = pd.merge(tg, reviews_cnt, on='style_genre')
	tg = tg.drop(['profile','beer','score','ratings','style'], axis=1)

	tg = pd.merge(tg, ss, on='style_genre' )

	beers = pd.read_csv('bokeh_app/data/beers.csv')
	tb = beers.sort_values(
		['style_genre', 'ratings'], 
		ascending=[True, False]).drop_duplicates(['style_genre']).reset_index(drop=True)

	tg = pd.merge(tg, tb, on='style_genre')
	tg= tg.drop(['place','beer','style'], axis=1 )

	tg= tg.rename(columns={'style_genre':'s_genre'})

	tg['score_x'] = tg['score_x'].round(2)

	tg =tg.sort_values(['count'], ascending=[False])


	# bokeh for styles table
	genre_src = ColumnDataSource(tg)

	table_columns = [
	TableColumn(field='s_genre', title='Most Popular Genre'),
	TableColumn(field='count', title='Number of Reviews in Genre'),
	TableColumn(field='score_x', title='Average Genre Score'),
	TableColumn(field='style_name', title='Top Style in Genre'),
	TableColumn(field='name', title='Most Popular Beer'),
	TableColumn(field='score_y', title='Beer Rating')
	]

	genre_table = DataTable(source=genre_src, 
		columns=table_columns, width=800, height=580)

	tab = Panel(child = genre_table, title = 'Beer Genre Summary')

	return tab