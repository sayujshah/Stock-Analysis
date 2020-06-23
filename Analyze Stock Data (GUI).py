# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 12:22:28 2020

@author: sayuj
"""

import pandas as pd
from pandas.util.testing import assert_frame_equal
import pandas_datareader.data as web

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import tkinter as tk

from datetime import datetime

import talib


# Set today's date in order to pull stock data through current time
today = datetime.strftime(datetime.today(), "%Y-%m-%d")

class StockAnalysis(tk.Frame):
    
    def __init__(self, master=None):    
        self.tickers = []
        
        tk.Frame.__init__(self, master)
        master.minsize(width=0, height=350)
        master.maxsize(width=1000, height=1000)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        master = tk.Tk()
        variable = tk.StringVar(master)
        OPTIONS = dir(talib)
        
        self.inputTicker = tk.Label(master, text="Ticker").grid(row=0)
        self.entrybox = tk.Entry(master)
        self.entrybox.grid(row=1, column=0)
        
        self.tickerButton = tk.Button(master, text='Graph', command=self.graphStock)
        self.tickerButton.grid(row=2, column=0, sticky='NSEW')
    
        self.indicatorDropdown = tk.OptionMenu(master, variable, *OPTIONS)
        self.indicatorDropdown.grid(row=1, column=1)
        
        self.indicatorButton = tk.Button(master, text='Graph')
        # self.indicatorButton['command'] = self.graphIndicator
        self.indicatorButton.grid(row=2, column=1, sticky='NSEW')
    
    # Create the function to extract data from a specific data sources (CSV, API, JSON, etc.)
    def get_symbols(self, symbol, data_source, begin_date=None, end_date=None):
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
        df = web.DataReader(symbol, data_source,begin_date, end_date, api_key=""""<input your api key here>""")\
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
        
        # User-specified stock ticker will be the "symbols" input for the "get_symbols" function
        symbol = self.entrybox.get()
        
        # Call the function and assign the returned dataframe object to a variable
        df = self.get_symbols(symbol,data_source='quandl',\
                             begin_date='2009-12-31',end_date=today)
                
        root = tk.Tk()
        
        fig = Figure(figsize=(14,5), dpi=100) 
        graph = fig.add_subplot(111)
        
        plt.plot(df['Date'], df[symbol], label=symbol + ' stock')
        plt.xlabel('Date')
        plt.ylabel('USD')
        plt.title('Figure 2: ' + symbol + ' stock price')
        plt.legend()
        plt.show()
        
        canvas = FigureCanvasTkAgg(fig, root)
        canvas.get_tk_widget().pack(side="top",fill='both',expand=True)
        
        root.mainloop()
        
    # def graphIndicator(self):
    #     """
        
    #     Function that allows user to input what technical analysis indicator they would like to use for their analysis
        
    #     """

app = StockAnalysis(tk.Tk())
app.mainloop()