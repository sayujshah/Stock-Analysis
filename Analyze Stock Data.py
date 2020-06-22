# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 12:22:28 2020

@author: sayuj
"""

from datetime import datetime as dt

import pandas as pd
from pandas.util.testing import assert_frame_equal
import pandas_datareader.data as web
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

# Set today's date in order to pull stock data through current time
today = datetime.strftime(datetime.today(), "%Y-%m-%d")

# Create the function to extract data from a specific data sources (CSV, API, JSON, etc.)
def get_symbols(symbols,data_source, begin_date=None,end_date=None):
    """

    Parameters
    ----------
    symbols : stock ticker you want to pull data for
    data_source : data source that the stock data will be pulled from (CSV, API, JSON, etc.)
    begin_date : start of lookback period/start point for the timeframe you want data for (default is None)
    end_date : end of lookback period/end point for the timeframe you want data for (default is None)
        DESCRIPTION. The default is None.

    Returns: a dataframe of stock data for the specified ticker that includes opening, high, low, and closing price, as well as stock volume
    -------

    """
    
    out = pd.DataFrame()
    for symbol in symbols:
        df = web.DataReader(symbol, data_source,begin_date, end_date, api_key='K45BwXh1hBWjQMVjz7d5')\
        [['AdjOpen','AdjHigh','AdjLow','AdjClose','AdjVolume']].reset_index()
        df.columns = ['Date','Open','High','Low',symbol,'Volume'] #my convention: always lowercase
        df['Symbol'] = symbol # add a new column which contains the symbol so we can keep multiple symbols in the same dataframe
        df = df[::-1].reset_index()
        out = pd.concat([out,df],axis=0) #stacks on top of previously collected data
    return out.sort_index()

def input_ticker():
    """
    
    Function that allows for a user to input as many stock tickers they would like to extract data for
    
    """
    
    tickers = []
    while True:
        user_input = input('Stock Ticker (type "Done" if finished): ')
        if user_input == 'Done':
            break
        else:
            tickers.append(user_input)
            continue
    return tickers

# User-specified stock ticker will be the "symbols" input for the "get_symbols" function
symbol = input_ticker()

# Call the function and assign the returned dataframe object to a variable
df = get_symbols(symbol,data_source='quandl',\
                     begin_date='2009-12-31',end_date=today)

# Plot the stock price data for each stock symbol
for i in symbol:
    plt.figure(figsize=(14, 5), dpi=100)
    plt.plot(df['Date'],df[i], label=i + ' stock')
    plt.xlabel('Date')
    plt.ylabel('USD')
    plt.title('Figure 2: ' + i + ' stock price')
    plt.legend()
    plt.show()
