import pytest
import model.calculations as calc

def test_average():
    #arrange
    list = [ 1 , 8 , 12]
    expected = 7

    #act
    actual = calc.average(list)

    #assert
    return actual == expected


# Make more calculation tests here 
