
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
import pandas as pd 
import pandas_datareader as pdr
import re
import yfinance as yf
from dash.exceptions import PreventUpdate
from datetime import date, datetime, timedelta
from helpers import make_table, make_card, ticker_inputs, make_item


# Basically index.py

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
        date=date(2021, 8, 1)
    ),

	# Works well enough. 2 years working ok
	html.Div("Select the time range. Please select a starting date before launch and an end date after launch. We recommend 1 year BEFORE launch and 1 year AFTER launch. Please note that selecting competitors that were not public during this entire range will result in skewed data."),
    dcc.DatePickerRange(
        id='input-date-range-picker',
        min_date_allowed=date(2000, 1, 1),
        max_date_allowed=date.today(), # in deployment, would need to make this callback to be dynamic: https://stackoverflow.com/questions/62608204/dash-datepicker-max-date-allowed-as-current-date-not-working-properly
        initial_visible_month=date(2021, 9, 1),
		clearable=True
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
			{'label': 'IDK', 'value': 'AD'},
			{'label': 'Shoprite', 'value': 'SRGHY'},
			{'label': 'Spartan Nash', 'value': 'SPTN'},
			{'label': 'Kroger', 'value': 'KR'},
			{'label': 'Walgreens', 'value': 'WBA'},
			{'label': 'Walmart', 'value': 'WMT'},
			{'label': 'Wegmans', 'value': 'WEGMANS'}			
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
			{'label': 'Costco', 'value': 'COST'},
			{'label': 'IDK', 'value': 'AD'},
			{'label': 'Shoprite', 'value': 'SRGHY'},
			{'label': 'Spartan Nash', 'value': 'SPTN'},
			{'label': 'Kroger', 'value': 'KR'},
			{'label': 'Walgreens', 'value': 'WBA'},
			{'label': 'Walmart', 'value': 'WMT'},
			{'label': 'Wegmans', 'value': 'WEGMANS'}			
		],
		value=['COST', 'SRGHY', 'SPTN', 'KR', 'WBA'],
		multi=True
	), 

    # Next step: Just add a graph or any info that displays 
    # the client's ticker info

    # Outputs - UI
    html.Div(id='output-date-picker'),
    html.Div(id='output-client-picker'),
	html.Div(id='output-date-range-picker'),
	html.Div(id='output-subindustry-picker'), 
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


# Select client BUT using yfinance to look up tickers, not hardcoded 
# TBD, not in use yet
@app.callback(
    Output('output-yf-client-ticker', 'children'),
    Input('input-yf-client-ticker', 'value'))

# TBD
def update_yf_client_ticker(ticker):
    string_answer = 'You have selected: '

	# if input is accurate ticker
    if ticker is not None: # switch for is a ticker
        string_answer = string_answer + ticker
    else:
        string_answer = 'This is not a valid ticker. Try again.'

    return string_answer


# Select client we're targeting
@app.callback(
    Output('output-client-picker', 'children'), # must be children?
    Input('input-client-picker', 'value'))
 
# Takes the client_name input and outputs info about  stock
# Connect the yfinance API here 
def update_client_picker(ticker):
    ticker = ticker.upper()
    TICKER = yf.Ticker(ticker)
        
    cards = [ 
	dbc.Col(make_card("Client selected:", "secondary", TICKER.info['shortName'])),
    dbc.Col(make_card("Open", "secondary", TICKER.info['open']))
    ] #end cards list
    return cards


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
	Input('input-client-picker', 'value')]) 

#if companies is None or start_date is None or end_date is None or launch_date is None or client is None:
#	raise PreventUpdate
	

