#!/usr/bin/env python
# -*- coding: utf-8 -*-

from solver import Solver
import numpy as np

class QLearning(Solver):
    """A solver class for the q-learning algorithm."""
    
    def __init__(self, cells, gamma = 0.95, l = 0.01,
                 epsilon = 0.1, N_iter = 100000):
        """Initializes a solver with additional q-learning parameters:
                gamma: discount factor (0 < gamma < 1)
                l: learning rate (0<l<=1, higher is faster)
                epsilon: convergence threshold (epsilon > 0)
                N_iter: number of iterations
        """
        
        Solver.__init__(self, cells)
        self.gamma = gamma
        self.l = l
        self.epsilon = epsilon
        self.N_iter = N_iter
        
    def solve(self):
        """Performs the q-learning algorithm to find the optimal grid 
        navigation policy. In q-learning an action is taken based on the 
        Q-value of each state-action pair. The Q-value is updated after taking 
        action and obtaining a new state. When deciding which action to take, 
        we try to balance between improving the accuracy of Q(s,a) and taking 
        the action with the highest Q-value. Here the Multi-Armed Bandit rule 
        is used for the decision.
        Returns:
            - Names of states (cells)
            - Q-values for state-action pairs
            - Highest Q-value for START (1,1) state
            - Number of completed iterations
        """
        
        # List of actions to take
        actions = ["north","east","south","west"]
        
        # States
        states = self.cells
        state_container = {cell.get_name():cell for cell in states}
        state_names = [cell.get_name() for cell in states]
        
        # Cumulative reward matrix
        c_rew = np.zeros([len(states),len(actions)])
        
        # Q matrix
        Q = np.zeros([len(states),len(actions)])
        
        # T-values for actions
        T = np.zeros([len(states),len(actions)])
        
        # Choose every action once for each state
        for state_name in state_names:
            state_ind = state_names.index(state_name)
            for action in range(0,4):
                state = state_container[state_name]
                next_state = self.move(state, actions[action])
                c_rew[state_ind,action] += \
                        self.get_immediate_reward(state_container[next_state])
                Q[state_ind,action] += self.l*c_rew[state_ind,action]
                T[state_ind,action] += 1
                
        # Initial state
        state = state_container["11"]
        state_ind = state_names.index("11")
        
        # Q-Learning
        q11 = [0]*self.N_iter
        for i in range(self.N_iter):
        
            # Choose action based on MAB rule
            max_action = 0
            max_mab = -10000
            for action in range(4):
                mab = c_rew[state_ind,action]/T[state_ind,action] + \
                    np.sqrt(2*np.log(np.sum(T[state_ind,]))/T[state_ind,action])
                if mab > max_mab:
                    max_action = action
                    max_mab = mab
            chosen_action = max_action
            
            # Update T
            T[state_ind,chosen_action] += 1
            
            # Execute chosen action
            next_state_name = self.move(state, actions[chosen_action])
            next_state = state_container[next_state_name]
            next_state_ind = state_names.index(next_state_name)
            reward = self.get_immediate_reward(next_state)
            
            # Find action that maximizes Q-value for next state
            max_action = 0
            max_q = -10000
            for action in range(4):
                q = Q[next_state_ind,action]
                if q > max_q:
                    max_action = action
                    max_q = q
                    
            c_rew[state_ind,chosen_action] += reward + self.gamma*max_q
            
            # Update Q-value
            Q[state_ind,chosen_action] = (1-self.l)*Q[state_ind,chosen_action] \
                                            + self.l*(reward + self.gamma*max_q)
                                            
            q11[i] = np.amax(Q[state_names.index("11"),])
            
            state = next_state
            state_ind = state_names.index(state.get_name())
            
        return [state_names, Q, q11, i]

