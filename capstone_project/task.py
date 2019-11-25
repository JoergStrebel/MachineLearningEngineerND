import numpy as np
from  market import Market
import pandas as pd

class Task():
    """
    Task (environment) that defines the goal and provides feedback to the agent.
    In this project, the class Task can be seen as the bank or broker of the agent, i.e. a facility by which the agent
    interacts with the stock market.
    The task environment also enforces the budget constraints (like a bank or a broker) and tracks the portfolio of the
    agent.
    The task also creates and tracks the state. THe state is defined according to
    https://teddykoker.com/2019/06/trading-with-reinforcement-learning-in-python-part-ii-application/ as a numpy
    array with the stock prices, the budget and the number of shares per ETF.
    xt = [p1t-M, ..., p1t, r1t-M, ..., r1t, No. of shares in t, Budget in t]
    """
    def __init__(self, oMarkt: Market, cons_mon_budget: float, starting_budget: float, stocks: list, symbol):
        """Initialize a Task object.
        Params
        ======
        oMarkt: the market data
        cons_mon_budget: value of budget constraint
        starting_budget
        """
        # Market
        self.market = oMarkt

        dfzero = np.zeros(self.timewindow)
        state = np.concatenate([dfzero], [dfzero], [0], [self.start_budget])

        self.state_size = len(state)
        self.action_low = -1.0*starting_budget/np.mean(oMarkt.marketdata[symbol])  #maximum no of shares that can be bought
        self.action_high = -1.0*self.action_low
        self.action_size = 1

        self.stocks=stocks
        self.portfolio = {x: 0.0 for x in stocks} # dictionary with key:value pairs for the portfolio positions
        self.account = starting_budget
        self.start_budget = starting_budget
        self.cons_month_budget = cons_mon_budget
        self.rewardscale = 0.001
        self.timewindow = 10  # length of time window for the historic data
        self.symbol = symbol

    def get_reward(self):
        """
        Uses current portfolio to calculate and return total portfolio value for the current time slot.
        """
        totalvalue = 0.0

        for key,value in self.portfolio.items():
            totalvalue=totalvalue + value*self.market.get_value(key)

        totalvalue = totalvalue + self.account - self.start_budget
        reward = np.tanh(self.rewardscale*totalvalue)
        return reward

    def step(self, transactions: dict):
        """
        the transactions come out of the agent.act() function
        Uses action to obtain next state, reward, done.
        transactions are a dict with the ticker names and the shares to buy or sell
        """
        reward = 0
        done = self.market.next_timestep()  # no need to pass transactions to market as they do not impact it

        # execute the transactions and change the portfolio
        for key,value in transactions.items():
            transvalue=self.account-value*self.market.get_value(key)
            if transvalue>0:  #budget constraint
                if (value<0 and self.portfolio[key]>=np.abs(value)) or value>=0:  #I can only sell what I have
                    self.portfolio[key]=self.portfolio[key]+value
                    self.account=self.account-value*self.market.get_value(key)

        # calculate reward
        #TODO: penalize agent for trying to go over the budget constraints
        reward += self.get_reward()

        # construct next state
        next_state = np.concatenate([[self.market.get_last_values(self.symbol,self.timewindow)],\
                             [self.market.get_last_values('US_rate',self.timewindow)],\
                                [self.portfolio[self.symbol]],\
                                [self.account]])
        return next_state, reward, done

    def reset(self):
        """
        Reset the task to start a new episode.
        The state vector is initialized with zeros.
        """
        #market reset
        self.market.reset()
        #state reset
        dfzero = np.zeros(self.timewindow)
        state = np.concatenate([dfzero], [dfzero], [0], [self.start_budget])
        # portfolio reset
        self.portfolio = {x: 0.0 for x in self.stocks}
        # bank account reset
        self.account = self.start_budget
        return state

    def get_monthstart(self):
        return self.market.get_value('monthstart')
