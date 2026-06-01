from pulp import *
from math import sqrt 
from matplotlib import pyplot as plt


'''
Problem 2¶
Imagine you are operating a bunch of grocery stores across the country with  𝑛
  store locations numbered  0,…,𝑛−1
  wherein each location  𝑖
  has coordinates  (𝑥𝑖,𝑦𝑖)
 . The travel distance between locations  𝑖
  and  𝑗
  is given by  𝑑𝑖,𝑗=(𝑥𝑖−𝑥𝑗)2+(𝑦𝑖−𝑦𝑗)2⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯√
  (the Euclidean distance).

You are asked to locate warehouses among these  𝑛
  locations so that for each location  𝑗
 , the distance to the closest warehouse is less than some specified limit  𝑅≥0
 . Of course, you need to minimize the number of warehouses since warehouses are expensive to create and operate.

In this problem, we will formulate an integer linear program that will solve the problem of finding the minimum number or warehouses and their locations given inputs:

[(𝑥0,𝑦0),…,(𝑥𝑛−1,𝑦𝑛−1)]
 : the list of coordinates of the locations;
𝑅>0
  : the acceptable distance limit from each location to its nearest warehouse.

Let's begin to formulate an ILP to compute the minimum number of warehouses.

(A) Identifying Decision Variables
We will have binary decision variable  𝑤𝑖
  corresponding to each location  𝑖∈{0,…,𝑛−1}
  wherein

𝑤𝑖={1,0,if we locate a warehouse at location 𝑖otherwise
 

(B) Objective function
Express the number of warehouses created in terms of the decision variables  𝑤0,…,𝑤𝑛−1
 . This will give us the objective that we will minimize.

 my_answer = {
    minimize sum(w_i for i in range(n))
 }


 (C) Constraints
Let's consider from the point of view of each location  𝑗
  in our list. We would like at least one warehouse to be located at a location  𝑖
  where  𝑑𝑖,𝑗≤𝑅
 .

Define the set  𝐷𝑗={𝑖 | 𝑑𝑖,𝑗≤𝑅}
  to be all locations within distance  𝑅
  from  𝑗
  (this set includes  𝑗
  as well since  𝑑𝑗,𝑗=0
 ).

Write down the constraint that at least one warehouse must be located among the locations in the set  𝐷𝑗.

my_answer = {

s.t. = sum(w_i for i in range(n) if D[i][j] <= R) >= 1 

}

'''

# Problem 2

def euclidean_distance(location_coords, i, j):
    assert 0 <= i and i < len(location_coords)
    assert 0 <= j and j < len(location_coords)
    if i == j: 
        return 0.0
    (xi, yi) = location_coords[i] # unpack coordinate
    (xj, yj) = location_coords[j]
    return sqrt( (xj - xi)**2 + (yj - yi)**2 )

    
def solve_warehouse_location(location_coords, R):
    assert R > 0.0, 'radius must be positive'
    n = len(location_coords)
    prob = LpProblem('Warehouselocation', LpMinimize)
    #1. Formulate the decision variables
    #2. Add the constraints for each vertex and edge in the graph.
    #3. Solve and interpret the status of the solution.
    #4. Return the result in the required form to pass the tests below.
    # your code here

    # 1. the decision variables

    w_i_selected = []

    for i in range(n):
        w_i_selected.append(LpVariable(f'w_i_{i}', cat='Binary'))

    # 1.2 the objective function

    prob += lpSum(w_i_selected)
    
    # 2. the constraints

    for j in range(n):
      prob += lpSum(w_i_selected[i] for i in range(n)
                  if euclidean_distance(location_coords, i, j) <= R) >= 1 

    # 3. solve

    prob.solve()

    return [ i for i in range(n) if value(w_i_selected[i]) == 1]
    raise NotImplementedError


def check_solution(location_coords, R, warehouse_locs):
    # for each location i, calculate all locations j within distance R of location i
    # use list comprehension instead of accumulating using a nested for loop.
    n = len(location_coords)
    assert all(j >= 0 and j < n for j in warehouse_locs), f'Warehouse locations must be between 0 and {n-1}'
    neighborhoods = [ [j for j in range(n) if euclidean_distance(location_coords, i, j) <= R] for i in range(n)]
    W = set(warehouse_locs)
    for (i, n_list)  in enumerate(neighborhoods):
        assert any(j in W for j in n_list), f'Location # {i} has no warehouse within distance {R}. The locations within distance {R} are {n_list}'
    print('Your solution passed test')
    
def visualize_solution(location_coords, R, warehouse_locs):
    n = len(location_coords)
    (xCoords, yCoords) = zip(*location_coords)
    warehouse_x, warehouse_y = [xCoords[j] for j in warehouse_locs], [yCoords[j] for j in warehouse_locs]
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    plt.scatter(xCoords, yCoords)
    for j in warehouse_locs: 
        circ = plt.Circle(location_coords[j], R, alpha=0.5, color='g',ls='--',lw=2,ec='k')
        ax.add_patch(circ)
    
    for i in range(n):
        (x,y) = location_coords[i]
        ax.annotate(f'{i}', location_coords[i])
    
    plt.scatter(warehouse_x, warehouse_y, marker='x',c='r', s=30)
        
    
    
    
location_coords = [(1,1), (1, 2), (2, 3), (1, 4), (5, 1), (3, 3), (4,4), (1,6), (0,3), (3,5), (2,4)]

## TEST 1

R = 2
print("R = 2 Test:")
locs = solve_warehouse_location(location_coords, R )
print(f'Your code returned warehouse locatitons: {locs}')
assert len(locs) <= 4, f'Error: There is an solution involving just 4 locations whereas your code returns {len(locs)}'
visualize_solution(location_coords, R, locs)
check_solution(location_coords, R, locs)
print('Test with R= 2 has passed')


## TEST 2

print("R=3 Test:")
R = 3
locs3 = solve_warehouse_location(location_coords, R )
print(f'Your code returned warehouse locatitons: {locs3}')
assert len(locs3) <= 2, f'Error: There is an solution involving just 4 locations whereas your code returns {len(locs)}'
visualize_solution(location_coords, R, locs3)
check_solution(location_coords, R, locs3)
print("Test with R = 3 has passed.")