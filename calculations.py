

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

