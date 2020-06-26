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

# Set today's date in order to pull stock data through current time
today = datetime.strftime(datetime.today(), "%Y-%m-%d")

class StockAnalysis(tk.Frame):
    
    def __init__(self, master=None):    
        self.tickers = []
        self.input_list = []
        
        tk.Frame.__init__(self, master)
        self.pack(fill='both', expand=1)
        self.createWidgets()
        
    def createWidgets(self):
        master = tk.Tk()
        master.geometry("")
        self.variable = tk.StringVar(master)
        OPTIONS = dir(talib)
        self.variable.set(OPTIONS[0])
        
        stock_graph_title = tk.Label(master, text='Ticker').grid(row=0)
        self.entrybox = tk.Entry(master)
        self.entrybox.grid(row=1, column=0, sticky='NSEW')
        
        self.tickerButton = tk.Button(master, text='Graph', command=self.graphStock)
        self.tickerButton.grid(row=2, column=0, sticky='NSEW')
    
        indicator_graph_title = tk.Label(master, text='Indicator').grid(row=4, column=0)
        self.indicatorDropdown = tk.OptionMenu(master, self.variable, *OPTIONS)
        self.indicatorDropdown.grid(row=5, column=0, sticky='NSEW')
        
        self.indicatorButton = tk.Button(master, text='Graph')
        self.indicatorButton['command'] = self.graphIndicator
        self.indicatorButton.grid(row=6, column=0, sticky='NSEW')
        
        self.clearButton1 = tk.Button(master, text='Clear')
        self.clearButton1.grid(row=2, column=1, sticky='NSEW')
        
        self.clearButton2 = tk.Button(master, text='Clear')
        self.clearButton2.grid(row=5, column=1, sticky='NSEW')
        
        self.canvas1 = tk.Canvas(master, width=1000, height=250)
        self.canvas1.grid(row=3, column=0, columnspan=3)
        
        self.canvas2 = tk.Canvas(master, width=1000, height=250)
        self.canvas2.grid(row=7, column=0, columnspan=3)
    
    # Create the function to extract data from a specific data sources (CSV, API, JSON, etc.)
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
        df = web.DataReader(symbol, data_source,begin_date, end_date, api_key="""INSERT YOUR API KEY HERE""")\
        [['AdjOpen','AdjHigh','AdjLow','AdjClose','AdjVolume']].reset_index()
        df.columns = ['Date','Open','High','Low',symbol,'Volume'] #my convention: always lowercase
        df['Symbol'] = symbol # add a new column which contains the symbol so we can keep multiple symbols in the same dataframe
        df = df[::-1].reset_index()
        out = pd.concat([out,df],axis=0) #stacks on top of previously collected data
        return out.sort_index()
    
    # def input_ticker(self):
    #     """
        
    #     Function that allows for a user to input as many stock tickers they would like to extract data for
        
    #     """

    #     self.ticker = self.tickers.append(self.inputTicker)
        
    #     return self.ticker

    def graphStock(self):
        try:
            self.can1.get_tk_widget().pack_forget()
        except AttributeError:
            pass
       
        # User-specified stock ticker will be the "symbols" input for the "getSymbols" function
        user_entry = self.entrybox.get()
        self.input_list.append(user_entry)
        
        fig = Figure(figsize=(10,2), dpi=100) 
        graph = fig.add_subplot(111)
        
        i = 0
        for symbol in self.input_list:
            # Call the function and assign the returned dataframe object to a variable
            self.df = self.getSymbols(symbol,data_source='quandl',\
                                 begin_date='2009-12-31',end_date=today)
                
            line = self.df[['Date', symbol]].groupby('Date').sum()
            line.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
            graph.set_title(f'{", ".join(self.input_list)} stock price')
            graph.set_ylabel('USD')
            i += 1
            
        self.can1 = FigureCanvasTkAgg(fig, self.canvas1)
        self.can1.get_tk_widget().pack(side="top",fill='both',expand=True)
        
    def graphIndicator(self):
        """
        
        Function that allows user to input what technical analysis indicator they would like to use for their analysis
        
        """
        
        try:
            self.can2.get_tk_widget().pack_forget()
        except AttributeError:
            pass
        
        indicator = self.variable.get()
        indicator_dict = {'HT_DCPERIOD': HT_DCPERIOD, 'HT_DCPHASE': HT_DCPHASE, 'HT_PHASOR': HT_PHASOR, 'HT_SINE': HT_SINE, 'HT_TRENDMODE': HT_TRENDMODE, 'ADD': ADD, 'DIV': DIV, 'MAX': MAX, 'MAXINDEX': MAXINDEX, 'MIN': MIN, 'MININDEX': MININDEX, 'MINMAX': MINMAX, 'MINMAXINDEX': MINMAXINDEX, 'MULT': MULT, 'SUB': SUB, 'SUM': SUM, 'ACOS': ACOS, 'ASIN': ASIN, 'ATAN': ATAN, 'CEIL': CEIL, 'COS': COS, 'COSH': COSH, 'EXP': EXP, 'FLOOR': FLOOR, 'LN': LN, 'LOG10': LOG10, 'SIN': SIN, 'SINH': SINH, 'SQRT': SQRT, 'TAN': TAN, 'TANH': TANH, 'ADX': ADX, 'ADXR': ADXR, 'APO': APO, 'AROON': AROON, 'AROONOSC': AROONOSC, 'BOP': BOP, 'CCI': CCI, 'CMO': CMO, 'DX': DX, 'MACD': MACD, 'MACDEXT': MACDEXT, 'MACDFIX': MACDFIX, 'MFI': MFI, 'MINUS_DI': MINUS_DI, 'MINUS_DM': MINUS_DM, 'MOM': MOM, 'PLUS_DI': PLUS_DI, 'PLUS_DM': PLUS_DM, 'PPO': PPO, 'ROC': ROC, 'ROCP': ROCP, 'ROCR': ROCR, 'ROCR100': ROCR100, 'RSI': RSI, 'STOCH': STOCH, 'STOCHF': STOCHF, 'STOCHRSI': STOCHRSI, 'TRIX': TRIX, 'ULTOSC': ULTOSC, 'WILLR': WILLR, 'BBANDS': BBANDS, 'DEMA': DEMA, 'EMA': EMA, 'HT_TRENDLINE': HT_TRENDLINE, 'KAMA': KAMA, 'MA': MA, 'MAMA': MAMA, 'MAVP': MAVP, 'MIDPOINT': MIDPOINT, 'MIDPRICE': MIDPRICE, 'SAR': SAR, 'SAREXT': SAREXT, 'SMA': SMA, 'T3': T3, 'TEMA': TEMA, 'TRIMA': TRIMA, 'WMA': WMA, 'CDL2CROWS': CDL2CROWS, 'CDL3BLACKCROWS': CDL3BLACKCROWS, 'CDL3INSIDE': CDL3INSIDE, 'CDL3LINESTRIKE': CDL3LINESTRIKE, 'CDL3OUTSIDE': CDL3OUTSIDE, 'CDL3STARSINSOUTH': CDL3STARSINSOUTH, 'CDL3WHITESOLDIERS': CDL3WHITESOLDIERS, 'CDLABANDONEDBABY': CDLABANDONEDBABY, 'CDLADVANCEBLOCK': CDLADVANCEBLOCK, 'CDLBELTHOLD': CDLBELTHOLD, 'CDLBREAKAWAY': CDLBREAKAWAY, 'CDLCLOSINGMARUBOZU': CDLCLOSINGMARUBOZU, 'CDLCONCEALBABYSWALL': CDLCONCEALBABYSWALL, 'CDLCOUNTERATTACK': CDLCOUNTERATTACK, 'CDLDARKCLOUDCOVER': CDLDARKCLOUDCOVER, 'CDLDOJI': CDLDOJI, 'CDLDOJISTAR': CDLDOJISTAR, 'CDLDRAGONFLYDOJI': CDLDRAGONFLYDOJI, 'CDLENGULFING': CDLENGULFING, 'CDLEVENINGDOJISTAR': CDLEVENINGDOJISTAR, 'CDLEVENINGSTAR': CDLEVENINGSTAR, 'CDLGAPSIDESIDEWHITE': CDLGAPSIDESIDEWHITE, 'CDLGRAVESTONEDOJI': CDLGRAVESTONEDOJI, 'CDLHAMMER': CDLHAMMER, 'CDLHANGINGMAN': CDLHANGINGMAN, 'CDLHARAMI': CDLHARAMI, 'CDLHARAMICROSS': CDLHARAMICROSS, 'CDLHIGHWAVE': CDLHIGHWAVE, 'CDLHIKKAKE': CDLHIKKAKE, 'CDLHIKKAKEMOD': CDLHIKKAKEMOD, 'CDLHOMINGPIGEON': CDLHOMINGPIGEON, 'CDLIDENTICAL3CROWS': CDLIDENTICAL3CROWS, 'CDLINNECK': CDLINNECK, 'CDLINVERTEDHAMMER': CDLINVERTEDHAMMER, 'CDLKICKING': CDLKICKING, 'CDLKICKINGBYLENGTH': CDLKICKINGBYLENGTH, 'CDLLADDERBOTTOM': CDLLADDERBOTTOM, 'CDLLONGLEGGEDDOJI': CDLLONGLEGGEDDOJI, 'CDLLONGLINE': CDLLONGLINE, 'CDLMARUBOZU': CDLMARUBOZU, 'CDLMATCHINGLOW': CDLMATCHINGLOW, 'CDLMATHOLD': CDLMATHOLD, 'CDLMORNINGDOJISTAR': CDLMORNINGDOJISTAR, 'CDLMORNINGSTAR': CDLMORNINGSTAR, 'CDLONNECK': CDLONNECK, 'CDLPIERCING': CDLPIERCING, 'CDLRICKSHAWMAN': CDLRICKSHAWMAN, 'CDLRISEFALL3METHODS': CDLRISEFALL3METHODS, 'CDLSEPARATINGLINES': CDLSEPARATINGLINES, 'CDLSHOOTINGSTAR': CDLSHOOTINGSTAR, 'CDLSHORTLINE': CDLSHORTLINE, 'CDLSPINNINGTOP': CDLSPINNINGTOP, 'CDLSTALLEDPATTERN': CDLSTALLEDPATTERN, 'CDLSTICKSANDWICH': CDLSTICKSANDWICH, 'CDLTAKURI': CDLTAKURI, 'CDLTASUKIGAP': CDLTASUKIGAP, 'CDLTHRUSTING': CDLTHRUSTING, 'CDLTRISTAR': CDLTRISTAR, 'CDLUNIQUE3RIVER': CDLUNIQUE3RIVER, 'CDLUPSIDEGAP2CROWS': CDLUPSIDEGAP2CROWS, 'CDLXSIDEGAP3METHODS': CDLXSIDEGAP3METHODS, 'AVGPRICE': AVGPRICE, 'MEDPRICE': MEDPRICE, 'TYPPRICE': TYPPRICE, 'WCLPRICE': WCLPRICE, 'BETA': BETA, 'CORREL': CORREL, 'LINEARREG': LINEARREG, 'LINEARREG_ANGLE': LINEARREG_ANGLE, 'LINEARREG_INTERCEPT': LINEARREG_INTERCEPT, 'LINEARREG_SLOPE': LINEARREG_SLOPE, 'STDDEV': STDDEV, 'TSF': TSF, 'VAR': VAR, 'ATR': ATR, 'NATR': NATR, 'TRANGE': TRANGE, 'AD': AD, 'ADOSC': ADOSC, 'OBV': OBV}
    
        ind = indicator_dict.get(indicator)
        
        fig = Figure(figsize=(10,2), dpi=100) 
        graph = fig.add_subplot(111)
        
        legend = []
        
        i = 0
        for j in self.input_list:
            line = ind(self.df[j])
            line.plot(kind='line', legend=True, ax=graph, color=f'C{i}', fontsize=10)
            graph.set_title(f'{", ".join(self.input_list)} {indicator}')
            graph.set_ylabel('USD')
            graph.set_xlabel('Date')
            legend.append(j)
            graph.legend(legend)
            i += 1
        
        self.can2 = FigureCanvasTkAgg(fig, self.canvas2)
        self.can2.get_tk_widget().pack(side="top",fill='both',expand=True)
        
app = StockAnalysis(tk.Tk())
app.mainloop()
