from pulp import *
from math import floor, ceil
from stats_b_n_b import *

# Given a list of numbers, find all indices in the list that correspond to fractional numbers.
# we use the function is_fractional to define what it means to be "fractional" -- we have to 
# account for floating point errors in this criterion
def find_all_fractional_indices(sols):
    n = len(sols)
    def is_fractional(f):
        epsilon = 0.001 # this is the precision to which we check whether something is an integer
        return  epsilon <= (f - floor(f)) <= 1-epsilon
    return [j for j in range(n) if is_fractional(sols[j]) ]

# This is the main function. 
# stats keeps track of statistics of number of LPs solved, infeasible and max. depth of recursion.
def branch_and_bound_solve(c, A, b, lb, ub, stats, depth=1, debug=True):
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
        
    if any(lb[i] > ub[i] for i in range(n)): # if any lower bound is greater than upper bound, problem is infeasible, BAIL
        if debug:
            indent()
            print('Infeasibility detected due to lb[i]> ub[i].')
        return (-float('inf'), None)
   
    # Record statistics
    if depth > stats.max_depth:
        stats.max_depth = depth
    stats.num_lps = stats.num_lps + 1
    ## 1. PART  1: Setup and Solve the LP Relaxation
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
            print('Infeasible Problem: returning -infty')
        stats.num_infeas = stats.num_infeas + 1
        return (-float('inf'), None) # return objective value of -infinity
    elif status == constants.LpStatusUnbounded: # unbounded
        if debug: 
            indent()
            print('Unbounded Problem: returning +infty')
        return (float('inf'), None) # return objective value of +infinity
    else: # optimal?
        assert status == LpStatusOptimal, 'Problem results in undefined status -- cannot continue'
        sols = [x.varValue for x in dvars] # extract the solutions for each decision variable
        obj_value = sum([ci*xi for (ci, xi) in zip(c, sols)]) # compute objective value
        if debug:
            indent()
            print(f'Obtained solution: {sols} with objective {obj_value}')
        ## PART 2: Branch and Bound Solve
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
            return (obj_value, sols) # done
        else:
            ## This is the part where we branch
            split_var = jList[0]
            assert 0 <= split_var < n
            if debug:
                indent()
                print(f'Splitting variable : {split_var} which has a current solution {sols[split_var]}')
            # adjust the upper bound 
            tmp = ub[split_var]
            ub[split_var] = floor(sols[split_var])
            if debug: 
                indent()
                print(f'Branch #1: Adding x{split_var} <= {ub[split_var]}')
            (obj1,sols1) = branch_and_bound_solve(c, A, b, lb, ub, stats, depth+1, debug)
            if obj1 == float('inf'):
                return (obj1, sols1)
            ub[split_var] = tmp
            # adjust the lower bound
            tmp = lb[split_var]
            lb[split_var] = ceil(sols[split_var])
            if debug: 
                indent()
                print(f'Branch #2: Adding x{split_var} >= {lb[split_var]}')
            (obj2, sols2) = branch_and_bound_solve(c, A, b, lb, ub, stats, depth+1, debug)
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


# example 1
c = [1, 1, -1]
A = [[1, -1, 0], [0, 1, -1], [1, 0, -1], [1, 1, 1]]
b = [2.5, 1.2, 3.1, 4.3]
lb = [-2, -2, -2]
ub = [2, 2, 2]
stats = Stats()
best_obj, best_solution = branch_and_bound_solve(c, A, b, lb, ub, stats)
stats.print()

'''
# example 2
c = [1, -2, 3]
A = [[1, -3, 0], [0, 3, -1], [2, 0, -3], [1, 1, 1]]
b = [7.1, 4, 5, 12.3]
lb = [-5, -5, -5]
ub = [5, 5, 5]
stats = Stats()
branch_and_bound_solve(c, A, b, lb, ub, stats)
stats.print()

# example 3
c = [1, -2, 3]
A = [[1, -3, 0], [0, 3, -1], [2, 0, -3], [1, 1, 1]]
b = [7.1, 4, 5, 12.3]
lb = [-15, -15, -15]
ub = [15, 15, 15]
stats = Stats()
branch_and_bound_solve(c, A, b, lb, ub, stats)
stats.print()
'''