# Need to do expected input/ output audit for these functions
def update_output(companies, start_date, end_date, launch_date, client):
    if companies is None or start_date is None or end_date is None or launch_date is None or client is None:
        raise PreventUpdate
	
    all_companies = [*companies]
    all_companies.append(client)

    if start_date is not None:
        dates_data = pd.date_range(start_date, end_date, periods=6)

    # Both lines will have all companies' avg growth over time
    pre_launch_all_avgs = calculate_avg_growth_over_time(all_companies, start_date, launch_date)
    # print(pre_launch_all_avgs)
    # print("pre_launch_all_avgs")   
	
	# After launch date, the subindustry growth rate is different 
    post_launch_subind_avgs = calculate_avg_growth_over_time(companies, launch_date, end_date)
    # print(post_launch_subind_avgs)
    # print("post_launch_subind_avgs")

    # we're adding client growth as a trace line over custom index
    client_post_launch_snippet = calculate_avg_growth_over_time([client], launch_date, end_date)
    # print(client_post_launch_snippet)
    # print("client_post_launch_snippet")

    client_growth = [*pre_launch_all_avgs, *client_post_launch_snippet]
    print("client_growth:")
    print(client_growth)

    all_growths = [*pre_launch_all_avgs, *post_launch_subind_avgs]

    print("all_growths:")
    print(all_growths)

    return make_graph(dates_data, all_growths, client_growth)

# we can change the start/ end date to be start_date to launch then launch to end_date
def calculate_avg_growth_over_time(companies, start_date, end_date): 
    # Will need some sort of helper function most likely 
    all_growths = []
    
    for x in companies: 
        if start_date is not None:
            df = pdr.get_data_yahoo(x, start_date, end_date)
            stock_data = df['Open']
            prev_day = 0
            stock_percent_change = []   
              
            for day_price in stock_data:
                    if prev_day == 0:
                        prev_day = day_price
                    else:
                        percent_change = ((day_price - prev_day) / day_price) * 100 
                        rounded = round(percent_change, 3)
                        stock_percent_change.append(rounded)

                        prev_day = day_price
                        all_growths.append(stock_percent_change)
            
    if start_date is not None:
        return avg_math(all_growths)

# Would return an arr of stock price growth averages
def avg_math(all_growths):
	all_average_growths = []

	num_days = len(all_growths[0])
	i = 0

	#  list index out of range error here sometimes
	while i < num_days:
		sum = 0
		for arr in all_growths:
			sum += arr[i]
		i += 1

		avg = sum / len(all_growths)
		rounded = round(avg, 3)
		all_average_growths.append(rounded)    
	#print(all_average_growths)

	return all_average_growths


def make_graph(dates, all_growths, client_growth):
	fig = go.Figure(
		data=[go.Scatter(x=dates, y=all_growths)],
		layout=go.Layout(
        	title=go.layout.Title(text="Custom index growth over time"))
	)
	newGraph = html.Div(dcc.Graph(
		id='output-subindustry-picker',
		figure=fig
	))
	reference_line2 = go.Scatter(x=dates,
                            y=client_growth,
                            # showlegend=False
							)
	fig.add_trace(reference_line2)

	return newGraph    





# These next 3 functions are perfect and work VERY well
# I'm just commenting out so I can try the new versions of 
# these functions, so we can add client growth trace
# Would be good to divide into a couple functions

# def update_output(companies, start_date, end_date, client, launch_date):	
# 	dict = {} # for debugging company : stock changes
# 	client_growth = []

# 	if start_date is not None:
# 		growths_in_arrs = [] # for slightly easier averaging
# 		dates_data = pd.date_range(start_date, end_date, periods=6)
# 	#  end_date_object = date.fromisoformat(end_date)

# 	# Probably too slow, causing lag?
# 	for x in companies: 
# 		if start_date is not None:			
# 			# start_date_object = date.fromisoformat(start_date)
# 			# new_date = start_date_object + timedelta(days=30)

# 			df = pdr.get_data_yahoo(x, start_date, end_date)
# 			stock_data = df['Open']
# 			prev_day = 0
# 			stock_change = []	

# 			print(stock_data)			

# 			# Calculates growth over time for each company 
# 			for day_price in stock_data:
# 				if prev_day == 0:
# 				    prev_day = day_price
# 				else:
# 					percent_change = ((day_price - prev_day) / day_price) * 100 
# 					rounded = round(percent_change, 3)
# 					stock_change.append(rounded)
# 					if x == client:
# 						client_growth.append(rounded)
# 					prev_day = day_price

