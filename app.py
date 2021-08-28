
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output # So I can simplify callback
import plotly 
import pandas
import re
from datetime import date
from datetime import datetime


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

    # html.Div(get_info_box()),
    
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

    # Next step: Just add a graph or any info that displays 
    # the client's ticker info

    # Outputs - UI
    html.Div(id='output-date-picker'),
    html.Div(id='output-client-picker')

    # Now add a stock sticker tab 
    # Simple display current stock price

    # Step after that is showing a graph, any graph  
])



# Back end stuffs 
# Each input/ output uses it's own callback   

# Callbacks
@app.callback(
    Output('output-date-picker', 'children'),
    Input('input-date-picker', 'date'))
def update_output(date_value):
    string_prefix = 'You have selected: '
    if date_value is not None:
        date_object = date.fromisoformat(date_value)
        date_string = date_object.strftime('%B %d, %Y')
        return string_prefix + date_string
    
# Keep it simple for now, only hardcoded clients as option  
@app.callback(
    Output('output-client-picker', 'children'),
    Input('input-client-picker', 'value'))
 
# Takes the client_name input and outputs info about 
# stock
# Basically just connect the world finance API now 

def update_client_picker(client_name):
    string_prefix = 'You have selected: '
    if client_name is not None: 
        return string_prefix + client_name



# Step 1: Check if the fiance API is working
# Just display on page in a div




# Helper functions to be added into layout/ callbacks 
# def display_value(value):
#     return 'You have selected "{}"'.format(value)

def display_graph(date):
    return "got it"



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