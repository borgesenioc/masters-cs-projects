from minimize_ILP_binary_problem import *
from random import randint

# Test number 1

n = 20
m = 12
T_lists = [[1, 5, 12, 18, 19], [2, 3, 4, 6, 7], [1, 2, 4, 7, 8, 9, 10, 11, 12, 14, 16], [1, 3, 4, 5, 6, 13, 15, 17, 18, 19], [1, 5, 7, 8,9, 19]]
G_lists = [[1, 5], [5, 19], [4, 7], [4, 12], [4, 19], [4, 18], [3, 4, 15, 19], [4, 7, 18, 2]]
pp_scores = [1, 2, 2, 1, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3.5, 1, 0.6, 0, 1, 8, 8]
plan_invite_list(n, m, T_lists, G_lists, pp_scores)

# Test number 2

n = 32
m = 18
num_teams = 30
num_grievances = 6
T_lists = [list(set([randint(0,31) for k in range(randint(3,10))])) for i in range(num_teams)] # 30 random teams
G_lists = [list(set([randint(0,31) for k in range(randint(2,4))])) for i in range(num_grievances)] # 6 random pairs of grievances
for i, ti in enumerate(T_lists):
    print(f'\t Team # {i}: {ti}')
for j, gj in enumerate(G_lists):
    print(f'\t Grievance set # {j}: {gj}')
pp_scores = [randint(0, 8) for i in range(n)]
plan_invite_list(n, m, T_lists, G_lists, pp_scores)