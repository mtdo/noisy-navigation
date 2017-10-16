# noisy-navigation #
A navigation task with noisy movements is a type of decision-theoretic planning
problem where the aim is to find the best action in each system state.
Such problems can be modeled as Markov decision processes and solved with
dynamic programming algorithms and reinforcement learning.  
Here a grid navigation task is solved with value iteration and q-learning to
compare both the accuracy and the convergence speed of the solutions given by the two
approaches.

## Grid ##
The navigation grid used in this project is shown below:  

![alttext](img/grid.svg)

Reaching the grid cells marked with +1 and -1 have the respective rewards,
while the rest cells have reward 0. The gray cell is inaccessible and all
move actions in the top right cell cause the agent to be teleported to the
cell marked as 'start'.

The noise in the movement actions is shown below:  

![alttext](img/movement.svg)

There are four possible moves: North, West, South and East.
When attempting a movement action, there is a 10% chance that the agent
ends up in either one of the directions that are perpendicular to the intended
one.

## Value iteration ##

In the value iteration algorithm all actions are iterated for each state to
find the best action and update the state values. The state value is a
combination of the immediate reward as well as the discounted long-term reward
associated with the state. The algorithm returns the best navigation policy, given by the actions yielding the maximum value.

## Q-learning ##

In contrast to value iteration, the state transition probabilities and the
state rewards are not known a priori in Q-learning. The algorithm begins from
the 'start' state, chooses an action to take and then updates the state-action
Q-value. The chosen action is decided with the so called Multi-Armed Bandit rule which optimally balances between improving the accuracy of the Q-values and taking the action with the highest Q-value. The algorithm returns the state-action Q-values and the navigation policy can be
extracted by choosing the action with the highest Q-value in each state.

## Requirements

The following python packages are required to run the solver:  
* `numpy 1.13.3`
* `matplotlib 2.1.0`

## Running the solver

The grid navigation task can be solved with the two algorithms by:

```sh
$ python3 main.py
```

Q-learning is run for 100000 iterations by default. The number of iterations
can be changed with the `-i` argument:

```sh
$ python3 main.py -i 150000
```


The accuracy and convergence rate of the algorithms can be plotted with the
`-p` argument:

```sh
$ python3 main.py -p
```
## Todos

* Convergence criterion for Q-learning

## References

* [Decision-Theoretic Planning: Structural Assumptions and Computational Leverage][decision-theoretic-planning],  
Boutilier C., Dean T. and Hanks S., Journal of Artificial Intelligence Research, 1999, vol. 11

* [Learning from Delayed Rewards][q-learning],  
Watkins, C. J. C. H., Ph.D. Thesis, Cambridge University, 1989


* [Algorithms for the Multi-Armed Bandit Problem][multi-armed-bandit],  
Kuleshov, V. and Precup, D.,
Journal of Machine Learning Research, 2000, vol. 1

* [CE-E4800 Artificial Intelligence][aalto-course],  
Aalto University






[decision-theoretic-planning]: https://arxiv.org/pdf/1105.5460.pdf

[multi-armed-bandit]: https://arxiv.org/pdf/1402.6028.pdf

[q-learning]: http://www.cs.rhul.ac.uk/~chrisw/thesis.html

[aalto-course]: https://mycourses.aalto.fi/course/search.php?search=CS-E4800+Artificial+Intelligence
