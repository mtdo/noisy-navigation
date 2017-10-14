#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

class Solver:
    """A generic class for a grid navigation solver."""
    
    # Moves and their respective coordinate deltas
    MOVES = {"north":[0,1],
             "east":[1,0],
             "south":[0,-1],
                  "west":[-1,0]}
                  
    # Possible outcomes for each move
    POSOUT = {"north":["north","east","west"],
              "east":["east","south","north"],
              "south":["south","west","east"],
              "west":["west","north","south"]}
              
    def __init__(self, cells):
        """The solver is initialized by a list of cells (a grid)."""
        
        self.cells = cells
        
    def get_possible_outcomes(self, direction):
        """Returns the possible outcomes when attempting move in 
        given direction.
        """
        
        return self.POSOUT[direction]
        
    def get_immediate_reward(self, cell):
        """Returns the immediate reward when moving to given cell."""
        
        if (cell.get_name() == "43"):
            return 1
        elif (cell.get_name() == "42"):
            return -1
        else:
            return 0
            
    def move(self, cell, direction):
        """Attemps to move in given direction from the given cell."""
        
        # Possible outcomes
        pos_outcomes = self.get_possible_outcomes(direction)
        
        # Sample outcome
        outcome = sum(sum(np.random.multinomial(1, [0.8,0.1,0.1]).nonzero()))
        outcome = pos_outcomes[outcome]
        
        # Teleportation
        if cell.get_name() == "43":
            return "11"
        # Legit move
        elif outcome in cell.get_moves():
            x_new = cell.get_x() + self.MOVES[outcome][0]
            y_new = cell.get_y() + self.MOVES[outcome][1]
            return str(x_new)+str(y_new)
        # Not legit move -> stay put
        else:
            return cell.get_name()
            
    def solve(self):
        """A dummy method for the navigation solving algorithm."""
        raise NotImplementedError

