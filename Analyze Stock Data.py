# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 12:22:28 2020

@author: sayuj
"""

import pandas as pd
import pandas_datareader.data as web

import numpy as np

import matplotlib.pyplot as plt

from talib._ta_lib import *
import talib

from datetime import datetime

import inspect

# Set today's date in order to pull stock data through current time
today = datetime.strftime(datetime.today(), "%Y-%m-%d")

# Create the function to extract data from a specific data sources (CSV, API, JSON, etc.)
def get_symbols(symbols,data_source, begin_date, end_date=today):
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
    
    out = []
    for symbol in symbols:
        df = web.DataReader(symbol, data_source, begin_date, end_date, api_key="""INSERT YOUR API KEY HERE""")\
        [['AdjOpen','AdjHigh','AdjLow','AdjClose','AdjVolume']].reset_index()
        df.columns = ['Date','Open','High','Low',symbol,'Volume'] #my convention: always lowercase
        df = df[::-1].reset_index()
        out.append(df.sort_index())
    return out


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

def input_indicator():
    """
    
    Function that allows for a user to input as many technical indicators as they would like to plot for the selected stocks
    
    """
    
    indicators = []
    while True:
        user_input = input('Technical Indicator (type "Done" if finished and "Help" for list of indicators): ')
        if user_input == 'Done':
            break
        elif user_input == 'Help':
            print(talib.get_functions())
            continue
        else:
            if user_input in dir(talib):
                indicators.append(user_input)
            else:
                continue
    return indicators

def plot_graphs():
    # User-specified stock ticker will be the "symbols" input for the "get_symbols" function
    symbol = input_ticker()
    
    # Call the function and assign the returned dataframe object to a variable
    df = get_symbols(symbol,data_source='quandl',\
                         begin_date='2009-12-31', end_date=today)
    
    open_df = {}
    high_df = {}
    low_df = {}
    close_df = {}
    volume_df = {}
    
    
    # Plot the stock price data for each stock symbol
    plt.figure(figsize=(14, 5), dpi=100)
    for i,v in enumerate(symbol):
        plt.plot(df[i]['Date'], df[i][v], label=f'{v}')
        open_df[f'{v}'] = df[i]['Open']
        high_df[f'{v}'] = df[i]['High']
        low_df[f'{v}'] = df[i]['Low']
        close_df[f'{v}'] = df[i][v]
        volume_df[f'{v}'] = df[i]['Volume']
        
    plt.xlabel('Date')
    plt.ylabel('USD')
    plt.title(f'{", ".join(symbol)} stock price')
    plt.legend()
    plt.show()
    
    openprice = pd.DataFrame(open_df)
    high = pd.DataFrame(open_df)
    low = pd.DataFrame(low_df)
    close = pd.DataFrame(close_df)
    volume= pd.DataFrame(volume_df)
    periods = 30
    
    indicators = input_indicator()
    indicator_dict = {'HT_DCPERIOD': HT_DCPERIOD, 'HT_DCPHASE': HT_DCPHASE, 'HT_PHASOR': HT_PHASOR, 'HT_SINE': HT_SINE, 'HT_TRENDMODE': HT_TRENDMODE, 'ADD': ADD, 'DIV': DIV, 'MAX': MAX, 'MAXINDEX': MAXINDEX, 'MIN': MIN, 'MININDEX': MININDEX, 'MINMAX': MINMAX, 'MINMAXINDEX': MINMAXINDEX, 'MULT': MULT, 'SUB': SUB, 'SUM': SUM, 'ACOS': ACOS, 'ASIN': ASIN, 'ATAN': ATAN, 'CEIL': CEIL, 'COS': COS, 'COSH': COSH, 'EXP': EXP, 'FLOOR': FLOOR, 'LN': LN, 'LOG10': LOG10, 'SIN': SIN, 'SINH': SINH, 'SQRT': SQRT, 'TAN': TAN, 'TANH': TANH, 'ADX': ADX, 'ADXR': ADXR, 'APO': APO, 'AROON': AROON, 'AROONOSC': AROONOSC, 'BOP': BOP, 'CCI': CCI, 'CMO': CMO, 'DX': DX, 'MACD': MACD, 'MACDEXT': MACDEXT, 'MACDFIX': MACDFIX, 'MFI': MFI, 'MINUS_DI': MINUS_DI, 'MINUS_DM': MINUS_DM, 'MOM': MOM, 'PLUS_DI': PLUS_DI, 'PLUS_DM': PLUS_DM, 'PPO': PPO, 'ROC': ROC, 'ROCP': ROCP, 'ROCR': ROCR, 'ROCR100': ROCR100, 'RSI': RSI, 'STOCH': STOCH, 'STOCHF': STOCHF, 'STOCHRSI': STOCHRSI, 'TRIX': TRIX, 'ULTOSC': ULTOSC, 'WILLR': WILLR, 'BBANDS': BBANDS, 'DEMA': DEMA, 'EMA': EMA, 'HT_TRENDLINE': HT_TRENDLINE, 'KAMA': KAMA, 'MA': MA, 'MAMA': MAMA, 'MAVP': MAVP, 'MIDPOINT': MIDPOINT, 'MIDPRICE': MIDPRICE, 'SAR': SAR, 'SAREXT': SAREXT, 'SMA': SMA, 'T3': T3, 'TEMA': TEMA, 'TRIMA': TRIMA, 'WMA': WMA, 'CDL2CROWS': CDL2CROWS, 'CDL3BLACKCROWS': CDL3BLACKCROWS, 'CDL3INSIDE': CDL3INSIDE, 'CDL3LINESTRIKE': CDL3LINESTRIKE, 'CDL3OUTSIDE': CDL3OUTSIDE, 'CDL3STARSINSOUTH': CDL3STARSINSOUTH, 'CDL3WHITESOLDIERS': CDL3WHITESOLDIERS, 'CDLABANDONEDBABY': CDLABANDONEDBABY, 'CDLADVANCEBLOCK': CDLADVANCEBLOCK, 'CDLBELTHOLD': CDLBELTHOLD, 'CDLBREAKAWAY': CDLBREAKAWAY, 'CDLCLOSINGMARUBOZU': CDLCLOSINGMARUBOZU, 'CDLCONCEALBABYSWALL': CDLCONCEALBABYSWALL, 'CDLCOUNTERATTACK': CDLCOUNTERATTACK, 'CDLDARKCLOUDCOVER': CDLDARKCLOUDCOVER, 'CDLDOJI': CDLDOJI, 'CDLDOJISTAR': CDLDOJISTAR, 'CDLDRAGONFLYDOJI': CDLDRAGONFLYDOJI, 'CDLENGULFING': CDLENGULFING, 'CDLEVENINGDOJISTAR': CDLEVENINGDOJISTAR, 'CDLEVENINGSTAR': CDLEVENINGSTAR, 'CDLGAPSIDESIDEWHITE': CDLGAPSIDESIDEWHITE, 'CDLGRAVESTONEDOJI': CDLGRAVESTONEDOJI, 'CDLHAMMER': CDLHAMMER, 'CDLHANGINGMAN': CDLHANGINGMAN, 'CDLHARAMI': CDLHARAMI, 'CDLHARAMICROSS': CDLHARAMICROSS, 'CDLHIGHWAVE': CDLHIGHWAVE, 'CDLHIKKAKE': CDLHIKKAKE, 'CDLHIKKAKEMOD': CDLHIKKAKEMOD, 'CDLHOMINGPIGEON': CDLHOMINGPIGEON, 'CDLIDENTICAL3CROWS': CDLIDENTICAL3CROWS, 'CDLINNECK': CDLINNECK, 'CDLINVERTEDHAMMER': CDLINVERTEDHAMMER, 'CDLKICKING': CDLKICKING, 'CDLKICKINGBYLENGTH': CDLKICKINGBYLENGTH, 'CDLLADDERBOTTOM': CDLLADDERBOTTOM, 'CDLLONGLEGGEDDOJI': CDLLONGLEGGEDDOJI, 'CDLLONGLINE': CDLLONGLINE, 'CDLMARUBOZU': CDLMARUBOZU, 'CDLMATCHINGLOW': CDLMATCHINGLOW, 'CDLMATHOLD': CDLMATHOLD, 'CDLMORNINGDOJISTAR': CDLMORNINGDOJISTAR, 'CDLMORNINGSTAR': CDLMORNINGSTAR, 'CDLONNECK': CDLONNECK, 'CDLPIERCING': CDLPIERCING, 'CDLRICKSHAWMAN': CDLRICKSHAWMAN, 'CDLRISEFALL3METHODS': CDLRISEFALL3METHODS, 'CDLSEPARATINGLINES': CDLSEPARATINGLINES, 'CDLSHOOTINGSTAR': CDLSHOOTINGSTAR, 'CDLSHORTLINE': CDLSHORTLINE, 'CDLSPINNINGTOP': CDLSPINNINGTOP, 'CDLSTALLEDPATTERN': CDLSTALLEDPATTERN, 'CDLSTICKSANDWICH': CDLSTICKSANDWICH, 'CDLTAKURI': CDLTAKURI, 'CDLTASUKIGAP': CDLTASUKIGAP, 'CDLTHRUSTING': CDLTHRUSTING, 'CDLTRISTAR': CDLTRISTAR, 'CDLUNIQUE3RIVER': CDLUNIQUE3RIVER, 'CDLUPSIDEGAP2CROWS': CDLUPSIDEGAP2CROWS, 'CDLXSIDEGAP3METHODS': CDLXSIDEGAP3METHODS, 'AVGPRICE': AVGPRICE, 'MEDPRICE': MEDPRICE, 'TYPPRICE': TYPPRICE, 'WCLPRICE': WCLPRICE, 'BETA': BETA, 'CORREL': CORREL, 'LINEARREG': LINEARREG, 'LINEARREG_ANGLE': LINEARREG_ANGLE, 'LINEARREG_INTERCEPT': LINEARREG_INTERCEPT, 'LINEARREG_SLOPE': LINEARREG_SLOPE, 'STDDEV': STDDEV, 'TSF': TSF, 'VAR': VAR, 'ATR': ATR, 'NATR': NATR, 'TRANGE': TRANGE, 'AD': AD, 'ADOSC': ADOSC, 'OBV': OBV}
    keys_list = list(indicator_dict)
    legend = []
    
    for i in indicators:
        plt.figure(figsize=(20, 5), dpi=100)
        
        # CYCLE INDICATORS
        if i in keys_list[0:5]:
            ind = indicator_dict.get(i)
            for j in symbol:
                plot_ind = ind(close[j])
                plt.plot(plot_ind)
                legend.append(j)
        
        # MATH OPERATOR FUNCTIONS
        elif i in keys_list[5:7]:
            ind = indicator_dict.get(i)
            for j in symbol:
                plot_ind = ind(high[j], low[j])
                plt.plot(plot_ind)
                legend.append(j)
        elif i in keys_list[7:13]:
            ind = indicator_dict.get(i)
            for j in symbol:
                plot_ind = ind(close[j])
                plt.plot(plot_ind)
                legend.append(j)
        elif i in keys_list[13:15]:
            ind = indicator_dict.get(i)
            for j in symbol:
                plot_ind = ind(high[j], low[j])
                plt.plot(plot_ind)
                legend.append(j)
        elif i in keys_list[15]:
            ind = indicator_dict.get(i)
            for j in symbol:
                plot_ind = ind(close[j])
                plt.plot(plot_ind)
                legend.append(j)
        
                
        # MATH TRANSFORM FUNCTIONS
        elif i in keys_list[16:31]:
            ind = indicator_dict.get(i)
            for j in symbol:
                plot_ind = ind(close[j])
                plt.plot(plot_ind)
                legend.append(j)
        
        # MOMENTUM INDICATORS
        elif i in keys_list[31:33]:
            ind = indicator_dict.get(i)
            for j in symbol:
                plot_ind = ind(high[j], low[j], close[j])
                plt.plot(plot_ind)
                legend.append(j)
        elif i in keys_list[33]:
            ind = indicator_dict.get(i)
            for j in symbol:
                plot_ind = ind(close[j])
                plt.plot(plot_ind)
                legend.append(j)
        elif i in keys_list[34]:
            ind = indicator_dict.get(i)
            for j in symbol:
                aroondown, aroonup = ind(high[j], low[j])
                plt.plot(aroondown)
                plt.plot(aroonup)
                legend.append(j)
        elif i in keys_list[35]:
            ind = indicator_dict.get(i)
            for j in symbol:
                plot_ind = ind(high[j], low[j])
                plt.plot(plot_ind)
                legend.append(j)
        elif i in keys_list[36]:
            ind = indicator_dict.get(i)
            for j in symbol:
                plot_ind = ind(openprice[j], high[j], low[j], close[j])
                plt.plot(plot_ind)
                legend.append(j)
        elif i in keys_list[37]:
            ind = indicator_dict.get(i)
            for j in symbol:
                plot_ind = ind(high[j], low[j], close[j])
                plt.plot(plot_ind)
                legend.append(j)
        elif i in keys_list[38]:
            ind = indicator_dict.get(i)
            for j in symbol:
                plot_ind = ind(close[j])
                plt.plot(plot_ind)
                legend.append(j)
        elif i in keys_list[39]:
            ind = indicator_dict.get(i)
            for j in symbol:
                plot_ind = ind(high[j], low[j], close[j])
                plt.plot(plot_ind)
                legend.append(j)
        elif i in keys_list[40:43]:
            ind = indicator_dict.get(i)
            for j in symbol:
                macd, macdsignal, macdhist = ind(close[j])
                # plt.plot(macd)
                # plt.plot(macdsignal)
                plt.plot(macdhist)
                legend.append(j)
        elif i in keys_list[43]:
            ind = indicator_dict.get(i)
            for j in symbol:
                plot_ind = ind(high[j], low[j], close[j], volume[j])
                plt.plot(plot_ind)
                legend.append(j)
        elif i in keys_list[44]:
            ind = indicator_dict.get(i)
            for j in symbol:
                plot_ind = ind(high[j], low[j], close[j])
                plt.plot(plot_ind)
                legend.append(j)
        elif i in keys_list[45]:
            ind = indicator_dict.get(i)
            for j in symbol:
                plot_ind = ind(high[j], low[j])
                plt.plot(plot_ind)
                legend.append(j)
        elif i in keys_list[46]:
            ind = indicator_dict.get(i)
            for j in symbol:
                plot_ind = ind(close[j])
                plt.plot(plot_ind)
                legend.append(j)
        elif i in keys_list[47]:
            ind = indicator_dict.get(i)
            for j in symbol:
                plot_ind = ind(high[j], low[j], close[j])
                plt.plot(plot_ind)
                legend.append(j)
        elif i in keys_list[48]:
            ind = indicator_dict.get(i)
            for j in symbol:
                plot_ind = ind(high[j], low[j])
                plt.plot(plot_ind)
                legend.append(j)
        elif i in keys_list[49:55]:
            ind = indicator_dict.get(i)
            for j in symbol:
                plot_ind = ind(close[j])
                plt.plot(plot_ind)
                legend.append(j)
        elif i in keys_list[55]:
            ind = indicator_dict.get(i)
            for j in symbol:
                slowk, slowd = ind(high[j], low[j], close[j])
                plt.plot(slowk)
                plt.plot(slowd)
                legend.append(j)
        elif i in keys_list[56]:
            ind = indicator_dict.get(i)
            for j in symbol:
                fastk, fastd = ind(high[j], low[j], close[j])
                plt.plot(fastk)
                plt.plot(fastd)
                legend.append(j)
        # elif i in keys_list[57]:
        #     ind = indicator_dict.get(i)
        #     for j in symbol:
        #         fastk, fastd = ind(close[j])
        #         plt.plot(fastk)
        #         plt.plot(fastd)
        #         legend.append(j)
        elif i in keys_list[58]:
            ind = indicator_dict.get(i)
            for j in symbol:
                plot_ind = ind(close[j])
                plt.plot(plot_ind)
                legend.append(j)
        elif i in keys_list[59:61]:
            ind = indicator_dict.get(i)
            for j in symbol:
                plot_ind = ind(high[j], low[j], close[j])
                plt.plot(plot_ind)
                legend.append(j)
        
        # OVERLAP STUDIES FUNCTIONS
        elif i in keys_list[61]:
            ind = indicator_dict.get(i)
            for j in symbol:
                upperband, middleband, lowerband = ind(close[j])
                plt.plot(upperband)
                plt.plot(middleband)
                plt.plot(lowerband)
                legend.append(j)
        elif i in keys_list[62:68]:
            ind = indicator_dict.get(i)
            for j in symbol:
                plot_ind = ind(close[j])
                plt.plot(plot_ind)
                legend.append(j)
        elif i in keys_list[68]:
            ind = indicator_dict.get(i)
            for j in symbol:
                plot_ind = ind(close[j], periods)
                plt.plot(plot_ind)
                legend.append(j)
        elif i in keys_list[69]:
            ind = indicator_dict.get(i)
            for j in symbol:
                plot_ind = ind(close[j])
                plt.plot(plot_ind)
                legend.append(j)
        elif i in keys_list[70:73]:
            ind = indicator_dict.get(i)
            for j in symbol:
                plot_ind = ind(high[j], low[j])
                plt.plot(plot_ind)
                legend.append(j)
        elif i in keys_list[73:78]:
            ind = indicator_dict.get(i)
            for j in symbol:
                plot_ind = ind(close[j])
                plt.plot(plot_ind)
                legend.append(j)
        
        # PATTERN RECOGNITION FUNCTIONS
        elif i in keys_list[78:139]:
            ind = indicator_dict.get(i)
            for j in symbol:
                plot_ind = ind(openprice[j], high[j], low[j], close[j])
                plt.plot(plot_ind)
                legend.append(j)
                
        # PRICE TRANSFORM FUNCTIONS
        elif i in keys_list[139]:
            ind = indicator_dict.get(i)
            for j in symbol:
                plot_ind = ind(openprice[j], high[j], low[j], close[j])
                plt.plot(plot_ind)
                legend.append(j)
        elif i in keys_list[140]:
            ind = indicator_dict.get(i)
            for j in symbol:
                plot_ind = ind(high[j], low[j])
                plt.plot(plot_ind)
                legend.append(j)
        elif i in keys_list[141:143]:
            ind = indicator_dict.get(i)
            for j in symbol:
                plot_ind = ind(high[j], low[j], close[j])
                plt.plot(plot_ind)
                legend.append(j)
        
        # STATISTIC FUNCTIONS
        elif i in keys_list[143:145]:
            ind = indicator_dict.get(i)
            for j in symbol:
                plot_ind = ind(high[j], low[j])
                plt.plot(plot_ind)
                legend.append(j)
        elif i in keys_list[145:152]:
            ind = indicator_dict.get(i)
            for j in symbol:
                plot_ind = ind(close[j])
                plt.plot(plot_ind)
                legend.append(j)
    
        # VOLATILITY INDICATORS
        elif i in keys_list[152:155]:
            ind = indicator_dict.get(i)
            for j in symbol:
                plot_ind = ind(high[j], low[j], close[j])
                plt.plot(plot_ind)
                legend.append(j)
                
        # VOLUME INDICATORS
        elif i in keys_list[155:157]:
            ind = indicator_dict.get(i)
            for j in symbol:
                plot_ind = ind(high[j], low[j], close[j], volume[j])
                plt.plot(plot_ind)
                legend.append(j)
        elif i in keys_list[157]:
            ind = indicator_dict.get(i)
            for j in symbol:
                plot_ind = ind(close[j], volume[j])
                plt.plot(plot_ind)
                legend.append(j)

        plt.xlabel('Date')
        plt.ylabel(f'{i}')
        plt.title(f'{", ".join(symbol)} {i}')
        plt.legend(legend)
        plt.show()

plot_graphs()
