from pulp import *
from math import floor, ceil
from stats_b_n_b import *
from random import uniform, randint
from notebook_branch_and_bound import branch_and_bound_solve


# Given a list of numbers, find all indices in the list that correspond to fractional numbers.
# we use the function is_fractional to define what it means to be "fractional" -- we have to 
# account for floating point errors in this criterion
def find_all_fractional_indices(sols):
    n = len(sols)
    def is_fractional(f):
        epsilon = 0.001 # this is the precision to which we check whether something is an integer
        return  epsilon <= (f - floor(f)) <= 1-epsilon
    return [j for j in range(n) if is_fractional(sols[j]) ]


class Solution:
    # a class that will hold the best solution so far
    def __init__(self):
        self.obj_val = -float('inf') # initialize it to -infinity
        self.sol = None
    
    # replace current solution with a new one if it is better
    def replace(self, obj_val, new_sol):
        if obj_val > self.obj_val:
            self.obj_val = obj_val
            self.sol = new_sol
        return
    
# Branch and Bound with Pruning.
# The logic is almost identical to Branch and Bound but we pass around an extra argument
# that tracks the best solution so far
# We pass this argument as a class so that the reference to the class is passed. This allows
# changes made to the best solution so far in one branch to reflect elsewhere in the code.
# If you are unaware of this aspect of python, read about it here: https://www.geeksforgeeks.org/pass-by-reference-vs-value-in-python/#

def branch_and_bound_pruning_solve(c, A, b, lb, ub, best_sol_so_far, stats, depth=1, debug=True):
    n = len(c)
    m = len(A)
    assert all( len(ai) == n for ai in A), 'All rows in A must have same length'
    assert len(b) == m
    assert len(lb) == n
    assert len(ub) == n
    ## This function is just for pretty printing the tabs
    def indent():
        for _ in range(depth-1):
            print('|  ', end='')
        print(u'\u21B3', end='')
    # Check if all lower bounds are <= upper bounds, if not exit
    if any(lb[i] > ub[i] for i in range(n)): # if any lower bound is greater than upper bound, problem is infeasible, BAIL
        if debug:
            indent()
            print('Infeasibility detected due to lb[i]> ub[i].')
        return (-float('inf'), None)
    # record statistics
    if depth > stats.max_depth:
        stats.max_depth = depth
    stats.num_lps = stats.num_lps + 1
    # setup and solve the LP
    prob = LpProblem('b_and_b', LpMaximize) # create the problem
    # declare all the variables, set the upper and lower bound here
    # Note: variables are set to "Continuous" since we are solving the LP relaxation
    dvars = [LpVariable(f'x{i}', lowBound=lb[i], upBound=ub[i],cat='Continuous') for i in range(n)]
    # add the objective function -- we already set it to maximize
    prob += lpSum([ci*xi for (ci,xi) in zip(c, dvars)])
    # add the constraints for each row
    for (ai, bi) in zip(A,b):
        prob += lpSum([ aij*xj for (aij,xj) in zip(ai, dvars)]) <= bi
    #Let's solve the problem but supress the output
    status = prob.solve(apis.PULP_CBC_CMD(mip=False, msg=False))
    # Check the problem status
    if status == constants.LpStatusInfeasible: # infeasible?
        if debug:
            indent()
            print('Infeasible Problem: returning -\infty')
        stats.num_infeas = stats.num_infeas + 1
        return (-float('inf'), None) # return objective value of -infinity
    elif status == constants.LpStatusUnbounded: # unbounded
        if debug: 
            indent()
            print('Unbounded Problem: returning + \infty')
        return (float('inf'), None) # return objective value of +infinity
    else: # optimal?
        assert status == LpStatusOptimal, 'Problem results in undefined status -- cannot continue'
        sols = [x.varValue for x in dvars] # extract the solutions for each decision variable
        obj_value = sum([ci*xi for (ci, xi) in zip(c, sols)]) # compute objective value
        if debug:
            indent()
            print(f'Obtained solution: {sols} with objective {obj_value}')
        # is this objective less than the best so far?
        if obj_value < best_sol_so_far.obj_val: # if it is , then we do not need to go any further
            if debug:
                indent()
                print(f'Pruned solution: we already have an integer solution with objective {best_sol_so_far.obj_val}')
            return (-float('inf'), None) # it does not matter that we return a fake solution here since this will never beat the best solution so far.
 
        # check if the solution is integral
        jList = find_all_fractional_indices(sols)
        if len(jList) == 0: # no fractional values 
            if obj_value > stats.best_obj:
                stats.best_obj = obj_value
                stats.best_solution = sols.copy()
            if debug:
                indent()
                print('All variables are integral in optimal solution.')
                indent()
                print(f'Returning solution: {sols} with objective {obj_value}')
            if debug and obj_value > best_sol_so_far.obj_val:
                indent()
                print(f'This solution is the BEST SO FAR!!')
            best_sol_so_far.replace(obj_value, sols) # replace the best so far if appropriate.
            return (obj_value, sols) # done
        else:
            # solution is not integral
            split_var = jList[0]
            assert 0 <= split_var < n
            if debug:
                indent()
                print(f'Splitting variable : {split_var} which has a current solution {sols[split_var]}')
            # adjust upper bound 
            tmp = ub[split_var]
            ub[split_var] = floor(sols[split_var])
            if debug: 
                indent()
                print(f'Branch #1: Adding x{split_var} <= {ub[split_var]}')
            (obj1,sols1) = branch_and_bound_pruning_solve(c, A, b, lb, ub, best_sol_so_far,stats, depth+1, debug)
            if obj1 == float('inf'):
                return (obj1, sols1)
            ub[split_var] = tmp
            # adjust the lower bound
            tmp = lb[split_var]
            lb[split_var] = ceil(sols[split_var])
            if debug: 
                indent()
                print(f'Branch #2: Adding x{split_var} >= {lb[split_var]}')
            (obj2, sols2) = branch_and_bound_pruning_solve(c, A, b, lb, ub, best_sol_so_far, stats, depth+1, debug)
            lb[split_var] = tmp
            if obj2 == float('inf'): # unbounded 
                return (obj2, sols2)
            # compare solutions and return
            if obj1 < obj2: # which solution is larger?
                if debug:
                    indent()
                    print(f'Returning solution: {sols2} with objective {obj2}')
                return (obj2, sols2)
            else:
                if debug:
                    indent()
                    print(f'Returning solution: {sols1} with objective {obj1}')
                return (obj1, sols1)
    
