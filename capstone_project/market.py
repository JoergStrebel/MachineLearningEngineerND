import numpy as np
import pandas as pd


class Market:
    """
    A class that models the market and stores the stock prices for a certain time interval
    Trading is only possible on trading days, i.e. when the stock exchange is in session.
    Therefore, the class does not track dates but indices on the input data frame.

    data structure: dataframe with the following columns
    ['date','dayofweek','month','dayno','monthstart','SP500_price', 'SP500_volno', \
    'ESTOXX_price', 'ESTOXX_volno', 'MSCI_price', 'MSCI_volno', 'US_rate']

    """
    def __init__(self, dfdata: pd.DataFrame):
        self.startdate = np.min(dfdata['date'])
        self.enddate = np.max(dfdata['date'])
        self.notradingdays = dfdata.shape[0]
        self.currentdate = 0

        self.stockprices = dfdata.iloc[self.currentdate]  # what is the current market price
        self.marketdata = dfdata
        self.done = False

    def reset(self):
        self.currentdate = 0
        self.stockprices = self.marketdata.iloc[self.currentdate]  # what is the current market price
        self.done = False

    def next_timestep(self):
        """ Get the stock price for the next day"""
        self.currentdate += 1
        if self.currentdate >= self.notradingdays:
            self.done = True
        return self.done

    def get_value(self, symbol):
        """symbol can be a list of columns"""
        return self.marketdata.iloc[self.currentdate][symbol]

    def get_last_values(self, symbol, no):
        return self.marketdata[symbol][self.currentdate-no:self.currentdate]