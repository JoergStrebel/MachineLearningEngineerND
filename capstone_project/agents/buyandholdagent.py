import numpy as np
import keras
from task import Task

class BAH_Agent():
    """
    buy-and-hold agent without learning capabilities
    Financial Modeling: ./capstone_project/resources/optimal_trading_strategy.ods"
    The approach to validation is as follows: there are two tasks, one for training and one for validation. Both tasks
    are handed over to the agent and parameter switches control which task environment is used by the agent

    """
    def __init__(self, task_train: Task, task_test: Task,  monthly_allocation: dict):
        """
        :param task_train: task environment with training data
        :param task_validate: task environment with test data
        :param monthly_allocation: dictionary with monthly budget per ETF

        the constructor does not return any value
        Task (environment) information
        """
        self.task = task_train
        self.state_size = self.task.state_size
        self.action_size = self.task.action_size
        self.action_low = self.task.action_low
        self.action_high = self.task.action_high
        self.action_range = self.action_high - self.action_low
        self.symbol = self.task.symbol
        self.monthly_allocation = monthly_allocation

        self.task_test = task_test
        self.testflag=False

        # internal agent state not needed

        # Episode variables
        self.last_state = self.task.reset()

    def reset_episode(self, testflag = False):
        self.testflag=testflag
        if testflag:
            self.task = self.task_test
            state = self.task.reset()
            self.last_state = state
            self.state_size = self.task.state_size
            self.action_size = self.task.action_size
            self.action_low = self.task.action_low
            self.action_high = self.task.action_high
            self.action_range = self.action_high - self.action_low
            self.symbol = self.task.symbol
        else:
            state = self.task.reset()
            self.last_state = state
        return state

    def step(self, action, reward, next_state, done):
        """ the agent follows up on action that it has taken"""
        # Save experience / reward
        pass

        # Learn, if at end of episode
        self.learn(None)

        # Roll over last state and action
        self.last_state = next_state

    def act(self, state):
        """
        Choose action based on given state and policy
        Returns actions for given state(s) as per current policy.
        :param state: the state of the task
        :param testflag: If true, the mode is test, then the test task is used.

        Policy of this agent:
        1. Check if it is the first of the month
        2. If yes, buy a fixed amount of shares
        """
        taskenv = self.task
        action = {}
        if taskenv.get_monthstart():
            # get current prices
            for key,value in self.monthly_allocation.items():
                current_price = taskenv.market.get_value(key+'_price')
                action[key] = value/current_price
        else:
            for key,value in self.monthly_allocation.items():
                action[key] = 0.0
        return action

    def learn(self, experiences):
        """Agent does not learn, so nothing is happening here"""
        pass
