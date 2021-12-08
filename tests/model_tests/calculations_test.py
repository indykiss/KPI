
# import sys
import pytest
import model.calculations as calc

def test_average():
    #arrange
    list = [1 , 8 , 12]
    expected = 7

    #act
    actual = calc.average(list)

    #assert
    return actual == expected

def another_test():
    return True


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