
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from dash.dependencies import Input, Output # So I can simplify callback
import plotly 
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas
import re
import yfinance as yf
from datetime import date, datetime, timedelta
from helpers import make_table, make_card, ticker_inputs, make_item


# Basically index.py

# Out of box specifications by Dash 
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
        date=date(2021, 8, 1)
    ),

	html.Div("Select the time range. Please select a starting date before launch and an end date after launch. We recommend 1 year BEFORE launch and 1 year AFTER launch. Please note that selecting competitors that were not public during this entire range will result in skewed data."),
    dcc.DatePickerRange(
        id='input-date-range-picker',
        min_date_allowed=date(2000, 1, 1),
        max_date_allowed=date.today(),
        initial_visible_month=date(2021, 8, 5),
        end_date=date(2021, 8, 25)
    ),

	# NEED TO SWAP OUT WITH DYNAMIC PICK OF ALL S&P COs    
    html.Div("Select the client"),
    dcc.Dropdown(
        id='input-client-picker',
        options=[
            {'label': 'Apple', 'value': 'AAPL'},
            {'label': 'Google', 'value': 'GOOGL'},
            {'label': 'Facebook', 'value': 'FB'}
        ],
        value='AAPL'        
    ),

	# NEED TO SWAP THIS OUT WITH DYNAMIC SEARCH OF ALL S&P COMPANIES
	html.Div("Select the subindustry competitors"),
	dcc.Dropdown(
		id='input-subindustry-picker',
		options=[
			{'label': 'Apple', 'value': 'AAPL'},
			{'label': 'Google', 'value': 'GOOGL'},
			{'label': 'Facebook', 'value': 'FB'}, 
			{'label': 'Amazon', 'value': 'AMZN'}			
		],
		value=['GOOGL', 'FB'],
		multi=True
	), 

    # Next step: Just add a graph or any info that displays 
    # the client's ticker info

    # Outputs - UI
    html.Div(id='output-date-picker'),
    html.Div(id='output-client-picker'),
	html.Div(id='output-date-range-picker'),
	html.Div(id='output-subindustry-picker')


# IDK, copied and pasted
	# html.Div([
	# dbc.Row([dbc.Col(make_card("Enter Ticker", "success", ticker_inputs('ticker-input', 'date-picker', 36)))]) #row 1
    
	# # Should be chart at some point in the future
	# , dbc.Row([
	# 		dbc.Col([dbc.Row([dbc.Alert("__Charts__", color="primary")], justify = 'center')
	# 		,dbc.Row(html.Div(id='x-vol-1'), justify = 'center')
	# 		, dcc.Interval(
	# 				id='interval-component',
	# 				interval=1*150000, # in milliseconds
	# 				n_intervals=0)   
	# 		, dcc.Interval(
	# 				id='interval-component2',
	# 				interval=1*60000, # in milliseconds
	# 				n_intervals=0)      
	# 				])#end col
	# 		])#end row           
	# ]) #end div
])



# Back end stuffs 
# Each input/ output uses it's own callback   

# Callbacks

# Select date of launch
@app.callback(
    Output('output-date-picker', 'children'),
    Input('input-date-picker', 'date'))

def update_output(date_value):
    string_prefix = 'Date selected: '
    if date_value is not None:
        date_object = date.fromisoformat(date_value)
        date_string = date_object.strftime('%B %d, %Y')
        return string_prefix + date_string
    



# Select the time frame 
@app.callback(
    Output('output-date-range-picker', 'children'),
    [Input('input-date-range-picker', 'start_date'),
    Input('input-date-range-picker', 'end_date')])

def update_output(start_date, end_date):
    string_prefix = 'You have selected: '
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
        return string_prefix




# Select client we're targeting
@app.callback(
    Output('output-client-picker', 'children'),
    Input('input-client-picker', 'value'))
 
# Takes the client_name input and outputs info about  stock
# Connect the yfinance API here 
def update_client_picker(ticker):
    ticker = ticker.upper()
    TICKER = yf.Ticker(ticker)
        
    cards = [ 
	dbc.Col(make_card("Client selected:", "secondary", TICKER.info['shortName'])),
	dbc.Col(make_card("Previous Close ", "secondary", TICKER.info['previousClose'])),
    dbc.Col(make_card("Open", "secondary", TICKER.info['open'])),
    dbc.Col(make_card("Sector", 'secondary', TICKER.info['sector'])),
    dbc.Col(make_card("50d Avg Price", 'secondary', TICKER.info['fiftyDayAverage']))
    ] #end cards list
    return cards




