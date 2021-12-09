

# What am I doing? 

# Algorithm:
# - Need to figure out how to graph the two lines such that they overlap
# THEN deviate for client growth 

# - Build the helper functions needed. 
#  - Maybe just need 1 "calculate companies in arr growth" 
#  - Before launch date, need all companies 
#  - After launch date, all except client 
#  - Problem is in how I'm calculcating growth now. I'm doing 
#  for each company, calculate growth from start to end date.
#  What I need to do is calculate growth from start to end, changing cos

# Trying to basically get the actual two line graph bit is priority. 

Not actually running, just get logics in here 

companies = ['COST', 'SPTN', 'KR', 'WBA']
client = 'SRGHY'
start_date = 9/1/2021 
end_date = 9/8/2021
launch_date = 9/5/2021


yfinance API --> input a ticker & date, gets stock price at open on date


# I am working on these 4 functions here: 
# Trying to copy the logics in the left panel to this, 
# but switching "for x in companies" to date specific data
def update_output(companies, start_date, end_date, launch_date, client):
    all_companies = companies.append(client)

    if start_date is not None:
        dates_data = pd.date_range(start_date, end_date, periods=6)

    # Both lines will have all companies' avg growth over time
    pre_launch_all_avgs = calculate_avg_growth_over_time(all_companies, start_date, launch)
    # After launch date, the subindustry growth rate is different 
    post_launch_subind_avgs = calculate_avg_growth_over_time(companies, launch, end_date)
    # we're adding client growth as a trace line over custom index
    client_post_launch_snippet = calculate_avg_growth_over_time([client], launch, end_date)

    client_growth = [*pre_launch_all_avgs, *client_post_launch_snippet]

    all_growths = [*pre_launch_all_avgs, *post_launch_subind_avgs]

    return make_graph(dates_data, all_growths, client_growth)

# we can change the start/ end date to be start_date to launch then launch to end_date
def calculate_avg_growth_over_time(companies, start_date, end_date): 
    # Will need some sort of helper function most likely 
    all_growths = []
    
    for x in companies: 
        if start_date is not None:
            df = pdr.get_data_yahoo(x, start_date, end_date)
            stock_data = df['Open']
            prev = 0
            stock_percent_change = []   
              
            for day_price in stock_data:
                    if prev_day == 0:
                        prev_day = day_price
                    else:
                        percent_change = ((day_price - prev_day) / day_price) * 100 
                        rounded = round(percent_change, 3)
                        stock_percent_change.append(rounded)

                        prev_day = day_price
                        all_growths.append(stock_change)
            
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




# def growth_math(stock_data, prev_day):
# 	stock_change = []				

# 	# Calculates growth over time for each company 
# 	for day_price in stock_data:
# 		if prev_day == 0:
# 			prev_day = day_price
# 		else:
# 			percent_change = ((day_price - prev_day) / day_price) * 100 
# 			rounded = round(percent_change, 3)
# 			stock_change.append(rounded)

#             # this is not a thing that will work here
# 			prev_day = day_price  # this wont update since new function
#             # need to fix this  

#     return stock_change


# def avg_math(all_growths):
    





# Functions that are okay and want to clear off my app.py


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
	# fig = go.Figure(
	# 	data=[go.Scatter(x=dates, y=avg_growth)],
	# 	layout=go.Layout(
	# 		title=go.layout.Title(text="Custom index growth over time"))
	# )

	# newGraph = html.Div(dcc.Graph(
	# 	id='output-subindustry-picker',
	# 	figure=fig
	# ))
	# reference_line2 = go.Scatter(x=dates,
	# 						y=client_growth,
	# 						# showlegend=False
	# 						)
	# fig.add_trace(reference_line2)

	# return newGraph





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



def make_graph(dates, all_growths, client_growth):
	fig = go.Figure()

	fig.add_trace(go.Scatter(
		x=dates,
		y=all_growths, 
		mode="lines+markers",
		name="Custom index growth"
	))

	fig.add_trace(go.Scatter(
		x=dates,
		y=client_growth,
		mode="lines+markers",
		name="Client growth"
	))

	newGraph = html.Div(dcc.Graph(
		id='output-subindustry-picker',
		figure=fig
	))	

	return newGraph

	# fig = go.Figure(
	# 	data=[go.Scatter(x=dates, y=all_growths)],
	# 	layout=go.Layout(
	# 		title=go.layout.Title(text="Custom index growth over time"))
	# )

	# fig.add_trace(go.Scatter(
	# 						x=dates,
	# 						y=client_growth,
	# 						mode="lines",
	# 						line=go.scatter.Line(color="gray")
	# 						# showlegend=False
	# 						))

	# newGraph = html.Div(dcc.Graph(
	# 	id='output-subindustry-picker',
	# 	figure=fig
	# ))

	# return newGraph    