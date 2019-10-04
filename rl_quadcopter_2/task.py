import numpy as np
from physics_sim import PhysicsSim

class Task():
    """Task (environment) that defines the goal and provides feedback to the agent."""
    def __init__(self, init_pose=None, init_velocities=None, 
        init_angle_velocities=None, runtime=5., target_pos=None):
        """Initialize a Task object.
        Params
        ======
            init_pose: initial position of the quadcopter in (x,y,z) dimensions and the Euler angles
            init_velocities: initial velocity of the quadcopter in (x,y,z) dimensions
            init_angle_velocities: initial radians/second for each of the three Euler angles
            runtime: time limit for each episode
            target_pos: target/goal (x,y,z) position for the agent
        """
        # Simulation
        self.sim = PhysicsSim(init_pose, init_velocities, init_angle_velocities, runtime) 
        self.action_repeat = 3

        self.state_size = self.action_repeat * 6
        self.action_low = 0
        self.action_high = 900
        self.action_size = 4

        # Goal
        self.target_pos = target_pos if target_pos is not None else np.array([0., 0., 10.]) 

    def get_reward(self):
        """
        Uses current pose of sim to return reward.
        The function implements a reward function based on the Euclidean distance (L2 norm),
        however it is mapped to the interval [-1.0 ... 1.0] using tanh() to make it easier to learn.
        """
        l2norm = np.sqrt(np.sum(np.square(self.sim.pose[:3] - self.target_pos)))
        #reward_distance = -2.0 * np.tanh(0.1 * l2norm) + 1.0
        reward_distance = -l2norm/10
        angles=[]
        for index in range(len(self.sim.pose[3:])):
            x=self.sim.pose[index]
            if x>np.pi:
                angles.append(x-2*np.pi)
            else:
                 angles.append(x)
        npangles = np.array(angles)
        #reward_tilt=np.amin(-2.0*np.tanh(np.abs(4.0*npangles))+1) #penalizes poses that are too tilted
        reward_tilt=-np.sum(np.abs(npangles))

        basic_reward=1.0 #you get at least 1 if the quadcopter manages to stay in the air

        return basic_reward+(reward_tilt+reward_distance)/2

    def step(self, rotor_speeds):
        """Uses action to obtain next state, reward, done."""
        reward = 0
        pose_all = []
        for _ in range(self.action_repeat):
            done = self.sim.next_timestep(rotor_speeds) # update the sim pose and velocities
            reward += self.get_reward() 
            pose_all.append(self.sim.pose)
        next_state = np.concatenate(pose_all)
        return next_state, reward, done

    def reset(self):
        """Reset the sim to start a new episode."""
        self.sim.reset()
        state = np.concatenate([self.sim.pose] * self.action_repeat) 
        return state
