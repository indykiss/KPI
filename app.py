
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
    html.H2('KPI Builder'),    
    html.H4('Please input target ticker, industry dropdown, and launch date.'),

    dcc.DatePickerSingle(
        id='my-date-picker-single',
        min_date_allowed=date(2010, 1, 1),
        max_date_allowed=date.today(),
        initial_visible_month=date.today(),
        date=date(2021, 8, 1)
    ),
    
    html.Div("Target vs "),
    html.Div(get_info_box),
    html.Div(get_graph),

    html.Div(id='output-container-date-picker-single')

    # Now add a stock sticker tab 
    # Simple display current stock price

    # Step after that is showing a graph, any graph  
])



# Callbacks
@app.callback(
    Output('output-container-date-picker-single', 'children'),
    Input('my-date-picker-single', 'date'))
def update_output(date_value):
    string_prefix = 'You have selected: '
    if date_value is not None:
        date_object = date.fromisoformat(date_value)
        date_string = date_object.strftime('%B %d, %Y')
        return string_prefix + date_string


# Helper functions to be added into layout/ callbacks 
# def display_value(value):
#     return 'You have selected "{}"'.format(value)

def display_graph(date):
    return "got it"

def get_info_box: 
	return html.Div([
			html.Div([dcc.Dropdown(id='stock-index-choice', #???
				                   options=index_choice,
				                   value=index_choice[0]['value']
								   )]),
			html.Div(style={'width':'20%','display': 'inline-block'}),
			html.Div([dcc.Dropdown(id='stock-include',
				                   options=[],
				                   value=[],
				                   multi=True
				                )])
		])    

def verify_ticker(ticker):
    tick = re.findall('^[A-Za-z]{1,4}$', ticker) 
    # python regex to find matches and return strings 
    if len(tick)>0:
        return True, tick[0].upper()
    else: 
        return False

ticker = "AAPL"

# def get_stock(ticker):
#     stock = yfinance.Ticker(ticker)

#     print(stock)
#     Assume stock ticker exists, but need to add check if doesnt


if __name__ == '__main__':
    app.run_server(debug=True)