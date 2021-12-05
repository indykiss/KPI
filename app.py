
# Import dash
import dash

# Fix this issue? IDK. ImportError in Heroku logs
# Auto-deploy not working
# import dash_core_components as dcc
# import dash_html_components as html
# from dash import dcc
# from dash import html

import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output # So I can simplify callback
from dash.exceptions import PreventUpdate

# Import plotly 
import plotly 
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Import pandas
import pandas as pd

# Import misc - maybe delete some
import re
import os
# import holidays
from datetime import date, datetime, timedelta

# Import functions from my code 
import model.calculations as calc
import dal.finance as fin
from helpers import make_table, make_card, ticker_inputs, make_item  #maybe delete


# Out of box specifications by Dash 
# Update to have McK branding at some point 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

# Layout of components 
app.layout = html.Div([

	# Inputs - UI
	html.H1('KPI Builder'),    
	html.H3('Please input target ticker, industry dropdown, and launch date.'),

	# Feature extension -- client launch date
	# Adds a dot to the screen and changes graph mathmatically
	# html.Div("Select the project launch date"),
	# dcc.DatePickerSingle(
	# 	id='input-date-picker',
	# 	min_date_allowed=date(2010, 1, 1),
	# 	max_date_allowed=date.today(),
	# 	initial_visible_month=date.today(),
	# 	date=date(2019, 1, 1)
	# ),

	# Works well enough. 2 years working ok
	html.H4("Select the time range. Please note that selecting competitors that were not public during this entire range will result in skewed data."),
	dcc.DatePickerRange(
		id='input-date-range-picker',
		min_date_allowed=date(2000, 1, 1),
		max_date_allowed=date.today(), # in deployment, would need to make this callback to be dynamic: https://stackoverflow.com/questions/62608204/dash-datepicker-max-date-allowed-as-current-date-not-working-properly
		initial_visible_month=date(2021, 9, 1),
		clearable=True, 
		start_date=date(2020,1,1),
		end_date=date(2021,1,1)
		#calendar_orientation="vertical",
	),

	# NEED TO SWAP OUT WITH DYNAMIC PICK OF ALL S&P COs    
	# Pausing on this because a little tougher to implement search
	# Extension -- ticker lookup with API
	# html.Div("This would be a dynamic search through yfinance for a ticker"),
	# dcc.Input(
	# 		id='input-yf-client-ticker', 
	# 		type = 'search'
	# 		# options = options,
	# 		# value = ['SPY'], 
	# 		# multi = True
	# ),	

	# Rethink entire strategy? 
	# Custom index is tough. Maybe ETF would be good
	# Need to look at S&P's charting 
	# Maybe instead of doing growth day over day, which is wildly up and down, 
	# we should do overall growth from start to end? 

	html.H4("Select a client"),
	dcc.Dropdown(
		id='input-client-picker',
		options=[
			# not a great first 2
			{'label': 'Airbus', 'value': 'EADSY'},
			{'label': 'Roche', 'value': 'RHHBY'},			
			{'label': 'Fluor', 'value': 'FLR'},			
			{'label': 'Amazon', 'value': 'AMZN'},			
			{'label': 'Bank of America', 'value': 'BAC'}, 	
			{'label': 'CVS', 'value': 'CVS'},
			{'label': 'BlackRock', 'value': 'BLK'},
			{'label': 'Raytheon', 'value': 'RTX'},
			{'label': 'UnitedHealth', 'value': 'UNH'},
			{'label': 'Booking.com', 'value': 'BKNG'},
			{'label': 'Netflix', 'value': 'NFLX'},
			{'label': 'Chevron', 'value': 'CVX'},
			{'label': 'Johnson & Johnson', 'value': 'JNJ'},
			{'label': 'Coldwell', 'value': 'RLGY'},
			{'label': 'Tesla', 'value': 'TSLA'},
			{'label': 'McDonalds', 'value': 'MCD'},
			{'label': 'Walmart', 'value': 'WMT'},
			{'label': 'Facebook', 'value': 'FB'},
			{'label': 'Apple', 'value': 'AAPL'},
			{'label': 'AT&T', 'value': 'T'},
			{'label': 'West Fraser Timber', 'value': 'WFG'},
			{'label': 'UPS', 'value': 'UPS'},		
		],
		value='EADSY'        
	),

	html.H4("Select the sector ETF"),
	dcc.Dropdown(
		id='input-subindustry-picker',
		options=[
			{'label': 'Aerospace & Defence', 'value': 'ITA'},
			{'label': 'Biotechnology', 'value': 'IBB'},			
			{'label': 'Construction & Engineering', 'value': 'PKB'},			
			{'label': 'Consumer discretionary', 'value': 'VCR'},			
			{'label': 'Financial Services', 'value': 'XLF'}, 	
			{'label': 'Healthcare', 'value': 'XLV'},
			{'label': 'Hedge Funds', 'value': 'QAI'},
			{'label': 'Industrials', 'value': 'XLI'},
			{'label': 'Insurance', 'value': 'KIE'},
			{'label': 'Leisure & recreation', 'value': 'PEJ'},
			{'label': 'Media & Publishing', 'value': 'PBS'},
			{'label': 'Oil & Gas', 'value': 'USO'},
			{'label': 'Pharmaceuticals', 'value': 'PJP'},
			{'label': 'Real Estate', 'value': 'VNQ'},
			{'label': 'Renewable energy', 'value': 'ICLN'},
			{'label': 'Restaurants & bars', 'value': 'EATZ'},
			{'label': 'Retail', 'value': 'XRT'},
			{'label': 'Software', 'value': 'SKYY'},
			{'label': 'Technology', 'value': 'VGT'},
			{'label': 'Telecommunications', 'value': 'FCOM'},
			{'label': 'Timber', 'value': 'WOOD'},
			{'label': 'Transportation', 'value': 'IYT'},
			{'label': 'QQQ', 'value': 'QQQ'}
		],
		value=['ITA'],
		multi=False
	), 

	# Add a submit button
	html.Button('Submit', id='input-submit', n_clicks=0),

	# Extension: Add a graph or any info that displays client's ticker info

	# Outputs - UI
	# html.Div(id='output-date-picker'), # Extension -- project launch date
	html.Div(id='output-client-picker'),
	html.Div(id='output-date-range-picker'),
	html.Div(id='output-subindustry-picker'),
	html.Div(id='output-submit')
	# html.Div(id='output-yf-client-ticker') # Extension -- ticker lookup	
])



