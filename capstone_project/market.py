import numpy as np
import pandas as pd

class Market():
    def __init__(self, dfdata):
        self.startdate = None
        self.enddate = None
        # init test /validation data
        self.reset(dfdata)

    def reset(self, dfdata):
        self.date = None  # set the minimum date from the dfdata
        self.stockprices = None # what is the current market price
        self.marketdata = dfdata
        self.done = False

    def next_timestep(self, rotor_speeds):
        self.stockprices = None
        self.date += self.dt
        if self.date > self.enddate:
            self.done = True
        return self.done
