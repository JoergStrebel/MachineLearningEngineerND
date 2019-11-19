import numpy as np
import keras

class BAH_Agent():
    """Reinforcement Learning agent that learns using DDPG."""
    def __init__(self, task):
        # the constructor does not return any value
        # Task (environment) information
        self.task = task
        self.state_size = task.state_size
        self.action_size = task.action_size
        self.action_low = task.action_low
        self.action_high = task.action_high
        self.action_range = self.action_high - self.action_low

        # internal agent state

        # Episode variables
        self.last_state = None
        self.reset_episode()

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
        """
        state = None
        action = None
        return action


    def learn(self, experiences):
        """Agent does not learn, so nothing is happening here"""
        pass
