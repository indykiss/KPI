
# Model - business logic for all calculations need to get average stock price growth 
# for the companies we're looking at. Calculates client stock growth and subindustry growth

import dal.finance as fin
from datetime import date, datetime, timedelta

# Total growth, not the day over day
# run a report in cap to check?
# https://docs.google.com/spreadsheets/d/19b3lTcmgVSpAHsV-Tar6kmg3FCv8964a/edit?usp=sharing&ouid=102344271465415076950&rtpof=true&sd=true
def calculate_avg_growth(entity, start_date, end_date):
	growths = []
	data = fin.get_data(entity, start_date, end_date) 
	stock_data = data['Open'] 
	first_day = 0
	print(entity)
	for day_price in stock_data:
		if first_day == 0:
			first_day = day_price
			growths.append(100) # need to start growth with 100%
		else:
			percent_change = ((day_price / first_day)) * 100 
			rounded = round(percent_change, 2)
			growths.append(rounded)	
	return growths

