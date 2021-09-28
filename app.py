
# Import dash
import dash
import dash_core_components as dcc
import dash_html_components as html
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
	html.H2('KPI Builder'),    
	html.H4('Please input target ticker, industry dropdown, and launch date.'),

	html.Div("Select the project launch date"),
	dcc.DatePickerSingle(
		id='input-date-picker',
		min_date_allowed=date(2010, 1, 1),
		max_date_allowed=date.today(),
		initial_visible_month=date.today(),
		date=date(2018, 4, 1)
	),

	# Works well enough. 2 years working ok
	html.Div("Select the time range. Please select a starting date before launch and an end date after launch. We recommend 1 year BEFORE launch and 1 year AFTER launch. Please note that selecting competitors that were not public during this entire range will result in skewed data."),
	dcc.DatePickerRange(
		id='input-date-range-picker',
		min_date_allowed=date(2000, 1, 1),
		max_date_allowed=date.today(), # in deployment, would need to make this callback to be dynamic: https://stackoverflow.com/questions/62608204/dash-datepicker-max-date-allowed-as-current-date-not-working-properly
		initial_visible_month=date(2021, 9, 1),
		clearable=True, 
		start_date=date(2017,4,1),
		end_date=date(2019,4,1)
		#calendar_orientation="vertical",
	),

	# NEED TO SWAP OUT WITH DYNAMIC PICK OF ALL S&P COs    
	# Pausing on this because a little tougher to implement search
	html.Div("This would be a dynamic search through yfinance for a ticker"),
	dcc.Input(
			id='input-yf-client-ticker', 
			type = 'search'
			# options = options,
			# value = ['SPY'], 
			# multi = True
	),	

	html.Div("Select the client"),
	dcc.Dropdown(
		id='input-client-picker',
		options=[
			{'label': 'Apple', 'value': 'AAPL'},
			{'label': 'Google', 'value': 'GOOGL'},
			{'label': 'Facebook', 'value': 'FB'},
			{'label': 'Costco', 'value': 'COST'},
			{'label': 'Shoprite', 'value': 'SRGHY'},
			{'label': 'Spartan Nash', 'value': 'SPTN'},
			{'label': 'Kroger', 'value': 'KR'},
			{'label': 'Walgreens', 'value': 'WBA'},
			{'label': 'Walmart', 'value': 'WMT'},
			{'label': 'Wegmans', 'value': 'WEGMANS'},			
			{'label': 'American Express', 'value': 'AXP'},
			{'label': 'Mastercard', 'value': 'MA'},
			{'label': 'Visa', 'value': 'V'},			
			{'label': 'Discover', 'value': 'DFS'}			
		],
		value='WMT'        
	),

	# NEED TO SWAP THIS OUT WITH DYNAMIC SEARCH OF ALL S&P COMPANIES
	html.Div("Select the subindustry competitors"),
	dcc.Dropdown(
		id='input-subindustry-picker',
		options=[
			{'label': 'Apple', 'value': 'AAPL'},
			{'label': 'Google', 'value': 'GOOGL'},
			{'label': 'Facebook', 'value': 'FB'},
			{'label': 'Costco', 'value': 'COST'},
			{'label': 'Shoprite', 'value': 'SRGHY'},
			{'label': 'Spartan Nash', 'value': 'SPTN'},
			{'label': 'Kroger', 'value': 'KR'},
			{'label': 'Walgreens', 'value': 'WBA'},
			{'label': 'Walmart', 'value': 'WMT'},
			{'label': 'Wegmans', 'value': 'WEGMANS'},
			{'label': 'American Express', 'value': 'AXP'},
			{'label': 'Mastercard', 'value': 'MA'},
			{'label': 'Visa', 'value': 'V'},
			{'label': 'Discover', 'value': 'DFS'}						
		],
		value=['COST', 'SRGHY', 'SPTN', 'KR', 'WBA'],
		multi=True
	), 

	# Add a submit button
	html.Button('Submit', id='input-submit', n_clicks=0),

	# Next step: Just add a graph or any info that displays 
	# the client's ticker info

	# Outputs - UI
	html.Div(id='output-date-picker'),
	html.Div(id='output-client-picker'),
	html.Div(id='output-date-range-picker'),
	html.Div(id='output-subindustry-picker'),
	html.Div(id='output-submit'), 
	html.Div(id='output-yf-client-ticker')	
])



# Callbacks are functions that are automatically called by Dash whenever an input component's property changes.
# Each input/ output uses it's own callback   

# Select date of launch
@app.callback(
	Output('output-date-picker', 'children'),
	Input('input-date-picker', 'date'))

def update_output(date_value):
	string_prefix = 'Date selected: '
	simple_output = ""

	if date_value is not None:
		date_object = date.fromisoformat(date_value)
		date_string = date_object.strftime('%B %d, %Y')
		string_prefix = string_prefix + date_string

	return simple_output
	


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


# Select client BUT using yfinance to look up tickers, not hardcoded 
# TBD, not in use yet
@app.callback(
	Output('output-yf-client-ticker', 'children'),
	Input('input-yf-client-ticker', 'value'))

# TBD
def update_yf_client_ticker(ticker):
	return ""
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
	Input('input-date-picker', 'date'),
	Input('input-submit', 'n_clicks'), 
	Input('input-client-picker', 'value')])

# Need to do expected input/ output audit for these functions for tests
def update_output(companies, start_date, end_date, launch_date, submitted, client):
	if submitted < 1:
		raise PreventUpdate

	all_companies = [*companies]
	all_companies.append(client)

	if start_date is not None:
		dates_data = pd.date_range(start_date, end_date, periods=8)
		# DATES_DATA IS NOT WORKING?? OR IS IT??

	# Both lines will have all companies' avg growth over time
	pre_launch_all_avgs = calc.calculate_avg_growth_over_time(all_companies, start_date, launch_date)

	# After launch date, the subindustry growth rate is different 
	post_launch_subind_avgs = calc.calculate_avg_growth_over_time(companies, launch_date, end_date)

	# we're adding client growth as a trace line over custom index
	client_post_launch_snippet = calc.calculate_avg_growth_over_time([client], launch_date, end_date)

	client_growth = [*pre_launch_all_avgs, *client_post_launch_snippet]

	all_growths = [*pre_launch_all_avgs, *post_launch_subind_avgs]

	return make_graph(dates_data, all_growths, client_growth)



# FIX SECOND TRACE LINE NOT WORKING
# Second trace line not visible for some reason?
def make_graph(dates, all_growths, client_growth):

	print("all_growths")
	print(all_growths)
	print("client_growth")
	print(client_growth)
	print("dates")
	print(dates)
	
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=dates, y=client_growth,
						mode="lines+markers",
						name='Client growth'))

	fig.add_trace(go.Scatter(x=dates, y=all_growths,
						mode="lines+markers",
						name='Custom index growth'))

	# fig.show()

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
	Input('input-date-picker', 'date'),
	Input('input-client-picker', 'value')])

def update_output(n_clicks, companies, start_date, end_date, launch_date, client):
	if companies is None or start_date is None or end_date is None or launch_date is None or client is None:
		raise PreventUpdate
	else:
		return 'Please be patient. Graph loading times vary.'




if __name__ == '__main__':
	app.run_server(debug=True)