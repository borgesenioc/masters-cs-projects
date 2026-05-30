from pulp import *

''' 
Problem 1
In this problem, you will setup and solve the three coloring problem as a integer linear programming problem.

The three coloring problem inputs an undirected graph  𝐺
  with vertices  𝑉={0,…,𝑛−1}
  and undirected edges  𝐸
 . We are looking to color each vertex one of three colors red, green or blue such that for any edge  (𝑖,𝑗)
  the nodes  𝑖,𝑗
  have different colors.

Given a graph, we wish to know if a three coloring is possible and if so, we wish to find the three coloring. Although this problem seems like a toy problem, it has applications to many practical problems in resource allocation and other areas.

First, we ask you to setup the three coloring problem as an integer linear program.

Decision variables
For each vertex  𝑖∈𝑉
 , we will use three decision variables  𝑥𝑅𝑖,𝑥𝐺𝑖
  and  𝑥𝐵𝑖
  that indicate whether the vertex if colored red, green or blue, respectively. Note that these are all binary variables taking on  0,1
  values.

(A) Each vertex can take just one color
Write down a constraint that says that each vertex must be colored exactly one of three colors: red, green or blue in terms of  𝑥𝑅𝑖,𝑥𝐺𝑖
  and  𝑥𝐵𝑖.

  my_answer = "
  for i in V:
    x_Ri + x_Gi + x_Bi == 1
  "

(B) Adjacent vertices cannot be the same color.
Write down constraints for each edge  (𝑖,𝑗)∈𝐸
  that they cannot be the same color. Hint Write down three constraints that express that the vertices  𝑖,𝑗
  cannot both be green, cannot both be red and cannot both be blue respectively. Translate these requirements into constraints involving  𝑥𝐺𝑖,𝑥𝐺𝑗
 ,  𝑥𝑅𝑖,𝑥𝑅𝑗
  and  𝑥𝐵𝑖,𝑥𝐵𝑗.

  my_answer = "
  for (i,j) in E:
    (x_Ri + x_Rj) <= 1 
    (x_Gi + x_Gj) <= 1 
    (x_Bi + x_Bj) <= 1
    "

    Write a function encodeAndSolveThreeColoring(n, edge_list) that given the number of vertices  𝑛≥1
  and the list of edges as a list of pairs of vertices [ (i1, j1), (i2, j2) ..., (im, jm) ] returns a tuple (flag, color_assignment) consisting of boolean flag and a list color_assignment, wherein
  flag is True if the graph is three colorable and False if not.

  color_assignment is a list of n colors r, g, or b (standing for red, green or blue) where the  𝑖𝑡ℎ
  element of the list stands for the color assigned to vertex  𝑖.

   Note that the color_assignment component of the return value is ignored if flag is set to False.
'''

def encode_and_solve_three_coloring(n, edge_list):
    assert n >= 1, 'Graph must have at least one vertex'
    assert all( 0 <= i and i < n and 0 <= j and j < n and i != j for (i,j) in edge_list ), 'Edge list is not well formed'
    prob = LpProblem('Three Color', LpMinimize)
    #1. Formulate the decision variables
    
    colors = ['r', 'g', 'b']

    x_r = []
    x_g = []
    x_b = []
    
    for i in range(n):
        x_r.append(LpVariable(f'x_r_{i}', cat='Binary'))
        x_g.append(LpVariable(f'x_g_{i}', cat='Binary'))
        x_b.append(LpVariable(f'x_b_{i}', cat='Binary'))

    #2. Add the constraints for each vertex and edge in the graph.

    prob += lpSum([])

    for i in range(n):
        prob += x_r[i] + x_g[i] + x_b[i] == 1
    
    for (i,j) in edge_list:
        prob += x_r[i] + x_r[j] <= 1
        prob += x_g[i] + x_g[j] <= 1
        prob += x_b[i] + x_b[j] <= 1

    #3. Solve and interpret the status of the solution.

    prob.solve()
    flag = LpStatus[prob.status] == 'Optimal'

    color_assignment = []
    for i in range(n):
        if value(x_r[i]) == 1:
            color_assignment.append(colors[0])
        elif value(x_g[i]) == 1:
            color_assignment.append(colors[1])
        else:
            color_assignment.append(colors[2])

    #4. Return the result in the required form to pass the tests below.
    # your code here

    if flag:
        return (flag, color_assignment)
    else:
        return (flag, [])