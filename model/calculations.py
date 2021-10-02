
# Model - business logic for all calculations need to get average stock price growth 
# for the companies we're looking at. Calculates client stock growth and subindustry growth

import dal.finance as fin
from datetime import date, datetime, timedelta

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


# total growth, not the day over day
def calculate_avg_growth_alt(entity, start_date, end_date):
	growths = []

	data = fin.get_data(entity, start_date, end_date)
	stock_data = data['Open']
	prev_day = 0

	for day_price in stock_data:
		if prev_day == 0:
			prev_day = day_price
		else:
			percent_change = ((day_price - prev_day) / day_price) * 100 
			rounded = round(percent_change, 3)
			growths.append(rounded)	

	return growths


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


# check on bank holidays? trading floor closed? 
def calc_weekdays(start, end, excluded=(6, 7)):
    all_days = []

    start_date_object = date.fromisoformat(start)
    end_date_object = date.fromisoformat(end)

    print(start_date_object.isoweekday())

    while start_date_object <= end_date_object:
        if start_date_object.isoweekday() not in excluded:
            print(start_date_object.isoweekday())
            all_days.append(start_date_object)
        start_date_object += datetime.timedelta(days=1)

    return all_days






    #     new_date = start_date_object + timedelta(days=1)

    # start_date_object = date.fromisoformat(start)
    # end_date_object = date.fromisoformat(end)

    # while start_date_object <= end_date_object:
    #     if start_date_object.isoweekday() not in excluded:
    #         all_days.append(start_date_object)
    #     start_date_object += datetime.timedelta(days=1)

    # return all_days