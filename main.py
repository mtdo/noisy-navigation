#!/usr/bin/env python
# -*- coding: utf-8 -*-

from value_iteration import ValueIteration
from q_learning import QLearning
from cell import Cell
import matplotlib.pyplot as plt
import numpy as np
import sys, getopt

def construct_grid():
    # Define grid (coordinates and their possible moves)
    pmoves = {"11":["north","east"],
              "21":["east","west"],
              "31":["north","east","west"],
              "41":["north","west"],
              "12":["north","south"],
              "32":["north","east","south"],
              "42":["north","south","west"],
              "13":["east","south"],
              "23":["east","west"],
              "33":["east","south","west"],
              "43":["south","west"]}
              
    # Construct cell objects for the grid
    xs = [1,2,3,4]
    ys = [1,2,3]
    grid = []
    for x in xs:
        for y in ys:
            if (x != 2 or y != 2):
                name = str(x)+str(y)
                moves = pmoves[name]
                grid.append(Cell(x,y,moves))
                
    return grid
    
def main(argv):
    # Get command line arguments
    try:
        opts, args = getopt.getopt(argv, "pi:")
    except getopt.GetoptError:
        print("main.py [-p] [-i=n_iter]")
        sys.exit(1)
        
    # Plot switch
    plot = False
    
    # Default iterations
    n_iter = 100000
    
    # Parse command line arguments
    for opt, arg in opts:
        # Help
        if opt == "-h":
            print("main.py [-p] [-i=n_iter]")
            sys.exit()
        
        # Plot
        elif opt == "-p":
            plot = True
        
        # Number of iterations
        elif opt == "-i":
            n_iter = arg
            
    # Construct grid
    grid = construct_grid()
    
    # Find solution with value iteration
    print("Performing value iteration...")
    vi = ValueIteration(grid)
    vi = vi.solve()
    print("----------")
    print("The value for each cell is:")
    print("(x,y): value")
    for cell in grid:
        print(cell.name_x()+","+cell.name_y()+":     "+\
              str(vi[0][cell.get_name()]))
    print("----------")
    print("The policy found by value iteration is:")
    print("(x,y): action")
    for cell in grid:
        print(cell.name_x()+","+cell.name_y()+":     "+\
              str(vi[1][cell.get_name()]))
              
    # Find solution with Q-learning
    print("\n")
    print("Performing Q-learning...")
    ql = QLearning(grid, N_iter = int(n_iter))
    ql = ql.solve()
    ql_states = ql[0]
    ql_Q = ql[1]
    print("----------")
    
    print("The policy found by Q-learning is.")
    print("(x,y): action")
    
    actions = ["north","east","south","west"]
    for cell in grid:
        ind = ql_states.index(cell.get_name())
        action = actions[np.argmax(ql_Q[ind,])]
        print(cell.name_x()+","+cell.name_y()+":     "+str(action))
        
    if plot:
        # Convergence graph for q-learning: 
        # best Q-value of the best action for the START state 
        fig, ax = plt.subplots()
        ax.plot(ql[2][0:ql[3]], label = "Q-values for best action in START")
        ax.plot((0,ql[3]),(vi[0]["11"],vi[0]["11"]), label = "Values of START")
        plt.xlabel("Iterations")
        
    plt.show()
    
if __name__ == "__main__":
    main(sys.argv[1:])

