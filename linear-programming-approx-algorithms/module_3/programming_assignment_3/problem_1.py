import networkx as nx
from matplotlib import pyplot as plt 
from random import *

'''

P1: Max-Cut Problem
We will guide you through the design of a factor-2 approximation algorithm for the Max-Cut problem. You are given an undirected graph 𝐺
 with 𝑛
 vertices and 𝑚
 edges.

The maxcut problem asks you to partition the vertices into two subsets 𝑆+
 and 𝑆−
 such that the total number of edges crossing the cut is as large as possible.
𝗆𝖺𝗑 ||{(𝑖,𝑗)∈𝐸 | 𝑖∈𝑆+, 𝑗∈𝑆−, 𝑆+∩𝑆−=∅,𝑆+∪𝑆−=𝑉}||

Example
Consider the graph below:

'''

def draw_graph(n, edge_list, node_set_flag, set1_color='lightblue', set2_color='red'):
    # get the list of nodes in various sets and edges that are cut and uncut
    set1_nodes = [i for i in range(1, n+1) if node_set_flag[i-1] == True]
    set2_nodes = [i for i in range(1, n+1) if node_set_flag[i-1] == False]
    edge_list_not_cut = [(i,j) for (i,j) in edge_list if node_set_flag[i-1] == node_set_flag[j-1] ]
    edge_list_cut = [(i,j) for (i,j) in edge_list if node_set_flag[i-1] != node_set_flag[j-1] ]
    # now draw the graph
    G = nx.Graph()
    G.add_edges_from(edge_list)
    pos = nx.spring_layout(G, seed=1234)
    plt.figure()
    nx.draw_networkx_nodes(G, pos, nodelist=set1_nodes, node_color=set1_color)
    if len(set2_nodes) >= 1:
        nx.draw_networkx_nodes(G, pos, nodelist=set2_nodes, node_color=set2_color, alpha=0.5)
    
    labels = {i:i for i in range(1, n+1)}
    nx.draw_networkx_labels(G, pos,  labels=labels)
    
    nx.draw_networkx_edges(G, pos, width=2, edgelist = edge_list_not_cut)
    nx.draw_networkx_edges(G, pos, width=2, edgelist = edge_list_cut, edge_color='red')
    plt.show()
    
'''
n = 5
edges = [(1,2),(1,3),(1,4),(1,5), (2,3),(2,4),(3,5),(4,5)]
node_set_flag = [True, True, True, True, True] # all nodes are in set1
draw_graph(5, edges, node_set_flag)
'''


'''
We would like to partition the set  {1,…,5}
  into two subsets  𝑆1,𝑆2
  so that the number of edges going from a vertex in  𝑆1
  to a vertex in  𝑆2
  is as large as possible.

First Cut
Suppose we set  𝑆1={1,2,3}
  and therefore,  𝑆2={4,5}
 , we have a cut with  4
  edges crossing it.
'''
'''
Second Cut
We can do better by setting  𝑆1={1,2,5}
  and  𝑆2={3,4}
  with  6
  edges crossing the cut.

'''

'''
n = 5
edges = [(1,2),(1,3),(1,4),(1,5), (2,3),(2,4),(3,5),(4,5)]
node_set_flag = [True, True, True, False, False] # 1, 2, 3 are in set1
draw_graph(5, edges, node_set_flag)
'''

'''
Therefore, the MAXCUT problem asks you to find a cut with as many edges as possible crossing the cut. This problem is often encountered in applications such as circuit layout in chip design where we have a graph between the circuit components and the edges are formed by wires going between these components.

MAXCUT is known to be NP-complete though we will not ask you to prove it here. The goal of this problem is to design a greedy algorithm and prove an approximation guarantee.

Greedy Algorithm
Suppose you have a graph  𝐺
  and we propose a partition of the vertices  𝑆1,𝑆2
 . We say that a node  𝑣
  is imbalanced if it has strictly more number of edges to other nodes within its partition than edges crossing the cut.

Examples
As an example, consider the graphs shown above and the first cut we showed above with  𝑆1={1,2,3}
  and  𝑆2={4,5}
 . Notice that vertices  2
  and  3
  are imbalanced.

However, if we consider the second cut of the graph above, we have  𝑆1={1,2,5}
  and  𝑆2={3,4}
  we see that all nodes are balanced in this cut.

P1: Design a Greedy Algorithm
Design a greedy algorithm that starts from an arbitrary (random?) initial partition, detects if there are imbalanced vertices and uses that information to find a partition with a better cut. Your algorithm should yield a partition with no imabalanced nodes in the final result.

Write down the pseudocode and prove that the algorithm terminates/find its time complexity.

Note These problems are meant for you to develop your own thinking/problem solving and will not be graded due to the online nature of this class. We will be grading just the programming assignments based on test cases. The answers to select questions are given at the end of the notebook.
'''