# Callbacks are functions that are automatically called by Dash whenever an input component's property changes.
# Each input/ output uses it's own callback   

# Select date of launch
# Extension -- project launch date 
# @app.callback(
# 	Output('output-date-picker', 'children'),
# 	Input('input-date-picker', 'date'))

# def update_output(date_value):
# 	string_prefix = 'Date selected: '
# 	simple_output = ""
# 	if date_value is not None:
# 		date_object = date.fromisoformat(date_value)
# 		date_string = date_object.strftime('%B %d, %Y')
# 		string_prefix = string_prefix + date_string
# 	return simple_output
	


# Select the time frame 
@app.callback(
	Output('output-date-range-picker', 'children'),
	[Input('input-date-range-picker', 'start_date'),
	Input('input-date-range-picker', 'end_date')])

def update_output(start_date, end_date):
	string_prefix = 'You have selected: '
	simple_output = ""

	if start_date is not None:
		start_date_object = date.fromisoformat(start_date)
		start_date_string = start_date_object.strftime('%B %d, %Y')
		string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
	if end_date is not None:
		end_date_object = date.fromisoformat(end_date)
		end_date_string = end_date_object.strftime('%B %d, %Y')
		string_prefix = string_prefix + 'End Date: ' + end_date_string
	if len(string_prefix) == len('You have selected: '):
		return 'Select a date to see it displayed here'
	else:
		return simple_output


# Extension - ticker lookup
# Select client BUT using yfinance to look up tickers, not hardcoded 
# TBD, not in use yet
# @app.callback(
# 	Output('output-yf-client-ticker', 'children'),
# 	Input('input-yf-client-ticker', 'value'))

# def update_yf_client_ticker(ticker):
# 	return ""
	# string_answer = 'You have selected: '

	# # if input is accurate ticker
	# if ticker is not None: # switch for is a ticker
	# 	string_answer = string_answer + ticker
	# else:
	# 	string_answer = 'This is not a valid ticker. Try again.'

	# return string_answer


# Select client we're targeting
@app.callback(
	Output('output-client-picker', 'children'), # must be children?
	Input('input-client-picker', 'value'))
 
