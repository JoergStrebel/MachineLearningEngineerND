import numpy as np
from task import Task


class Pilot_Agent():
    def __init__(self, task):
        #the constructor does not return any value
        # Task (environment) information
        self.task = task
        self.state_size = task.state_size
        self.action_size = task.action_size
        self.action_low = task.action_low
        self.action_high = task.action_high
        self.action_range = self.action_high - self.action_low

        # Score tracker and learning parameters
        self.best_w = None
        self.best_score = -np.inf

        # Episode variables
        self.reset_episode()

    def reset_episode(self):
        self.total_reward = 0.0
        self.count = 0
        state = self.task.reset()
        return state

    def step(self, reward, done):
        # Save experience / reward
        self.total_reward += reward
        self.count += 1

        # Learn, if at end of episode
        if done:
            self.learn()

    def act(self, state):
        # Choose action based on given state and policy

        return None

    def learn(self):
        # Learn by random policy search, using a reward-based score
        pass
