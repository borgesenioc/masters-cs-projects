from pulp import *

# cat='Integer' turns this LP into an ILP
# remove that parameter to obtain the LP relaxation solution

def solve_assignment_1():

    prob = LpProblem('ILP_Assignment', LpMaximize)

    # add decision variables
    x1 = LpVariable('x1', lowBound=-15, upBound=15, cat='Integer')
    x2 = LpVariable('x2', lowBound=-15, upBound=15, cat='Integer')
    x3 = LpVariable('x3', lowBound=-15, upBound=15, cat='Integer')
    x4 = LpVariable('x4', lowBound=-15, upBound=15, cat='Integer')
    x5 = LpVariable('x5', lowBound=-15, upBound=15, cat='Integer')

    # objective function
    prob += 2*x1 - 3*x2 + x3

    # constraints
    prob += x1 - x2 + x3 <= 5
    prob += x1 - x2 + 4*x3 <= 7 
    prob += x1 + 2*x2 - x3 + x4 <= 14
    prob += x3 - x4 + x5 <= 7

    status = prob.solve()

    print(LpStatus[status])

# expect 40.00 from the ILP and LP relaxation solutions
solve_assignment_1()


def solve_assignment_2():

    prob = LpProblem('Minimize X', LpMinimize)

    # add decision variables
    x1 = LpVariable('x1', lowBound=-1, upBound=1, cat='Integer')
    x2 = LpVariable('x2', lowBound=-1, upBound=1, cat='Integer')
    x3 = LpVariable('x3', lowBound=-1, upBound=1, cat='Integer')

    # define the objective function
    prob += 2*x1 - 3*x2 + x3

    # add the constraints
    prob += x1 - x2 >= 0.5
    prob += x1 - x2 <= 0.75
    prob += x2 - x3 <= 1.25
    prob += x2 - x3 >= 0.95

    status = prob.solve()
    print(LpStatus[status])

# expect 'unfeasible' from the ILP and -0.25 from the LP relaxation solution
solve_assignment_2()
