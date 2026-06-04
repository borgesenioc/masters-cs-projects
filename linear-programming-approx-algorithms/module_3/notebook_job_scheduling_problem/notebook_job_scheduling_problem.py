from pulp import *

# integer linear programming formulation

def formulate_min_makespan(task_times, m):
    n = len(task_times)
    assert m < n
    prob = LpProblem('min-makespan', LpMinimize)
    # create a list of list of indicator variables w_i_j
    indicator_vars = [ [LpVariable(f'w_{i}_{j}', cat='Binary') for j in range(m)] for i in range(n) ]
    M = LpVariable('M', cat='Continuous') # create a variable M for makespan -- it is real-valued
    # set objective
    prob += M
    # add constraints
    # each task must be assigned to exactly one processor
    for i in range(n): # for each task
        prob += lpSum(indicator_vars[i]) == 1
    # working time for each processor must be less than the makespan
    for j in range(m):
        vars_i = [indicator_vars[i][j] for i in range(n)]
        prob += lpDot(task_times, vars_i) <= M # lpDot is a very useful function that pulp supports to take dot product of two lists
    # solve and extract answer
    prob.solve()
    assert prob.status == constants.LpStatusOptimal
    # extract the job assignment
    A = []
    for i in range(n):
        w_list = indicator_vars[i]
        ## TODO: Replace code below using a suitable python list API function
        assigned_proc = None
        for j in range(m):
            if w_list[j].varValue > 0:
                assigned_proc = j
                break
        assert assigned_proc != None, f'Task # {i} did not get assigned to any processor. There is a bug in problem formulation'
        A.append(assigned_proc)
    return (A, M.varValue)


# greedy solution

def greedy_jobshop_scheduling(timings, m):
    n = len(timings)
    A = []
    K = [(0,j) for j in range(m)] # for simplicity of coding maintain K as a array of tuples consisting of timing and processor index
    for i in range(n):
        print(f'K = {K}')
        (min_proc_timing, min_proc_idx) = min(K) # this can be improvedd using a priority queue but right now this will take O(m) time
        A.append(min_proc_idx) 
        print(f'Task {i} assigned to processor {min_proc_idx}')
        K[min_proc_idx] = (min_proc_timing + timings[i], min_proc_idx) # update the array K
    print(f'K = {K}')
    makeSpan, max_proc_idx = max(K)
    print(f'Make span = {makeSpan}')
    return A

# greedy + sorting

def greedy_jobshop_scheduling_sorted(T, m):
    # First sort the array T provided but as we do so remember the indices in the old array
    # When we refer to Task # i, we are refering to its index in the array T.
    timings = [(ti, j) for (j, ti) in enumerate(T)] # Store each task and index
    timings.sort(reverse=True) # Sort it in reverse order
    n = len(timings)
    A = [-1] * n # Initialize the assignment to -1 (dummy value)
    K = [(0,j) for j in range(m)] # for simplicity of coding maintain K as a array of tuples consisting of timing and processor index
    for (ti, ti_idx) in timings: # iterate through the array of times and indices into original array
        print(f'K = {K}')
        (min_proc_timing, min_proc_idx) = min(K) # this can be improved using a priority queue but right now this will take O(m) time
        A[ti_idx]= min_proc_idx # Assign the task ti_idx to processor min_proc_idx with minimum load so far.
        print(f'Task {ti_idx} assigned to processor {min_proc_idx}') 
        K[min_proc_idx] = (min_proc_timing + ti, min_proc_idx) # update the array K
    print(f'K = {K}')
    makeSpan, max_proc_idx = max(K)
    print(f'Make span = {makeSpan}')
    return A