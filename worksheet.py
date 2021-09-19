

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
def main(companies, start_date, end_date, launch_date, client):
    all_companies = companies.append(client)

    if start_date is not None:
        dates_data = pd.date_range(start_date, end_date, periods=6)

    pre_launch_avgs = calculate_avg_growth_over_time(all_companies, start_date, launch)
    
    post_launch_avgs = calculate_avg_growth_over_time(companies, launch, end_date)
    # we're adding client growth as a trace line over custom index
    client_post_launch_snippet = calculate_avg_growth([client], launch, end_date)

    client_growth = [*pre_launch_avgs, *client_post_launch_snippet]

    all_growths = [*pre_launch_avgs, *post_launch_avgs]

    return make_graph(dates_data, all_growths, client_growth)


# we can change the start/ end date to be start_date to launch
# then launch to end_date
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

	num_days = len(growths_in_arrs[0])
	i = 0

	#  list index out of range error here sometimes
	while i < num_days:
		sum = 0
		for arr in growths_in_arrs:
			sum += arr[i]
		i += 1

		avg = sum / len(growths_in_arrs)
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
    



