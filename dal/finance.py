
# Data access layer. Facade for yf
import yfinance as yf

def get_data(symbol, start_date, end_date):
    ticker = yf.Ticker(symbol)
    result = ticker.history(start=start_date, end=end_date)
    return result 

def get_ticker(symbol):
    return yf.Ticker(symbol)

