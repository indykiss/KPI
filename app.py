
import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly 
import pandas
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

    # Date picker, last 5 years 
    dcc.DatePickerSingle(
        id="date-picker", 
        min_date_allowed=date(2015, 1, 1),
        max_date_allowed=datetime.today(), # not sure if correct format
        # maybe datetime.today().strftime('%Y-%m-%d') to get => '2021-01-26'
        initial_visible_month=date(2021,8,1), 
        date=date(2021,8,1)
        # need to look at the dash documentation for date
    ),
    # Stock ticker dropdown 
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
        value='LA'
    ),
    html.Div(id='display-value')
])


# Callbacks
@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Output('date-picker', 'children')],
              [dash.dependencies.Input('dropdown', 'value')])

def display_value(value):
    return 'You have selected "{}"'.format(value)

def display_graph(date):
    return "got it"

if __name__ == '__main__':
    app.run_server(debug=True)