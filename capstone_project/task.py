import numpy as np
from market import Market
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
    xt = [p1t-M, ..., p1t, r1t-M, ..., r1t, No. of shares in t, Budget available in t, Monthly Budget available in t]
    """
    def __init__(self, oMarkt: Market, cons_mon_budget: float, starting_budget: float, stocks: list, symbol:str,
                 tcost:float, penalty:float):
        """Initialize a Task object.
        Params
        ======
        oMarkt: the market data
        cons_mon_budget: value of budget constraint
        starting_budget
        stocks: list of all ETFs
        symbol: ETF that is traded right now
        tcost: transaction cost , i.e. absolute € fee per transaction
        """
        # Market
        self.market = oMarkt
        self.account = starting_budget  # the bank account
        self.start_budget = starting_budget
        self.cons_month_budget = cons_mon_budget
        self.month_account = cons_mon_budget

        self.rewardscale = 0.00005
        self.symbol = symbol
        self.timewindow = 10  # length of time window for the historic data
        self.symbol2column = {'SP500':'SP500_price'}
        self.index2symbol = ['SP500']  # list of ETFs traded by the agents

        self.dfzero = np.zeros(self.timewindow)
        self.action_zero = np.zeros(len(self.index2symbol))
        state = np.concatenate([self.dfzero, self.dfzero, self.action_zero, [self.start_budget], [self.cons_month_budget]])

        self.state_size = len(state)

        # maximum no of shares that can be bought per month per ETF
        # SP500 as it is the only traded ETF
        # the low/high action is a bit reduced by 0.98 to avoid hitting the budget limits due to floating point
        # inaccuracies
        self.action_low = -0.98*cons_mon_budget/np.max(oMarkt.marketdata[self.symbol2column['SP500']])
        self.action_high = -0.98*self.action_low
        self.action_size = len(self.index2symbol)

        self.stocks=stocks
        self.portfolio = {x: 0.0 for x in stocks} # dictionary with key:value pairs for the portfolio positions
        self.transaction_cost=tcost
        self.penalty=penalty

    def get_reward(self, penalties = 0.0, tcosts = 0.0):
        """
        Uses current portfolio to calculate and return total portfolio value for the current time slot.
        """
        totalvalue = self.get_total_value()
        totalvalue = totalvalue - self.start_budget + penalties + tcosts
        reward = np.tanh(self.rewardscale*totalvalue)
        return reward

    def step(self, transactions: list):
        """
        the transactions come out of the agent.act() function
        Uses action to obtain next state, reward, done.
        transactions are a list with the the shares to buy or sell
        order: ['SP500', 'ESTOXX', 'MSCI']
        """
        reward = 0
        penalties = 0.0

        if self.get_monthstart():
            self.month_account = self.cons_month_budget

        # transaction costs are incurred if the transaction is submitted to the task environment
        tcosts=len([x for x in transactions if x>0.0])*self.transaction_cost

        # verify transactions
        # you can only sell what I have
        for i in range(len(transactions)):
            volume=float(transactions[i])
            if volume<0.0:  #sell
                if abs(volume)>self.portfolio[self.index2symbol[i]]:
                    transactions[i] = -self.portfolio[self.index2symbol[i]]
                    penalties = penalties + self.penalty

        # you can only do what fits in the overall budget
        transvalue = 0.0
        for i in range(len(transactions)):
            volume=float(transactions[i])
            price=float(self.market.get_value(self.symbol2column[self.index2symbol[i]]))
            transvalue = transvalue + float(volume*price)

        # check for overall account
        if self.account<transvalue:
            transactions = self.action_zero  #if the budget constraint is not fulfilled, then nothing happens
            penalties = penalties + self.penalty

        # check for monthly budget constraint
        if  self.month_account<transvalue:
            transactions = self.action_zero  #if the budget constraint is not fulfilled, then nothing happens
            penalties = penalties + self.penalty

        # execute the transactions and change the portfolio
        for i in range(len(transactions)):
            volume=float(transactions[i])
            price=float(self.market.get_value(self.symbol2column[self.index2symbol[i]]))
            tvalue = float(volume*price)
            self.portfolio[self.index2symbol[i]]=self.portfolio[self.index2symbol[i]]+transactions[i]
            self.account=self.account-tvalue
            self.month_account=self.month_account-tvalue

        reward = self.get_reward(penalties, tcosts)
        done = self.market.next_timestep()  # no need to pass transactions to market as they do not impact it

        # construct next state
        prices = self.market.get_last_values(self.symbol2column[self.symbol],self.timewindow)
        rates = self.market.get_last_values('US_rate',self.timewindow)
        next_state = np.concatenate([prices, rates, [self.portfolio[x] for x in self.index2symbol],[self.account],
                                     [self.month_account]])
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
        state = np.concatenate([dfzero, dfzero, self.action_zero, [self.start_budget], [self.cons_month_budget]])
        # portfolio reset
        self.portfolio = {x: 0.0 for x in self.stocks}
        # bank account reset
        self.account = self.start_budget
        self.month_account = self.cons_month_budget
        return state

    def get_monthstart(self):
        return self.market.get_value('monthstart')

    def get_total_value(self):
        """
        Returns the total value of the customer, i.e. portfolio value and account value
        :return: value of portfolio in Euro
        """
        totalvalue = 0.0
        for key,value in self.portfolio.items():
            totalvalue = totalvalue + float(value)*float(self.market.get_value(self.symbol2column[key]))
        return totalvalue + self.account