# Select the subindustry competitors
# OKAY now lets do a graph over time WITH companies AND the date info?
# HOW TO INCORPORATE DATA ACROSS BOTH DATE RANGE PICKER AND 
# COMPANY SELECTOR TO GET GRAPH
@app.callback(
    Output('output-subindustry-picker', 'children'),
    [Input('input-subindustry-picker', 'value'), 
	Input('input-date-range-picker', 'start_date'), 
	Input('input-date-range-picker', 'end_date')])

def update_output(companies, start_date, end_date):
	#print('You have selected "{}"'.format(companies))
	hash = {}
	end_date_object = date.fromisoformat(end_date)

	for x in companies: 
		if start_date is not None:			
			start_date_object = date.fromisoformat(start_date)
			new_date = start_date_object + timedelta(days=30)
			prices = []
			# NEED TO PULL YFINANCE DATA FOR EACH NEW_DATE
			# MAYBE USE PANDAS TO STRUCURE DATA LIKE EXCEL
			while new_date < end_date_object:
				temp = x.upper()
				# Use the new date to access the correct data
				TICKER = yf.Ticker(temp)
				print(TICKER.history(period = new_date)["open"])
				price = TICKER.info['open']
				prices.append(price)
				new_date = new_date + timedelta(30)	
			hash[x] = prices

		# This while loop isn't great. The yfinance stuff is accurate
		# just need to get the right dates
		# while begin < end_date:
		# 	temp = x.upper()
		# 	TICKER = yf.Ticker(temp)
		# 	price = TICKER.info['open']
		# 	prices.append(price)
		# 	begin = begin + datetime.timedelta(days=30) # 30 days?
		# 	print(begin)

	print(hash)
	# return make_graph(companies, hash)

	# For loop through companies
		# Access yfinance data
			# Possibly helper function because I need to 
			# pull open prices for each 1st Monday of the month
			# from start to end range  
		# MAYBE START SIMPLE AND JUST PLOT ALL OPENS 
		# FOR ENTIRE TIME RANGE SO WE CAN JUST A CHART UP
	# Now we have an array of tuples?

def make_graph(companies, hash):
	# I have a hash of numbers in "hash". I need to make an array 
	# of numbers (average stock growth) to input into fig
	fig = go.Figure(data=[go.Scatter(x=companies, y=prices)])

	newGraph = html.Div(dcc.Graph(
		id='output-subindustry-picker',
		figure=fig
	))
	return newGraph

						##### NOTES ####
# INDUSTRY GROWTH --> LOOK AT % STOCK PRICE GROWTH MONTH OVER MONTH FOR 1 YEAR PRE-LAUNCH
# AND 1 YEAR POST LAUNCH. USE GROCERY STORE SUBINDUSTRY AS EXAMPLE 

# MARKET CAPITALIZATION WEIGHTED IS ANOTHER WAY TO MAKE THE GRAPH
# MAYBE AN EXTEND FEATURE

# ANOTHER STEP IS LOOKING AT HOW TO BUILD A GRAPH WITH THE DATA 
# https://medium.com/swlh/how-to-create-a-dashboard-to-dominate-the-stock-market-using-python-and-dash-c35a12108c93
# DOES A GREAT JOB OF EXPLAINING WHAT TO DO 

# Still use the grocery store data EVEN THOUGH IT DOESNT PROVE OUTCOME

# Helper functions to be added into layout/ callbacks 
# def display_value(value):
#     return 'You have selected "{}"'.format(value)




# IDK JUST OLDER STUFF THAT I'M NOT CURRENTLY USING. 
# DELETE THIS SOON PROBABLY 



# def get_info_box(): 
# 	return html.Div([
# 			html.Div([dcc.Dropdown(id='stock-index-choice', #???
# 				                   options=index_choice,
# 				                   value=index_choice[0]['value']
# 								   )]),
# 			html.Div(style={'width':'20%','display': 'inline-block'}),
# 			html.Div([dcc.Dropdown(id='stock-include',
# 				                   options=[],
# 				                   value=[],
# 				                   multi=True
# 				                )])
# 		])    