# My answer
'''
MaxCutGreedy(G = (V, E)):

# divide the initial partition arbitrarily
S1 are the initial n/2 vertices of V
S2 are the remaining n/2 vertices of V

# evaluate if each node of each set dividion is imbalanced
while there exists an imbalanced vertex v in V:
  flip v to the opposite partition

return (S1, S2)
'''

'''
P2: Implement the Greedy Algorithm
Now let's implement the greedy algorithm to find a cut of the graph with no imbalanced vertices.

The graph will be given as an adjacency list representation.

Vertex set will be  {0,…,𝑛−1}
  where  𝑛 (the number of vertices) is a input parameter.
adj_list is an adjacency list which is given as a list of sets. For instance adj_list[i] for a vertex  𝑖 is a set to all vertices connected to vertex  𝑖.
Note that since the graph is undirected, if  𝑗 lies in adj_list[i], we know that  𝑖 will be in adj_list[j].
You can assume that the graph has no self loops or multiple edges between same pairs of nodes. We will specify a cut as a list of  𝑛 boolean values [b0, b1,...bn-1] wherein bi is True if  𝑖∈𝑆1, and False if vertex  𝑖 ∈ 𝑆2
 .
Implement the overall function find_balanced_cut that takes a graph as input and returns a list of Booleans specifying the final cut obtained by running the greedy algorithm. Please pay attention to efficiency, we will be running some large graphs through your code and it should run within a few seconds on graphs with thousands of nodes.
'''

# This is the function that you will implement the greedy algorithm
# It should input a graph as an adjacency list and return a partition where 
# every vertex is balanced, as described above.
# Return a list of Booleans of size n, wherein for any vertex v, if list[v] = True then 
# it belongs to partition S1 otherwise to partition S2.
def find_balanced_cut(n, adj_list): 
    assert n >= 1
    assert len(adj_list) == n
    # Check that the adjacency list makes sense and represents a directed graph
    for (i, neighbors) in enumerate(adj_list):
        assert all( 0 <= j < n for j in neighbors )
        assert i not in neighbors # no self loops allowed
        for j in neighbors: 
            assert i in adj_list[j]
    # just start with an initial cut tthat places first n/2 nodes in S1 and rest in S2.
    cut = [True if i < n/2 else False for i in range(n)]
    ## TODO: now run the greedy algorithm. It will be helpful to have helper functions to find 
    ## imbalanced_vertices, maintain an array with the number of edges for each node that are cut and so on.
    ## Note: your algorithm must return a cut where all nodes are balanced.
    # your code here

    # look for a vertex that has more edges inside its own partition than crossing the cut. return its index, or None if every vertex is balanced
    def find_imbalanced_vertex():
        for v in range(n):
            internal = 0
            crossing = 0
            for u in adj_list[v]:
                if cut[u] == cut[v]:
                    internal += 1
                else:
                    crossing += 1
            if internal > crossing:
                return v
        return None

    # while there exists an imbalanced vertex v in V
    v = find_imbalanced_vertex()
    while v is not None:
        # flip v to the opposite partition
        cut[v] = not cut[v]
        v = find_imbalanced_vertex()

    return cut

#These  are useful functions for the test cases
# IMPORTANT: 
# Please ensure that you run these cells before running test cases or else you may get unknown function errors.

# Make an adjacency list out of a list of edges.
def mk_adjacency_list(n, edge_list):
    adj_list = [set() for i in range(n)]
    for (i,j) in edge_list:
        adj_list[i].add(j)
        adj_list[j].add(i)
    return adj_list

# Test Partition
def test_cut(n, adj_list, cut):
    num_edges_crossing_cut = [0]*n
    for (i, neighbors) in enumerate(adj_list):
        num_edges_crossing_cut[i] = sum([cut[i] != cut[j] for j in neighbors])
        if 2 * num_edges_crossing_cut[i] < len(neighbors):
            assert False, f'Test Failed: In your cut, vertex {i} has {len(neighbors)} edges incident on it but only {num_edges_crossing_cut[i]} edges cross the cut'
    return 