# Takes the client_name input and outputs info about  stock
# Connect the yfinance API here 
def update_client_picker(ticker):
	ticker = ticker.upper()
	TICKER = fin.get_ticker(ticker)
	simple_output = ""
		
	cards = [ 
	dbc.Col(make_card("Client selected:", "secondary", TICKER.info['shortName'])),
	dbc.Col(make_card("Open", "secondary", TICKER.info['open']))
	]

	return simple_output


# Select the custom index competitors
# 1. Grab each one's stock price data from start to end date
# 2. Calculates stock price growth for each company over time
# 3. Calculates average growth for the custom index

# Confirmed that all math works in gsheet with manual data from yahoo finance: 
# https://docs.google.com/spreadsheets/d/1yQ6AgjBPN3EHST2TDfmaRXgS0VVP54qXQwhmxpw18Fs/edit#gid=0 
@app.callback(
	Output('output-subindustry-picker', 'children'),
	[Input('input-subindustry-picker', 'value'), 
	Input('input-date-range-picker', 'start_date'), 
	Input('input-date-range-picker', 'end_date'),
	# Input('input-date-picker', 'date'), # Extension - project launch date
	# IF I add back, need to add launch_date in parameter like:
	# def update_output(entity, start_date, end_date, launch_date, submitted, client):
	Input('input-submit', 'n_clicks'), 
	Input('input-client-picker', 'value')])

# Need to do expected input/ output audit for these functions for tests
def update_output(entity, start_date, end_date, submitted, client):
	if submitted < 1:
		raise PreventUpdate

	all_companies = [*entity]
	all_companies.append(client)

	start_date_object = date.fromisoformat(start_date)

	if start_date is not None:
		dates_data = pd.bdate_range(start_date, end_date)

	client_growth = calc.calculate_avg_growth_alt(client, start_date, end_date)
	all_growths = calc.calculate_avg_growth_alt(entity, start_date, end_date)

	return make_graph(dates_data, all_growths, client_growth, client, entity)

	# Extension -- IF using launch_date for project launch. 
	# Not working perfectly, but essentially: 
		# Both lines will have all companies' avg growth over time
	# pre_launch_all_avgs = calc.calculate_avg_growth_over_time(all_companies, start_date, launch_date)
		# After launch date, the subindustry growth rate is different 
	# post_launch_subind_avgs = calc.calculate_avg_growth_over_time(companies, launch_date, end_date)
		# We're adding client growth as a trace line over custom index
	# client_post_launch_snippet = calc.calculate_avg_growth_over_time([client], launch_date, end_date)
	# client_growth = [*pre_launch_all_avgs, *client_post_launch_snippet]
	# all_growths = [*pre_launch_all_avgs, *post_launch_subind_avgs]



def make_graph(dates, entity_growth, client_growth, client, entity):
	# Dates is including holidays but yf doesn't
	# So if there are issues, that might be the reason 
	
	client_name = fin.get_name_from_ticker(client)
	entity_name = fin.get_name_from_ticker(entity)

	fig = go.Figure()

	fig.add_trace(go.Scatter(x=dates, y=client_growth,
						mode="lines",
						name=client_name,
						line_shape='spline'))

	fig.add_trace(go.Scatter(x=dates, y=entity_growth,
						mode="lines",
						name=entity_name,
						line_shape='spline'))

	newGraph = html.Div(dcc.Graph(
		id='output-subindustry-picker',
		figure=fig
	))	

	return newGraph



# Hit submit button to load graph
@app.callback(
    Output('output-submit', 'children'),
	[Input('input-submit', 'n_clicks'), 
	Input('input-subindustry-picker', 'value'), 
	Input('input-date-range-picker', 'start_date'), 
	Input('input-date-range-picker', 'end_date'),
	# Input('input-date-picker', 'date'), # Extension for client launch
	# IF I add back, need to add launch_date in parameter like:
	# def update_output(n_clicks, companies, start_date, end_date, launch_date, client):
	Input('input-client-picker', 'value')])

def update_output(n_clicks, companies, start_date, end_date, client):
	if companies is None or start_date is None or end_date is None or client is None:
		raise PreventUpdate
	else:
		return 'Please be patient. Graph loading times vary.'




if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run_server(host="0.0.0.0", port=port)	
	# app.run_server(debug=True)


# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host="0.0.0.0", port=port)