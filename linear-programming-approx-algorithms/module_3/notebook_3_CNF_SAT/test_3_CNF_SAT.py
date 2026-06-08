from formulas_3_CNF_SAT import *

## TEST

# Example 1

n = 5
lst_of_clauses = [
    [1, 3, -4],
    [2, -3, -5],
    [-1, -2, -4],
    [1, -2],
    [-1, 3, -5],
    [4, 5]
]

print(expectation(lst_of_clauses))

(n1, f1, c1) = assign_and_simplify(lst_of_clauses, 3, False)
print(f'{n1}, {f1}')
print(c1)

approx_max_sat(n, lst_of_clauses)

assign, num_clauses = approx_max_sat(n, lst_of_clauses)
print(f'Found assignment satisfying {num_clauses} clauses.')

for i in range(n):
    print(f'x_{i+1} --> {assign[i]}')

print(num_clauses_satisfied(lst_of_clauses, assign))

# Example 2
n = 9
lst_of_clauses = [
    [1, 4, -7],
    [-1, -3, -8],
    [2, 5, -7],
    [-2, -6, -9],
    [1, -4, -7],
    [-1, 4, 5],
    [4, 6, 9],
    [-7, -8, 9],
    [8, 9],
    [-9],
    [-8],
    [-6]
]
assign, num_clauses = approx_max_sat(n, lst_of_clauses)
print(f'Found assignment satisfying {num_clauses} clauses.')
for i in range(n):
    print(f'x_{i+1} --> {assign[i]}')

print(num_clauses_satisfied(lst_of_clauses, assign))