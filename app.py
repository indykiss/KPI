
# Import dash
import dash 
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
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

# Local imports
import model.calculations as calc
import dal.finance as fin


# Out of box specifications by Dash 
# Update to have McK branding at some point 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__)
server = app.server


# Layout of components 
app.layout = html.Div([

	# Inputs - UI
	html.H1('KPI Builder'),    
	html.H3('Please input target ticker, industry dropdown, and launch date.'),

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

	# Need better client / index pairings

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
	html.Button('Submit', id='input-submit', n_clicks=0),
	# Outputs - UI
	html.Div(id='output-client-picker'),
	html.Div(id='output-date-range-picker'),
	html.Div(id='output-subindustry-picker'),
	html.Div(id='output-submit')
])



# Callbacks are functions that are automatically called by Dash whenever an 
# input component's property changes.
# Each input/ output uses it's own callback   

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


# Select client we're targeting
@app.callback(
	Output('output-client-picker', 'children'), # must be children?
	Input('input-client-picker', 'value'))
 
# Keep shell, using this input elsewhere
def update_client_picker(ticker):
	ticker = ticker.upper()
	simple_output = ""
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
	Input('input-submit', 'n_clicks'), 
	Input('input-client-picker', 'value')])

# Need to do expected input/ output audit for these functions for tests
def update_output(entity, start_date, end_date, submitted, client):
	if submitted < 1:
		raise PreventUpdate
	all_companies = [*entity]
	all_companies.append(client)
	if start_date is not None:
		dates_data = pd.bdate_range(start_date, end_date)
	client_growth = calc.calculate_avg_growth(client, start_date, end_date)
	all_growths = calc.calculate_avg_growth(entity, start_date, end_date)
	return make_graph(dates_data, all_growths, client_growth, client, entity)

def make_graph(dates, entity_growth, client_growth, client, entity):
	# Dates is including holidays but yf doesn't
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


# Submit button loads graph
@app.callback(
    Output('output-submit', 'children'),
	[Input('input-submit', 'n_clicks'), 
	Input('input-subindustry-picker', 'value'), 
	Input('input-date-range-picker', 'start_date'), 
	Input('input-date-range-picker', 'end_date'),
	Input('input-client-picker', 'value')])

def update_output(n_clicks, companies, start_date, end_date, client):
	if companies is None or start_date is None or end_date is None or client is None:
		raise PreventUpdate
	else:
		return 'Please be patient. Graph loading times vary.'



if __name__ == '__main__':
    app.run_server(debug=True)
