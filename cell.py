#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Cell:
    """Class for an individual grid cell. A list of individual cells each
    containing their legitimate moves to their neighbouring cells defines 
    a grid."""
    
    def __init__(self, x, y, legit_moves):
        """Initializes with coordinates and legitimate moves to neighbours."""
        self.x = x
        self.y = y
        self.moves = legit_moves
        self.name = str(x)+str(y)
        
    def get_x(self):
        """Returns the x-coordinate of the cell."""
        return self.x
        
    def name_x(self):
        return str(self.x)
        
    def get_y(self):
        """Returns the y-coordinate of the cell."""
        return self.y
        
    def name_y(self):
        return str(self.y)
        
    def get_moves(self):
        """Returns the legitimate moves from the cell."""
        return self.moves
        
    def get_name(self):
        """Returns the name of the cell."""
        return self.name

