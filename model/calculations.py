
# Model - business logic for all calculations need to get average stock price growth 
# for the companies we're looking at. Calculates client stock growth and subindustry growth

import dal.finance as fin

# we can change the start/ end date to be start_date to launch then launch to end_date
def calculate_avg_growth_over_time(companies, start_date, end_date): 
	all_growths = []

	for x in companies: 
		if start_date is not None:
			try:
				data = fin.get_data(x, start_date, end_date)
			except:
				print("An exception error")
			stock_data = data['Open']
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
		#print(all_growths)
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

	return all_average_growths


def average(input):
    sum = 0
    for a in input:
        sum += a
    
    avg = sum / len(input)
    return avg