import numpy as np
import keras
from task import Task

class BAH_Agent():
    """
    buy-and-hold agent without learning capabilities
    Financial Modeling: ./capstone_project/resources/optimal_trading_strategy.ods"
    """
    def __init__(self, task: Task):
        # the constructor does not return any value
        # Task (environment) information
        self.task = task
        self.state_size = task.state_size
        self.action_size = task.action_size
        self.action_low = task.action_low
        self.action_high = task.action_high
        self.action_range = self.action_high - self.action_low

        # internal agent state not needed

        # Episode variables
        self.last_state = self.task.reset()

    def reset_episode(self):
        state = self.task.reset()
        self.last_state = state
        return state

    def step(self, action, reward, next_state, done):
        """ the agent follows up on action that it has taken"""
        # Save experience / reward
        self.total_reward += reward
        self.count += 1

        # Learn, if at end of episode
        self.learn()

        # Roll over last state and action
        self.last_state = next_state

    def act(self, state):
        """
        Choose action based on given state and policy
        Returns actions for given state(s) as per current policy.
        Policy of this agent:
        1. Check if it is the first of the month
        2. If yes, buy a fixed amount of shares
        """
        action = {}
        if self.task.get_monthstart():
            action = None
            #TODO finish act() function
        return action


    def learn(self, experiences):
        """Agent does not learn, so nothing is happening here"""
        pass
