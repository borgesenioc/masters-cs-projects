from pulp import *

def plan_invite_list(n, m, T_lists, G_lists, pp_scores):
    assert m >= 0, 'Cannot invite a negative number of people'
    assert all( 0 <= j < n for ti in T_lists for j in ti ) # check that all employee IDs are valid
    assert all( 0<= j < n for gi in G_lists for j in gi)
    assert len(pp_scores) == n, 'Length of party pooper scores list does not match number of employees'
    prob = LpProblem('PartyPlanner', LpMinimize)
    # create decision variables
    dvars = [LpVariable(f'w_{i}', cat='Binary') for i in range(n)] # declare variables as binary
    # if we declared variables as binary they are automatically treated as either 0 or 1 in the optimization 
    # create objective
    prob += lpSum([si * wi for (si, wi) in zip(pp_scores, dvars)])
    # limit on number of invitees
    prob += sum(dvars) >= m
    # at least two people from each team
    for ti in T_lists:
        prob += lpSum([dvars[j] for j in ti]) >= len(ti)/4
    # no more than one person per grievance set
    for gj in G_lists:
        prob += lpSum(dvars[j] for j in gj) <= 1
    # solve and get the result
    status = prob.solve()
    if status == constants.LpStatusInfeasible:
        print('infeasible LP')
        return 
    elif status != constants.LpStatusOptimal:
        print('Unbounded or undefined LP Status -- there is some mistake in the problem formulation since it cannot happen in theory')
        return 
    else: 
        assert status == constants.LpStatusOptimal
        # extract values
        sol = [x.varValue for x in dvars]
        for (j,wj) in enumerate(sol):
            if wj >= 1:
                print(f'Invite person {j}')
        print(f'Total # of invitees: {sum(sol)}')
        for j,tj in enumerate(T_lists):
            print(f'# of invitees from Team # {j}: {sum([sol[k] for k in tj])}')
        for k, gk in enumerate(G_lists):
            print(f'# of invitees from Grievance set # {k}: {sum([sol[j] for j in gk])}')
        return
        