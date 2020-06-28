# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 12:22:28 2020

@author: sayuj
"""

import pandas as pd
import pandas_datareader.data as web

import numpy as np

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import tkinter as tk

from talib._ta_lib import *
import talib

from datetime import datetime

# API key is being pulled from a seperate config.py file
import config

# Set today's date in order to pull stock data through current time
today = datetime.strftime(datetime.today(), "%Y-%m-%d")

class StockAnalysis(tk.Frame):
    
    """
    
    This class creates a GUI that features the ability for a user to choose
    any stock and graph its price data. It also allows for a user to choose
    a stock indicator from a provided dropdown menu in order to conduct
    the proper analysis for a stock and determine whether to buy or sell
    
    """
    
    def __init__(self, master=None):
        
        """
    
        Initialization function that sets up the GUI
    
        """
        self.tickers = []
        self.input_list = []
        
        tk.Frame.__init__(self, master)
        self.pack(fill='both', expand=1)
        self.createWidgets()
        
    def createWidgets(self):
        
        """
        
        Function that deploys all the widgets that will be seen in the GUI
        window, as well as the action that will occur upon interacting with
        the widget
        
        """
        
        master = tk.Tk()
        master.geometry("")
        self.variable = tk.StringVar(master)
        OPTIONS = dir(talib)
        self.variable.set(OPTIONS[0])
        
        stock_graph_title = tk.Label(master, text='Ticker').grid(row=0)
        self.entrybox = tk.Entry(master)
        self.entrybox.grid(row=1, column=0, sticky='NSEW')
        
        self.tickerButton = tk.Button(master, text='Graph', command=self.graphStock)
        self.tickerButton.grid(row=1, column=1, sticky='NSEW')
    
        indicator_graph_title = tk.Label(master, text='Indicator').grid(row=4, column=0)
        self.indicatorDropdown = tk.OptionMenu(master, self.variable, *OPTIONS)
        self.indicatorDropdown.grid(row=5, column=0, sticky='NSEW')
        
        self.indicatorButton = tk.Button(master, text='Graph', command=self.graphIndicator)
        self.indicatorButton.grid(row=5, column=1, sticky='NSEW')
        
        self.clearButton1 = tk.Button(master, text='Clear', command=self.clearGraph1)
        self.clearButton1.grid(row=1, column=2, sticky='NSEW')
        
        self.clearButton2 = tk.Button(master, text='Clear', command=self.clearGraph2)
        self.clearButton2.grid(row=5, column=2, sticky='NSEW')
        
        self.canvas1 = tk.Canvas(master, width=1000, height=300)
        self.canvas1.grid(row=3, column=0, columnspan=4)
        
        self.canvas2 = tk.Canvas(master, width=1000, height=300)
        self.canvas2.grid(row=7, column=0, columnspan=4)
    
    # The following function extracts stock data from a specific data source
    # (CSV, API, JSON, etc.)
    def getSymbols(self, symbol, data_source, begin_date=None, end_date=None):
        
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
        df = web.DataReader(symbol, data_source,begin_date, end_date, api_key=config.api_key)\
        [['AdjOpen','AdjHigh','AdjLow','AdjClose','AdjVolume']].reset_index()
        df.columns = ['Date','Open','High','Low',symbol,'Volume']
        df['Symbol'] = symbol
        df = df[::-1].reset_index()
        out = pd.concat([out,df],axis=0)
        return out.sort_index()


    def graphStock(self):
        
        """
        
        Function that graphs the user-inputted stock tickers from the
        provided entry box
        
        """
        
        try:
            self.can1.get_tk_widget().pack_forget()
        except AttributeError:
            pass
       
        # User-specified stock ticker will be the "symbols" input for the
        # "getSymbols" function
        user_entry = self.entrybox.get()
        self.input_list.append(user_entry)
        
        fig = Figure(figsize=(12,3), dpi=100) 
        graph = fig.add_subplot(111)
        
        i = 0
        
        # The following for loop pulls stock data for the chosen stocks and
        # creates a dataframe
        for symbol in self.input_list:
            self.df = self.getSymbols(symbol,data_source='quandl',\
                                 begin_date='2009-12-31',end_date=today)
                
            line = self.df[['Date', symbol]].groupby('Date').sum()
            line.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
            graph.set_title(f'{", ".join(self.input_list)} stock price')
            graph.set_ylabel('USD')
            i += 1
        
        # The following creates the graph in the blank canvas
        self.can1 = FigureCanvasTkAgg(fig, self.canvas1)
        self.can1.get_tk_widget().pack(side="top",fill='both',expand=True)
        
    def graphIndicator(self):
        
        """
        
        Function that graphs thh user-chosen indicator from the provided
        dropdown. All indicators follow default parameters (see TA-Lib
        documentation for further information)
        
        """
        
        try:
            self.can2.get_tk_widget().pack_forget()
        except AttributeError:
            pass
        
        indicator = self.variable.get()
        # Dictionary of all functions from the TA-Lib library
        indicator_dict = {'HT_DCPERIOD': HT_DCPERIOD, 'HT_DCPHASE': HT_DCPHASE, 'HT_PHASOR': HT_PHASOR, 'HT_SINE': HT_SINE, 'HT_TRENDMODE': HT_TRENDMODE, 'ADD': ADD, 'DIV': DIV, 'MAX': MAX, 'MAXINDEX': MAXINDEX, 'MIN': MIN, 'MININDEX': MININDEX, 'MINMAX': MINMAX, 'MINMAXINDEX': MINMAXINDEX, 'MULT': MULT, 'SUB': SUB, 'SUM': SUM, 'ACOS': ACOS, 'ASIN': ASIN, 'ATAN': ATAN, 'CEIL': CEIL, 'COS': COS, 'COSH': COSH, 'EXP': EXP, 'FLOOR': FLOOR, 'LN': LN, 'LOG10': LOG10, 'SIN': SIN, 'SINH': SINH, 'SQRT': SQRT, 'TAN': TAN, 'TANH': TANH, 'ADX': ADX, 'ADXR': ADXR, 'APO': APO, 'AROON': AROON, 'AROONOSC': AROONOSC, 'BOP': BOP, 'CCI': CCI, 'CMO': CMO, 'DX': DX, 'MACD': MACD, 'MACDEXT': MACDEXT, 'MACDFIX': MACDFIX, 'MFI': MFI, 'MINUS_DI': MINUS_DI, 'MINUS_DM': MINUS_DM, 'MOM': MOM, 'PLUS_DI': PLUS_DI, 'PLUS_DM': PLUS_DM, 'PPO': PPO, 'ROC': ROC, 'ROCP': ROCP, 'ROCR': ROCR, 'ROCR100': ROCR100, 'RSI': RSI, 'STOCH': STOCH, 'STOCHF': STOCHF, 'STOCHRSI': STOCHRSI, 'TRIX': TRIX, 'ULTOSC': ULTOSC, 'WILLR': WILLR, 'BBANDS': BBANDS, 'DEMA': DEMA, 'EMA': EMA, 'HT_TRENDLINE': HT_TRENDLINE, 'KAMA': KAMA, 'MA': MA, 'MAMA': MAMA, 'MAVP': MAVP, 'MIDPOINT': MIDPOINT, 'MIDPRICE': MIDPRICE, 'SAR': SAR, 'SAREXT': SAREXT, 'SMA': SMA, 'T3': T3, 'TEMA': TEMA, 'TRIMA': TRIMA, 'WMA': WMA, 'CDL2CROWS': CDL2CROWS, 'CDL3BLACKCROWS': CDL3BLACKCROWS, 'CDL3INSIDE': CDL3INSIDE, 'CDL3LINESTRIKE': CDL3LINESTRIKE, 'CDL3OUTSIDE': CDL3OUTSIDE, 'CDL3STARSINSOUTH': CDL3STARSINSOUTH, 'CDL3WHITESOLDIERS': CDL3WHITESOLDIERS, 'CDLABANDONEDBABY': CDLABANDONEDBABY, 'CDLADVANCEBLOCK': CDLADVANCEBLOCK, 'CDLBELTHOLD': CDLBELTHOLD, 'CDLBREAKAWAY': CDLBREAKAWAY, 'CDLCLOSINGMARUBOZU': CDLCLOSINGMARUBOZU, 'CDLCONCEALBABYSWALL': CDLCONCEALBABYSWALL, 'CDLCOUNTERATTACK': CDLCOUNTERATTACK, 'CDLDARKCLOUDCOVER': CDLDARKCLOUDCOVER, 'CDLDOJI': CDLDOJI, 'CDLDOJISTAR': CDLDOJISTAR, 'CDLDRAGONFLYDOJI': CDLDRAGONFLYDOJI, 'CDLENGULFING': CDLENGULFING, 'CDLEVENINGDOJISTAR': CDLEVENINGDOJISTAR, 'CDLEVENINGSTAR': CDLEVENINGSTAR, 'CDLGAPSIDESIDEWHITE': CDLGAPSIDESIDEWHITE, 'CDLGRAVESTONEDOJI': CDLGRAVESTONEDOJI, 'CDLHAMMER': CDLHAMMER, 'CDLHANGINGMAN': CDLHANGINGMAN, 'CDLHARAMI': CDLHARAMI, 'CDLHARAMICROSS': CDLHARAMICROSS, 'CDLHIGHWAVE': CDLHIGHWAVE, 'CDLHIKKAKE': CDLHIKKAKE, 'CDLHIKKAKEMOD': CDLHIKKAKEMOD, 'CDLHOMINGPIGEON': CDLHOMINGPIGEON, 'CDLIDENTICAL3CROWS': CDLIDENTICAL3CROWS, 'CDLINNECK': CDLINNECK, 'CDLINVERTEDHAMMER': CDLINVERTEDHAMMER, 'CDLKICKING': CDLKICKING, 'CDLKICKINGBYLENGTH': CDLKICKINGBYLENGTH, 'CDLLADDERBOTTOM': CDLLADDERBOTTOM, 'CDLLONGLEGGEDDOJI': CDLLONGLEGGEDDOJI, 'CDLLONGLINE': CDLLONGLINE, 'CDLMARUBOZU': CDLMARUBOZU, 'CDLMATCHINGLOW': CDLMATCHINGLOW, 'CDLMATHOLD': CDLMATHOLD, 'CDLMORNINGDOJISTAR': CDLMORNINGDOJISTAR, 'CDLMORNINGSTAR': CDLMORNINGSTAR, 'CDLONNECK': CDLONNECK, 'CDLPIERCING': CDLPIERCING, 'CDLRICKSHAWMAN': CDLRICKSHAWMAN, 'CDLRISEFALL3METHODS': CDLRISEFALL3METHODS, 'CDLSEPARATINGLINES': CDLSEPARATINGLINES, 'CDLSHOOTINGSTAR': CDLSHOOTINGSTAR, 'CDLSHORTLINE': CDLSHORTLINE, 'CDLSPINNINGTOP': CDLSPINNINGTOP, 'CDLSTALLEDPATTERN': CDLSTALLEDPATTERN, 'CDLSTICKSANDWICH': CDLSTICKSANDWICH, 'CDLTAKURI': CDLTAKURI, 'CDLTASUKIGAP': CDLTASUKIGAP, 'CDLTHRUSTING': CDLTHRUSTING, 'CDLTRISTAR': CDLTRISTAR, 'CDLUNIQUE3RIVER': CDLUNIQUE3RIVER, 'CDLUPSIDEGAP2CROWS': CDLUPSIDEGAP2CROWS, 'CDLXSIDEGAP3METHODS': CDLXSIDEGAP3METHODS, 'AVGPRICE': AVGPRICE, 'MEDPRICE': MEDPRICE, 'TYPPRICE': TYPPRICE, 'WCLPRICE': WCLPRICE, 'BETA': BETA, 'CORREL': CORREL, 'LINEARREG': LINEARREG, 'LINEARREG_ANGLE': LINEARREG_ANGLE, 'LINEARREG_INTERCEPT': LINEARREG_INTERCEPT, 'LINEARREG_SLOPE': LINEARREG_SLOPE, 'STDDEV': STDDEV, 'TSF': TSF, 'VAR': VAR, 'ATR': ATR, 'NATR': NATR, 'TRANGE': TRANGE, 'AD': AD, 'ADOSC': ADOSC, 'OBV': OBV}
        keys_list = list(indicator_dict)
        
        legend = []
        
        fig = Figure(figsize=(12,2.5), dpi=100) 
        graph = fig.add_subplot(111)
            
        i = 0
        
        # The following for loop pulls stock data for the chosen stocks and
        # creates a dataframe
        for symbol in self.input_list:
            self.df = self.getSymbols(symbol,data_source='quandl',\
                                 begin_date='2009-12-31',end_date=today)
            openprice = self.df['Open']
            high = self.df['High']
            low = self.df['Low']
            volume= self.df['Volume']
            periods = 30
            close = self.df[symbol]
            
            # The following if statements are necessary to pull the chosen
            # indicator and plot the line based on its specific function
            # parameters
            
            # CYCLE INDICATORS
            if indicator in keys_list[0:5]:
                ind = indicator_dict.get(indicator)
                line = ind(close)
                line.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                legend.append(symbol)
                i += 1
            
            # MATH OPERATOR FUNCTIONS
            elif indicator in keys_list[5:7]:
                ind = indicator_dict.get(indicator)
                line = ind(high,low)
                line.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                legend.append(symbol)
                i += 1
            elif indicator in keys_list[7:13]:
                ind = indicator_dict.get(indicator)
                line = ind(close)
                line.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                legend.append(symbol)
                i += 1
            elif indicator in keys_list[13:15]:
                ind = indicator_dict.get(indicator)
                line = ind(high,low)
                line.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                legend.append(symbol)
                i += 1
            elif indicator in keys_list[15]:
                ind = indicator_dict.get(indicator)
                line = ind(close)
                line.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                legend.append(symbol)
                i += 1
            
            # MATH TRANSFORM FUNCTIONS
            elif indicator in keys_list[16:31]:
                ind = indicator_dict.get(indicator)
                line = ind(close)
                line.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                legend.append(symbol)
                i += 1
            
            # MOMENTUM INDICATORS
            elif indicator in keys_list[31:33]:
                ind = indicator_dict.get(indicator)
                line = ind(high, low, close)
                line.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                legend.append(symbol)
                i += 1
            elif indicator in keys_list[33]:
                ind = indicator_dict.get(indicator)
                line = ind(close)
                line.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                legend.append(symbol)
                i += 1
            elif indicator in keys_list[34]:
                ind = indicator_dict.get(indicator)
                aroondown, aroonup = ind(high, low)
                aroondown.plot(kind='line', legend=True, ax=graph, color=f'C{i+1}', fontsize=10)
                aroonup.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                legend.append(symbol)
                i += 1
            elif indicator in keys_list[35]:
                ind = indicator_dict.get(indicator)
                line = ind(high, low)
                line.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                legend.append(symbol)
                i += 1
            elif indicator in keys_list[36]:
                ind = indicator_dict.get(indicator)
                line = ind(openprice, high, low, close)
                line.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                legend.append(symbol)
                i += 1
            elif indicator in keys_list[37]:
                ind = indicator_dict.get(indicator)
                line = ind(openprice, high, low, close)
                line.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                legend.append(symbol)
                i += 1
            elif indicator in keys_list[38]:
                ind = indicator_dict.get(indicator)
                line = ind(close)
                line.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                legend.append(symbol)
                i += 1
            elif indicator in keys_list[39]:
                ind = indicator_dict.get(indicator)
                line = ind(high, low, close)
                line.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                legend.append(symbol)
                i += 1
            elif indicator in keys_list[40:43]:
                ind = indicator_dict.get(indicator)
                macd, macdsignal, macdhist = ind(close)
                # macd.plot(kind='line', legend=True, ax=graph, color=f'C{i+2}', fontsize=10)
                # macdsignal.plot(kind='line', legend=True, ax=graph, color=f'C{i+1}', fontsize=10)
                macdhist.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                legend.append(symbol)
                i += 1
            elif indicator in keys_list[43]:
                ind = indicator_dict.get(indicator)
                line = ind(high, low, close, volume)
                line.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                legend.append(symbol)
                i += 1
            elif indicator in keys_list[44]:
                ind = indicator_dict.get(indicator)
                line = ind(high, low, close)
                line.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                legend.append(symbol)
                i += 1
            elif indicator in keys_list[45]:
                ind = indicator_dict.get(indicator)
                line = ind(high, low)
                line.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                legend.append(symbol)
                i += 1
            elif indicator in keys_list[46]:
                ind = indicator_dict.get(indicator)
                line = ind(close)
                line.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                legend.append(symbol)
                i += 1
            elif indicator in keys_list[47]:
                ind = indicator_dict.get(indicator)
                line = ind(high, low, close)
                line.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                legend.append(symbol)
                i += 1
            elif indicator in keys_list[48]:
                ind = indicator_dict.get(indicator)
                line = ind(high, low)
                line.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                legend.append(symbol)
                i += 1
            elif indicator in keys_list[49:55]:
                ind = indicator_dict.get(indicator)
                line = ind(close)
                line.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                legend.append(symbol)
                i += 1
            elif indicator in keys_list[55]:
                ind = indicator_dict.get(indicator)
                slowk, slowd = ind(high, low, close)
                slowk.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                slowd.plot(kind='line', legend=True, ax=graph, color=f'C{i+1}', fontsize=10)
                legend.append(symbol)
                i += 1
            elif indicator in keys_list[56]:
                ind = indicator_dict.get(indicator)
                fastk, fastd = ind(high, low, close)
                fastk.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                fastd.plot(kind='line', legend=True, ax=graph, color=f'C{i+1}', fontsize=10)
                legend.append(symbol)
                i += 1
            # elif indicator in keys_list[57]:
            #     ind = indicator_dict.get(indicator)
            #     fastk, fastd = ind(high, low, close)
            #     fastk.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
            #     fastd.plot(kind='line', legend=True, ax=graph, color=f'C{i+1}', fontsize=10)
            #     legend.append(symbol)
            #     i += 1
            elif indicator in keys_list[58]:
                ind = indicator_dict.get(indicator)
                line = ind(close)
                line.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                legend.append(symbol)
                i += 1
            elif indicator in keys_list[59:61]:
                ind = indicator_dict.get(indicator)
                line = ind(high, low, close)
                line.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                legend.append(symbol)
                i += 1
            
            # OVERLAP STUDIES FUNCTIONS
            elif indicator in keys_list[61]:
                ind = indicator_dict.get(indicator)
                upperband, middleband, lowerband = ind(close)
                upperband.plot(kind='line', legend=True, ax=graph, color=f'C{i+1}', fontsize=10)
                middleband.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                lowerband.plot(kind='line', legend=True, ax=graph, color=f'C{i+1}', fontsize=10)
                legend.append(symbol)
                i += 1
            elif indicator in keys_list[62:68]:
                ind = indicator_dict.get(indicator)
                line = ind(close)
                line.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                legend.append(symbol)
                i += 1
            elif indicator in keys_list[68]:
                ind = indicator_dict.get(indicator)
                line = ind(close, periods)
                line.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                legend.append(symbol)
                i += 1
            elif indicator in keys_list[69]:
                ind = indicator_dict.get(indicator)
                line = ind(close)
                line.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                legend.append(symbol)
                i += 1
            elif indicator in keys_list[70:73]:
                ind = indicator_dict.get(indicator)
                line = ind(high, low)
                line.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                legend.append(symbol)
                i += 1
            elif indicator in keys_list[73:78]:
                ind = indicator_dict.get(indicator)
                line = ind(close)
                line.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                legend.append(symbol)
                i += 1
            
            # PATTERN RECOGNITION FUNCTIONS
            elif indicator in keys_list[78:139]:
                ind = indicator_dict.get(indicator)
                line = ind(openprice, high, low, close)
                line.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                legend.append(symbol)
                i += 1
                
            # PRICE TRANSFORM FUNCTIONS
            elif indicator in keys_list[139]:
                ind = indicator_dict.get(indicator)
                line = ind(openprice, high, low, close)
                line.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                legend.append(symbol)
                i += 1
            elif indicator in keys_list[140]:
                ind = indicator_dict.get(indicator)
                line = ind(high, low)
                line.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                legend.append(symbol)
                i += 1
            elif indicator in keys_list[141:143]:
                ind = indicator_dict.get(indicator)
                line = ind(high, low, close)
                line.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                legend.append(symbol)
                i += 1
            
            # STATISTIC FUNCTIONS
            elif indicator in keys_list[143:145]:
                ind = indicator_dict.get(indicator)
                line = ind(high, low)
                line.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                legend.append(symbol)
                i += 1
            elif indicator in keys_list[145:152]:
                ind = indicator_dict.get(indicator)
                line = ind(close)
                line.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                legend.append(symbol)
                i += 1
            
            # VOLATILITY INDICATORS
            elif indicator in keys_list[152:155]:
                ind = indicator_dict.get(indicator)
                line = ind(high, low, close)
                line.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                legend.append(symbol)
                i += 1
                
            # VOLUME INDICATORS
            elif indicator in keys_list[155:157]:
                ind = indicator_dict.get(indicator)
                line = ind(high, low, close, volume)
                line.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                legend.append(symbol)
                i += 1
            elif indicator in keys_list[157]:
                ind = indicator_dict.get(indicator)
                line = ind(close, volume)
                line.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
                legend.append(symbol)
                i += 1
    
            graph.set_title(f'{", ".join(self.input_list)} {indicator}')
            graph.set_ylabel('USD')
            graph.set_xlabel('Date')
            graph.legend(legend)
                
        # The following creates the graph in the blank canvas
        self.can2 = FigureCanvasTkAgg(fig, self.canvas2)
        self.can2.get_tk_widget().pack(side="top",fill='both',expand=True)
    
    def clearGraph1(self):
        
        """
        
        Function that clears the stock graph upon clicking the "Clear" button
        
        """
        
        self.can1.get_tk_widget().pack_forget()
        self.input_list = []
    
    def clearGraph2(self):
        
        """
        
        Function that clears the indicator graph upon clicking the "Clear"
        button
        
        """
        
        self.can2.get_tk_widget().pack_forget()    
    
# The following initiates the program
app = StockAnalysis(tk.Tk())
app.mainloop()
