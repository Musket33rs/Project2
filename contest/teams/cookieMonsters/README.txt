Tou LEE         656128 toul@student.unimelb.edu.au
Jaime MARTINEZ  642231 jmartinez1@student.unimelb.edu.au

Team name - cookieMonsters

% Planning strategy used.

At first we wanted to run FF to compute a plan for our PDDL domains for ghosts
and Pacman. However, we had a lot of issues trying to make FF run on Ubuntu
so we decided to use a Search Agent using A* and Manhattan distance as the
heuristic.

Our strategy is simple enough. We have one offensive and one defensive agent. On
each iteration, the offensive agent calculates the best path to reach the closest
food. The agent keeps recalculating the goal until a certain number of foods are
eaten. When this threshold is passed, then we simply find the closest point to
our side of the map to try to return the food. We used a modified version of the
AnyFoodSearchProblem used in project 1 to generate a plan using the mentioned
heuristic. We modified the function that calculates the costs of all actions,
trying to check for ghosts in the expanded nodes so that a higher cost could be
given to those positions.

The overall performance of the planner is not too bad as the calculation of the
plan is pretty fast. One improvement would be to modify the implementation
of A* to modify the heuristic when a ghost, or some other condition, applies at
a certain position on the grid.