# 			# after finishing creating an array of % changes from start to end
# 			dict[x] = stock_change
# 			growths_in_arrs.append(stock_change)

# 	if start_date is not None:
# 		return average_stock_growths(dates_data, growths_in_arrs, client_growth)

# def average_stock_growths(dates, growths_in_arrs, client_growth):
# 	all_average_growths = []
# 	num_days = len(growths_in_arrs[0])
# 	i = 0

# 	#  list index out of range error here sometimes
# 	while i < num_days:
# 		sum = 0
# 		for arr in growths_in_arrs:
# 			sum += arr[i]
# 		i += 1

# 		avg = sum / len(growths_in_arrs)
# 		rounded = round(avg, 3)
# 		all_average_growths.append(rounded)
# 	return make_graph(dates, all_average_growths, client_growth)

# def make_graph(dates, avg_growth, client_growth):
	fig = go.Figure(
		data=[go.Scatter(x=dates, y=avg_growth)],
		layout=go.Layout(
        	title=go.layout.Title(text="Custom index growth over time"))
	)

	newGraph = html.Div(dcc.Graph(
		id='output-subindustry-picker',
		figure=fig
	))
	reference_line2 = go.Scatter(x=dates,
                            y=client_growth,
                            # showlegend=False
							)
	fig.add_trace(reference_line2)

	return newGraph





# Add a trace line over graph, different color 



						##### NOTES ####
# INDUSTRY GROWTH --> LOOK AT % STOCK PRICE GROWTH MONTH OVER MONTH FOR 1 YEAR PRE-LAUNCH
# AND 1 YEAR POST LAUNCH. USE GROCERY STORE SUBINDUSTRY AS EXAMPLE 

# MARKET CAPITALIZATION WEIGHTED IS ANOTHER WAY TO MAKE THE GRAPH
# MAYBE AN EXTENDED FEATURE

# ANOTHER STEP IS LOOKING AT HOW TO BUILD A GRAPH WITH THE DATA 
# https://medium.com/swlh/how-to-create-a-dashboard-to-dominate-the-stock-market-using-python-and-dash-c35a12108c93
# DOES A GREAT JOB OF EXPLAINING WHAT TO DO 





# IDK JUST OLDER STUFF THAT I'M NOT CURRENTLY USING. 
# DELETE THIS SOON PROBABLY 

# I couldn't get output working bc of some antivirus or version thing, so dropping jupyter right now. 
# 
# https://mybinder.org/v2/gh/ipython/ipython-in-depth/7e5ce96cc9251083979efdfc393425f1229a4a68?filepath=binder%2FIndex.ipynb

# def update_output(companies, start_date, end_date):
# 	#print('You have selected "{}"'.format(companies))
	
# 	hash = {}
# 	#  end_date_object = date.fromisoformat(end_date)

# 	for x in companies: 
# 		if start_date is not None:			
			# start_date_object = date.fromisoformat(start_date)
			# new_date = start_date_object + timedelta(days=30)
			# NEED TO PULL YFINANCE DATA FOR EACH NEW_DATE
			# MAYBE USE PANDAS TO STRUCURE DATA LIKE EXCEL

			# IDK MAYBE TRYING TO REPLACE BELOW WITH PANDAS
			# while new_date < end_date_object:
			# 	temp = x.upper()
			# 	# Use the new date to access the correct data
			# 	TICKER = yf.Ticker(temp)
			# 	# print(TICKER.history(period = new_date)["open"])

			# 	price = TICKER.info['open']
			# 	prices.append(price)
			# 	new_date = new_date + timedelta(30)	
			# hash[x] = prices

		# This while loop isn't great. The yfinance stuff is accurate
		# just need to get the right dates
		# while begin < end_date:
		# 	temp = x.upper()
		# 	TICKER = yf.Ticker(temp)
		# 	price = TICKER.info['open']
		# 	prices.append(price)
		# 	begin = begin + datetime.timedelta(days=30) # 30 days?
		# 	print(begin)



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



# unused at the moment: stock ticker lookup 
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