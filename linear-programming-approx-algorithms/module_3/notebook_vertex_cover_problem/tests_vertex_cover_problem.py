from functions_vertex_cover_problem import *
from random import randint

'''
# Example 1: draw the vertex cover with networkx and matplotlib

edge_list=[ (1,4), (1,5), (2,5), (2,4), (3,4), (4,5)]
vert_cover = [1,  4, 5]
plot_graph_with_vc(5, edge_list, vert_cover)

# and the smallest vertex cover:

edge_list=[ (1,4), (1,5), (2,5), (2,4), (3,4), (4,5)]
smaller_vert_cover = [4, 5]
plot_graph_with_vc(5, edge_list, smaller_vert_cover)



# test the greedy solution via highest number of incident edges on a vertex

edge_list=[ (1,4), (1,5), (2,5), (2,4), (3,4), (4,5)]
vcover = greedy_vertex_cover(5, edge_list)
#plot_graph_with_vc(5, edge_list, vcover)
fig, ax = plt.subplots(figsize=(6,4))
anim = animate_algorithm_result(5, edge_list, vcover, ax)
plt.show() 
plt.close(fig)


# comparison with the optimal vertex

edge_list=[ (1,4), (1,5), (2,5), (2,4), (3,4), (4,5)]
opt_vcover = compute_optimal_vertex_cover(5, edge_list)
print(opt_vcover)
print(f'Optimal vertex cover has {len(opt_vcover)} vertices')


# example 2:

edge_list=[ (1,4), (1,5), (2,5), (2,4), (3,4), (4,5),(1,8),(2,7), (7,8),(4,6), (5,7), (6,8), (3,1)]
vcover = greedy_vertex_cover(8, edge_list)
#plot_graph_with_vc(8, edge_list, vcover)
fig, ax = plt.subplots(figsize=(6,4))
anim = animate_algorithm_result(8, edge_list, vcover, ax)
plt.show() 
plt.close(fig)

# compare with optimal 

opt_vcover = compute_optimal_vertex_cover(8, edge_list)
print(opt_vcover)
print(f'Optimal vertex cover has {len(opt_vcover)} vertices')
plot_graph_with_vc(8, edge_list, opt_vcover)

# randomly generated graph

n = 25
edge_list = [ ]
for _ in range(120):
    i = randint(1, n)
    j = randint(1, n)
    if i == 0 or j == 0 or i == j or (i,j) in edge_list or (j,i) in edge_list: 
        continue
    edge_list.append((i,j))

vcover = greedy_vertex_cover(n, edge_list)
print(f'Size of cover: {len(vcover)}')
plot_graph_with_vc(n, edge_list, vcover)


n = 25
edge_list = [ ]
for _ in range(120):
    i = randint(1, n)
    j = randint(1, n)
    if i == 0 or j == 0 or i == j or (i,j) in edge_list or (j,i) in edge_list: 
        continue
    edge_list.append((i,j))

opt_vcover = compute_optimal_vertex_cover(n, edge_list)
print(opt_vcover)
print(f'Optimal vertex cover has {len(opt_vcover)} vertices')
plot_graph_with_vc(n, edge_list, opt_vcover)
'''

# test greedy based on matching pair of edges in a vertice

edge_list=[ (1,4), (1,5), (2,5), (2,4), (3,4), (4,5),(1,8),(2,7), (7,8),(4,6), (5,7), (6,8), (3,1)]
vcover = matching_based_vertex_cover(8, edge_list)
plot_graph_with_vc(8, edge_list, vcover)