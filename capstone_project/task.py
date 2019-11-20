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
    """
    def __init__(self, oMarkt: Market, cons_mon_budget: float, starting_budget: float, stocks: list):
        """Initialize a Task object.
        Params
        ======
        oMarkt: the market data
        cons_mon_budget: value of budget constraint
        starting_budget
        """
        # Market
        self.market = oMarkt

        self.state_size = self.action_repeat * 1
        self.action_low = 0
        self.action_high = 900
        self.action_size = 4

        self.portfolio = {x: 0.0 for x in stocks} # dictionary with key:value pairs for the portfolio positions
        self.account = starting_budget
        self.start_budget = starting_budget
        self.cons_month_budget = cons_mon_budget
        self.rewardscale = 0.001

    def get_reward(self):
        """
        Uses current portfolio to calculate and return total portfolio value for the current time slot.
        """
        totalvalue = 0.0

        for key,value in self.portfolio.items():
            totalvalue=totalvalue + value*self.market.get_price(key)

        totalvalue = totalvalue + self.account - self.start_budget
        reward = np.tanh(self.rewardscale*totalvalue)
        return reward

    def step(self, portfolio: dict, transactions: dict):
        """
        the transactions come out of the agent.act() function
        Uses action to obtain next state, reward, done.
        transactions are a dict with the ticker names and the shares to buy or sell
        """
        reward = 0
        done = self.oMarket.next_timestep()  # no need to pass transactions to market as they do not impact it

        # execute the transactions and change the portfolio
        for key,value in transactions.items():
            self.portfolio[key]=self.portfolio[key]+value
            self.account=self.account-value*self.market.get_price(key)
        #TODO: check the budget constraints

        # calculate reward
        reward += self.get_reward()

        next_state = None #update portfolio with transactions
        return next_state, reward, done

    def reset(self):
        """Reset the task to start a new episode."""
        self.market.reset()

        state = None
        return state