# unused at the moment 
def verify_ticker(ticker):
    tick = re.findall('^[A-Za-z]{1,4}$', ticker) 
    # python regex to find matches and return strings 
    if len(tick)>0:
        return True, tick[0].upper()
    else: 
        return False

# ticker = "AAPL"

def get_ticker(n_clicks, time, ticker, mkt):
	# For default setting
	if ticker == '':
		return 'Please Enter a Stock Ticker', \
		       '','','',{'width':'20%', 'display':'inline-block'},'', \
		       {'width':'20%', 'display':'inline-block'},'', \
		       {'data':None}, None
	# Verify ticker format in respective to stock market
	stockFormat, ticker = verify_ticker(ticker, mkt)
	# Catch incorrect 
	if stockFormat is False:
		return 'Wrong Ticker', '#######', '$##.##', '##.##', \
		       {'width':'20%', 'display':'inline-block'}, '##.##%', \
		       {'width':'20%', 'display':'inline-block'}, \
		       'Error! Please try again.', {'data':None}, None
	# Obtain stock price and stats
	stock = yfinance.Ticker(ticker)
	# Catch if stock exists
	if stock.history(period='ytd').shape[0] == 0:
		return 'Wrong Ticker', '#######', '$##.##', '##.##', \
		       {'width':'20%', 'display':'inline-block'}, '##.##%', \
		       {'width':'20%', 'display':'inline-block'}, \
		       'Error! Please try again.', {'data':None}, None
	### Stock Stats for Info Box ###
	try: 
		# Name and price
		stock_name = stock.info['longName']
		price_list = stock.history(period=time)['Close'].tolist()
		price = f'${price_list[-1]:.2f}'
		# Price Change
		price_change = price_list[-1] - price_list[-2]
		price_percent_change = (price_list[-1]/price_list[-2])-1
		if price_change > 0:
			price_change_colour = {'color':'green'}
		else:
			price_change_colour = {'color':'red'}
		price_change_colour['display']= 'inline-block'
		price_change_colour['width']= '20%'
		price_change_colour['font-size'] = '150%'
		price_change = f'{price_change:.2f}'
		price_percent_change = f'{price_percent_change*100:,.2f}%'

		df = getMA(stock, time, 
			       stock.history(period=time).reset_index()['Date'])

		fig = getCandlestick(df)
		table = getTab1Table(stock.history(period=time).reset_index(),
			                 stock.info)

	except:
		return 'Sorry! Company Not Available', '#######', '$##.##', '##.##', \
		       {'width':'20%', 'display':'inline-block'}, '##.##%', \
		       {'width':'20%', 'display':'inline-block'}, \
		       'Error! Please try again another Company.', {'data':None}, None


	return stock_name, ticker, price, price_change, price_change_colour, \
	       price_percent_change, price_change_colour, '', fig, table



def get_tab1_info_box():
	return html.Div([
				html.Div([
					html.Div(id='tab1-stock-price',
						     style={'width':'30%','display':'inline-block',
						            'font-size':'200%'}),
					html.Div(id='tab1-stock-price-change'),
					html.Div(id='tab1-stock-price-percentchange')
					],style={'width':'30%','display': 'inline-block',
			                 'vertical-align':'top'}),
				html.Div(style={'width':'15%','display': 'inline-block'}),
				html.Div(dcc.Dropdown(id='tab1-market-dropdown',
					                  options=tab1_markets,
					                  value=tab1_markets[0]['value'],
				                      style={'text-align':'left'}),
					     style={'width':'20%','display': 'inline-block',
			            		'vertical-align':'top'}),
				html.Div(style={'width':'5%','display': 'inline-block'}),
				html.Div([
					html.Div([
						html.Div(dcc.Input(id='tab1-ticker-input',value='',
						                   type='text'),
						                   style={'display': 'inline-block'}),
						html.Div(html.Button('Submit',id='tab1-submit'),
							     style={'display': 'inline-block'})
						]),
					html.Div(id='tab1-error-message', style={'color':'red'}, children='Error Box')
					],style={'width':'30%','display': 'inline-block'})
			])


# def get_ticker():
#     stock = yfinance.Ticker(ticker)

#     print(stock)
# #     Assume stock ticker exists, but need to add check if doesnt


if __name__ == '__main__':
    app.run_server(debug=True)