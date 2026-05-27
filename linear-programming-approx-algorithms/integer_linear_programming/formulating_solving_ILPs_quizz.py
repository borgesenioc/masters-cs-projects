from pulp import *

def solve_assignment():

    prob = LpProblem('ILP_Assignment', LpMaximize)

    # add decision variables
    x1 = LpVariable('x1', lowBound=-15, upBound=15)
    x2 = LpVariable('x2', lowBound=-15, upBound=15)
    x3 = LpVariable('x3', lowBound=-15, upBound=15)
    x4 = LpVariable('x4', lowBound=-15, upBound=15)
    x5 = LpVariable('x5', lowBound=-15, upBound=15)

    # objective function
    prob += 2*x1 - 3*x2 + x3

    # constraints
    prob += x1 - x2 + x3 <= 5
    prob += x1 - x2 + 4*x3 <= 7 
    prob += x1 + 2*x2 - x3 + x4 <= 14
    prob += x3 - x4 + x5 <= 7

    status = prob.solve()

    print(LpStatus[status])


solve_assignment()
