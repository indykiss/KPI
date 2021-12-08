
# import sys
import pytest
import model.calculations as calc


# I actually need to double check my maths
def test_avg_math():
    #arrange
    all_growths = [[10,10,10,10], [10,10,10,10], [20,20,20,20], [20,20,20,20]]
    all_avg_growths = []
    num_days = 4
    i = 0

    while i < num_days:
    	sum = 0
        # arr = [10,10,10, 10]
    	for arr in all_growths:
    		sum += arr[i]
    	i += 1

        # sum = 40. 
        # maybe this needs to be len(arr)
    	avg = sum / len(all_growths)
        # avg = 10 
    	rounded = round(avg, 3)
        # rounded = 10 
    	all_avg_growths.append(rounded)  
        # [10]  

    expected = [10, 10, 20, 20]

    #actual 
    actual_res = calc.avg_math(all_avg_growths)    

    #assert
    return expected == actual_res


def test_average():
    #arrange
    list = [1 , 8 , 12]
    expected = 7

    #act
    actual = calc.average(list)

    #assert
    return actual == expected


# Make more calculation tests here 
# idk, nothing is working right now :(
# def test_calculate_avg_growth_over_time():
#     #arrange
#     companies = ["Apple", "Microsoft"]
#     start_date = 1/1/2020
#     end_date = 1/1/2021
#     all_growths = []

#     #act
#     for x in companies:
#         data = [10, 20, 30]
#         day_price = 10
#         prev_day = 5

#         percent_change = ((day_price - prev_day) / day_price) * 100 
#         all_growths.append(percent_change)

#     #assert


# # not right:
# def test_avg_maths(): 
#     # arrange
#     all_average_growths = [10, 5, 5, 10, 10]
#     all_growths = 5
#     expected = 8

#     #act
#     actual = calc.avg_math(all_average_growths)

#     #assert
#     return actual == expected