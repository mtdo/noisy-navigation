#!/usr/bin/env python
# -*- coding: utf-8 -*-

from solver import Solver

class ValueIteration(Solver):
    """A solver class for the value iteration algorithm."""
    
    def __init__(self, cells, gamma = 0.95, epsilon = 0.032, conv = True):
        """Initializes a solver with additional value iteration parameters:
                gamma: discount factor (0 < gamma < 1)
                epsilon: convergence threshold (epsilon > 0).
        """
        
        Solver.__init__(self, cells)
        self.gamma = gamma
        self.epsilon = epsilon
        self.conv = True
        
    def solve(self):
        """Performs the value iteration algorithm to find the optimal 
        grid navigation policy. In value iteration each action is iterated to
        find the current best action for each state (cell) and update the value 
        of each state. Both the immediate reward and long-term reward are 
        accounted for as defined by the discount factor gamma. The best policy 
        is given by the actions yielding the maximum value.
        Returns:
            - Value of each state
            - Policy
        """
        
        # States used in value iteration
        states = self.cells
        state_container = {cell.get_name():cell for cell in states}
        
        # Values for the states
        value = {cell.get_name():0 for cell in states}
        value_new = {cell.get_name():value[cell.get_name()] for cell in states}
        
        # Current policy
        policy = {cell.get_name():"" for cell in states}
        
        # Maximum number of iterations
        N_max = 10000 # Should be sufficient for pretty much all scenarios
        
        # Value iteration
        for i in range(N_max):
        
            # Iterate each state
            for state in states:
            
                # Possible actions from current state
                actions = ["north","east","south","west"]
                
                # Find best action for current state
                max_action = actions[0]
                max_value = -10000
                for action in actions:
                
                    # The possible actual outcomes from current action
                    # First one is always the correct outcome
                    possible_outcomes = self.get_possible_outcomes(action)
                    probs = [0.8, 0.1, 0.1]
                    
                    # Calculate the value of current action in current state
                    current_value = 0
                    
                    # Three possible outcomes from current action
                    for j in range(3):
                        outcome = possible_outcomes[j]
                        
                        # Teleportation
                        if state.get_name() == "43":
                            next_cell = state_container["11"]
                            
                        # Get next state if outcome is legit move
                        elif outcome in state.get_moves():
                            x_new = state.get_x() + self.MOVES[outcome][0]
                            y_new = state.get_y() + self.MOVES[outcome][1]
                            next_cell = state_container[str(x_new)+str(y_new)]
                            
                        # Remain in the current state if outcome is not legit
                        else:
                            next_cell = state
                            
                        # Update value of current action
                        current_value += probs[j]* \
                            (self.get_immediate_reward(next_cell) + \
                            self.gamma*value[next_cell.get_name()])
                            
                    # If the value of current action is best so far,
                    # update value function and policy
                    if (current_value > max_value):
                        max_action = action
                        max_value = current_value
                        
                # Store value and policy for this iteration in their dicts
                value_new[state.get_name()] = max_value
                policy[state.get_name()] = max_action
                
            # Check for convergence using the given threshold
            terminate = True
            for state in states:
                state_name = state.get_name()
                diff = value_new[state_name] - value[state_name]
                if diff > self.epsilon*(1-self.gamma)/(2*self.gamma) or \
                diff < -self.epsilon*(1-self.gamma)/(2*self.gamma):
                        terminate = False
                        
            if terminate:
                if self.conv:
                    print("Value iteration converged after "+str(i), \
                          " iterations.")
                return [value_new, policy]
            else:
                value = {cell.get_name():value_new[cell.get_name()] \
                         for cell in states}

