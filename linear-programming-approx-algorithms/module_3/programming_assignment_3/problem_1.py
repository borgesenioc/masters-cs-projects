import networkx as nx
from matplotlib import pyplot as plt 

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

