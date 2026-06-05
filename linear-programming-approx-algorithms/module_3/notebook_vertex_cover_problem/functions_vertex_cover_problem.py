import networkx as nx
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from pulp import *

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

# find the optimal vertex cover solution

def compute_optimal_vertex_cover(n, edge_list):
    prob = LpProblem('vert_cover', LpMinimize)
    dvars = [LpVariable(f'w_{i}', cat='Binary') for i in range(1, n+1)]
    prob += lpSum(dvars) # minimuze the sum of the variables
    for (i, j) in edge_list:
        assert 1 <= i <= n 
        assert 1 <= j <= n
        prob += dvars[i-1] + dvars[j-1] >= 1 # wi + wj >= 1
    stat = prob.solve()
    assert stat == LpStatusOptimal
    vert_cover = [i+1 for i in range(n) if dvars[i].varValue > 0 ]
    return vert_cover

# the greedy solution by highest number of edges incident on a vertex

def greedy_vertex_cover(n, orig_edge_list): 
    edge_list = [(i,j) if i < j else (j,i) for (i,j) in orig_edge_list]
    # Construct an adjacency list representation -- for every vertex collect all incident edges.
    adj_list = [set() for i in range(n+1)]
    for (i, j) in edge_list:
        adj_list[i].add(j)
        adj_list[j].add(i)
    # store an array of degrees with the vertex id
    # negate the adjacency degree to get a maxheap
    degrees_with_vert_id = [(-float('inf'),0)] + [(len(adj_list[i]), i) for i in range(1,n+1)]
    num_edges_remaining = len(edge_list)
    # vertex cover list
    vert_cover = []
    while num_edges_remaining >= 1:
        max_degree_vert, vert_id = max(degrees_with_vert_id) # this would be faster if we used a priority queue
        print(f'Adding vertex: {vert_id} of degree {max_degree_vert} to the cover')
        vert_cover.append(vert_id)
        # now delete the edges incident on this vertex and update the degrees
        for j in adj_list[vert_id]: # iterate through all incident edges
            # remove all edges adjacent to vertex vert_id
            adj_list[j].remove(vert_id)
            num_edges_remaining -= 1
            # adjust the degrees
            (dj,_) = degrees_with_vert_id[j]
            degrees_with_vert_id[j] = (dj-1, j)
        degrees_with_vert_id[vert_id] = (0, vert_id)
        adj_list[vert_id] = set() 
    print('All edges removed')
    return vert_cover


  
def animate_algorithm_result(n, edge_list, vert_cover,ax):
    g = nx.Graph()
    g.add_edges_from(edge_list)
    pos = nx.spring_layout(g)  # positions for all nodes
    def update(i):
        ax.clear()
        vertices_in_cover = vert_cover[:i]
        edges_covered = [(i,j) for (i,j) in edge_list if i in vertices_in_cover or j in vertices_in_cover]
        vertices_not_in_cover = [i for i in range(1,n+1) if i not in vertices_in_cover]
        edges_not_yet_covered = [(i,j) for (i,j) in edge_list if i not in vertices_in_cover and j not in vertices_in_cover]
        nx.draw_networkx_nodes(g, pos, ax = ax, nodelist=vertices_in_cover, node_size=1000, node_color="tab:orange")
        nx.draw_networkx_nodes(g, pos, ax = ax, nodelist=vertices_not_in_cover, node_size=800, node_color="tab:blue")
        nx.draw_networkx_edges(g, pos, ax = ax, edgelist=edges_covered, edge_color="gray", style="dashed")
        nx.draw_networkx_edges(g, pos, ax = ax, edgelist=edges_not_yet_covered, edge_color="black")
        nx.draw_networkx_labels(g, pos, ax = ax, font_size=12, font_color="whitesmoke")
    ani = FuncAnimation(ax.figure, update, frames=len(vert_cover)+1)
    return ani

# poorly performing greedy althorithim

def make_bad_example_for_greedy(n):
    num_vertices = n # start with n vertices 
    edge_list = [] # empty list of edges
    vert_labels = [f'a_{i}' for  i in range(1, n+1)] # we will name the vertices a_1, ..., a_n so far
    for i in range(1, n+1): # run through i from 1 to n inclusive
        j_lim = n//i # compute floor(n/i)
        cur_vert = 1
        for j in range(1, j_lim+1):
            num_vertices = num_vertices + 1
            vert_labels.append(f'b_{i}^{(j)}') # add a new vertex label
            for k in range(i):
                edge_list.append((cur_vert+k, num_vertices)) # add edges from the vertex we just created
            cur_vert += i
    return (num_vertices, edge_list, vert_labels)

# based on removing the matching pair selected

def matching_based_vertex_cover(n, edge_list):
    vertex_cover = [] 
    remaining_edges = list(edge_list)
    while len(remaining_edges) > 0:
        (i,j) = remaining_edges[0]
        vertex_cover.append(i)
        vertex_cover.append(j)
        remaining_edges = [(l,m) for (l,m) in remaining_edges if l != i and l != j and m != i and m != j]
        print(f'adding nodes {i}, {j} to the cover')
    return vertex_cover