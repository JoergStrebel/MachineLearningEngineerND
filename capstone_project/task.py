import numpy as np
from  market import Market
import pandas as pd

class Task():
    """Task (environment) that defines the goal and provides feedback to the agent."""
    def __init__(self, oMarkt: Market):
        """Initialize a Task object.
        Params
        ======

        """
        # Market
        self.sim = oMarkt
        self.action_repeat = 1

        self.state_size = self.action_repeat * 6
        self.action_low = 0
        self.action_high = 900
        self.action_size = 4

        # Goal
        self.target_pos = None

    def get_reward(self):
        """
        Uses current pose of sim to return reward.
        """
        # This part of the reward function is based on the Euclidean distance (L2 norm)
        #l2norm = np.sqrt(np.sum(np.square(self.sim.pose[:3] - self.target_pos)))
        #reward_distance = -2.0 * np.tanh(0.1 * l2norm)
        # reward_distance = -l2norm/5

        # This part of the reward function is based on the L1 norm
        distance=np.sum(abs(self.sim.pose[:3] - self.target_pos))

        if distance<3:
            reward=10
        else:            
            reward = np.tanh(2 - 0.005*(distance))
            
        return reward

    def step(self, rotor_speeds):
        """Uses action to obtain next state, reward, done."""
        reward = 0
        pose_all = []
        for _ in range(self.action_repeat):
            done = self.sim.next_timestep(rotor_speeds)  # update the sim pose and velocities
            reward += self.get_reward()
            pose_all.append(self.sim.pose)
        next_state = np.concatenate(pose_all)
        return next_state, reward, done

    def reset(self):
        """Reset the sim to start a new episode."""
        self.sim.reset()
        state = np.concatenate([self.sim.pose] * self.action_repeat)
        return state