'''
# example 1
c = [1, 1, -1]
A = [[1, -1, 0], [0, 1, -1], [1, 0, -1], [1, 1, 1]]
b = [2.5, 1.2, 3.1, 4.3]
lb = [-2, -2, -2]
ub = [2, 2, 2]
stats = Stats()
branch_and_bound_pruning_solve(c, A, b, lb, ub, Solution(), stats)
stats.print()


# example 2
c = [1, -2, 3]
A = [[1, -3, 0], [0, 3, -1], [2, 0, -3], [1, 1, 1]]
b = [7.1, 4, 5, 12.3]
lb = [-5, -5, -5]
ub = [5, 5, 5]
stats = Stats()

branch_and_bound_pruning_solve(c, A, b, lb, ub, Solution(), stats)
stats.print()

# example 3

c = [1, -2, 3]
A = [[1, -3, 0], [0, 3, -1], [2, 0, -3], [1, 1, 1]]
b = [7.1, 4, 5, 12.3]
lb = [-15, -15, -15]
ub = [15, 15, 15]
stats = Stats()
branch_and_bound_pruning_solve(c, A, b, lb, ub, Solution(), stats)
stats.print()
'''

# generate random problems
# WARNING!! this code tkes a long time to run

def formulate_random_problem_and_compare(n, m):
    c = [uniform(-3, 3) for i in range(n)]
    A = [[uniform(-1,1) for i in range(n)] for j in range(m)]
    b = [uniform(0,5) for i in range(m)]
    lb = [uniform(-10, -1) for i in range(n)]
    ub = [uniform(1, 10) for i in range(n)]
    stats0 = Stats()
    (obj1, _) = branch_and_bound_solve(c, A, b, lb, ub, stats0, debug=False)
    stats1 = Stats()
    (obj2, _) = branch_and_bound_pruning_solve(c, A, b, lb, ub, Solution(), stats1, debug=False)
    assert abs(obj2 - obj1) <= 0.01, f'Objectives do not match; {obj1} vs {obj2}'
    return (stats0.num_lps, stats1.num_lps)

bb_without_pruning = []
bb_with_pruning = []
for i in range(20):
    n = randint(3, 5)
    m = randint(3, 8)
    print(f'Problem # {i}, n = {n}, m = {m}')
    (m1, m2) = formulate_random_problem_and_compare(n, m)
    print(f'\t Without Pruning: {m1} LPs, With pruning: {m2} LPs')
    bb_without_pruning.append(m1)
    bb_with_pruning.append(m2)