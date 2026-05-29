from pulp import *
from random import randint
from matplotlib import pyplot as plt
import numpy as np


# the optimal vertex cover, including integer numbers only
def compute_optimal_vertex_cover(n, edge_list):
    # Create a problem -- indicate that we will minimize the objectives
    prob = LpProblem('vert_cover', LpMinimize)
    # Add all the decision vars (we do this using comprehensions in Python but you could write a for-loop as well)
    dvars = [LpVariable(f'w_{i}', cat='Binary') for i in range(1, n+1)]
    # Note that lpSum is defined in Pulp and it simply takes the sum of all variables in a list of vars.
    prob += lpSum(dvars) # minimize the sum of the variables
    for (i, j) in edge_list: # go through each edge in the list
        assert 1 <= i <= n 
        assert 1 <= j <= n
        prob += dvars[i-1] + dvars[j-1] >= 1 # add the constraint -- wi + wj >= 1 -- indexing in python starts from 0 and thus we require the -1
    stat = prob.solve(PULP_CBC_CMD(msg=False)) # solve the problem but suppress output
    assert stat == LpStatusOptimal, 'Problem does not have optimal status -- something went wrong -- this should not happen for this problem'
    vert_cover = [i+1 for i in range(n) if dvars[i].varValue > 0 ]
    return len(vert_cover)


# the optimal vertex cover, including fractional numbers
def compute_lp_relaxation_vertex_cover(n, edge_list):
    # Create a problem -- indicate that we will minimize the objectives
    prob = LpProblem('vert_cover', LpMinimize)
    # Add all the decision vars (we do this using comprehensions in Python but you could write a for-loop as well)
    dvars = [LpVariable(f'z_{i}', lowBound=0.0, upBound=1.0, cat='Continuous') for i in range(1, n+1)]
    # Note that lpSum is defined in Pulp and it simply takes the sum of all variables in a list of vars.
    prob += lpSum(dvars) # minimize the sum of the variables
    for (i, j) in edge_list: # go through each edge in the list
        assert 1 <= i <= n 
        assert 1 <= j <= n
        prob += dvars[i-1] + dvars[j-1] >= 1 # add the constraint -- wi + wj >= 1 -- indexing in python starts from 0 and thus we require the -1
    stat = prob.solve(PULP_CBC_CMD(msg=False)) # solve the problem but suppress the output
    assert stat == LpStatusOptimal, 'Problem does not have optimal status -- something went wrong -- this should not happen for this problem'
    vert_cover = [x.varValue for x in dvars]
    return sum(vert_cover)

## generate a random graph with n nodes and m edges + compute both optimal cover using ILP and LP relaxations
from random import randint
def formulate_random_problem(n, m):
    # n vertices and m edges
    edge_list = []
    for i in range(m):
        done = False
        vi= 1
        vj = n
        while not done: # get two random vertices
            vi, vj = randint(1, n), randint(1, n)
            vi, vj = min(vi, vj), max(vi, vj)
            if vi != vj and (vi, vj) not in edge_list: # if they are not the same vertex or we have not seen the edge previously
                done = True
        edge_list.append((vi, vj))
    assert len(edge_list) == m
    n1 = compute_optimal_vertex_cover(n, edge_list)
    n2 = compute_lp_relaxation_vertex_cover(n, edge_list)
    return (n1, n2)

# run 50 different random problems
# Each problem generates a random graph with 50 vertices and 240 edges
# This is going to take quite some time
opt_vertex_cover = []
lp_relax_obj = []
print('Opt Cover, Lp Relaxation')
print('------------------------')
for i in range(250):
    n = randint(15, 60)
    m = randint(n*2, n*5)
    print(f'n = {n}, m={m}')
    (n1, n2) = formulate_random_problem(n, m) 
    opt_vertex_cover.append(n1)
    lp_relax_obj.append(n2)
    print(f'opt-cover={n1}, lp-relax={n2}')

# generate the cool visuals to illustrate how the opt-cover (rounded to 1) is no more than 2x the lp-relax value
plt.scatter(opt_vertex_cover, lp_relax_obj,marker='*')
x = np.linspace(min(opt_vertex_cover), max(opt_vertex_cover), 50)
y = x/2
plt.plot(x,y, '--', label='y=x/2')
plt.plot(x,x, '--', label='y=x')
plt.legend()
plt.xlabel('LP Relaxation')
plt.ylabel('Optimal Cover')