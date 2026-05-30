import networkx as nx
from matplotlib import pyplot as plt
from pylab import rcParams
from pulp import *
from random import randint

# Use matplotlib and networkx to plot graphs with a designated
# vertex cover passed in as a list of vertices.
# n: number of vertices
# edge_list: list of edges. please ensure that if edge (i,j) 
#            is present then (j,i) is not. We will not be checking this.
# vert_cover: list of vertices in the cover to highlight in orange.
# All nodes will be plotted in blue with vertex cover highlighted in orange.
def plot_graph_with_vc(n, edge_list, vert_cover):
    g = nx.Graph()
    g.add_edges_from(edge_list)
    pos = nx.spring_layout(g)  # positions for all nodes
    not_vert_cover = [i for i in range(1, n+1) if i not in vert_cover]
    plt.figure(1)
    nx.draw_networkx_nodes(g, pos, nodelist=vert_cover,  node_color="tab:orange")
    nx.draw_networkx_nodes(g, pos, nodelist=not_vert_cover,  node_color="tab:blue")
    nx.draw_networkx_edges(g, pos, edgelist=edge_list)
    nx.draw_networkx_labels(g, pos, font_size=12, font_color="whitesmoke")
    plt.show()

'''
# case 1
edge_list_1=[ (1,4), (1,5), (2,5), (2,4), (3,4), (4,5)]
vert_cover = [1,  4, 5]
plot_graph_with_vc(5, edge_list_1, vert_cover)
'''

'''
# case 2
edge_list_2=[ (1,4), (1,5), (2,5), (2,4), (3,4), (4,5)]
smaller_vert_cover = [4, 5]
plot_graph_with_vc(5, edge_list_2, smaller_vert_cover)
'''

# solving vertex cover problems as ILPs

def compute_optimal_vertex_cover(n, edge_list):
    # Create a problem -- indicate that we will minimize the objectives
    prob = LpProblem('vert_cover', LpMinimize)
    # Add all the decision vars (we do this using comprehensions in Python but you could write a for-loop as well)
    dvars = [LpVariable(f'w_{i}', cat='Binary') for i in range(1, n+1)]
    # Note that lpSum is defined in Pulp and it simply takes the sum of all variables in a list of vars.
    prob += lpSum(dvars) # minimize the sum of the variables
    for (i, j) in edge_list: # go through each edge in the list
        assert 1 <= i <= n 
        assert 1 <= j <= n
        prob += dvars[i-1] + dvars[j-1] >= 1 # add the constraint -- wi + wj >= 1 -- indexing in python starts from 0 and thus we require the -1
    stat = prob.solve() # solve the problem
    assert stat == LpStatusOptimal, 'Problem does not have optimal status -- something went wrong -- this should not happen for this problem'
    vert_cover = [i+1 for i in range(n) if dvars[i].varValue > 0 ]
    return vert_cover

'''
# case 3
edge_list_3=[ (1,4), (1,5), (2,5), (2,4), (3,4), (4,5)]
opt_vcover = compute_optimal_vertex_cover(5, edge_list_3)
print(opt_vcover)
print(f'Optimal vertex cover has {len(opt_vcover)} vertices: {opt_vcover}')
plot_graph_with_vc(5, edge_list_3, opt_vcover)
'''

'''
$ case 4
edge_list_4=[ (1,4), (1,5), (2,5), (2,4), (3,4), (4,5),(1,8),(2,7), (7,8),(4,6), (5,7), (6,8), (3,1)]
vcover = compute_optimal_vertex_cover(8, edge_list_4)
plot_graph_with_vc(8, edge_list_4, vcover)
'''

# case 5: graph with 40 vertices and 240 edges
n = 40
edge_list_5 = [ ]
for _ in range(240):
    i = randint(1, n)
    j = randint(1, n)
    if i == 0 or j == 0 or i == j or (i,j) in edge_list_5 or (j,i) in edge_list_5: 
        continue
    edge_list_5.append((i,j))

vcover = compute_optimal_vertex_cover(n, edge_list_5)
print(f'Size of cover: {len(vcover)} consisting of vertices {vcover}')
plot_graph_with_vc(n, edge_list_5, vcover)