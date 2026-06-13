'''
P2: k-Centers Clustering Problem
You are given a set of points 𝑃1,…,𝑃𝑛 on a plane where for each point 𝑃𝑖 we provide its coordinates (𝑥𝑖,𝑦𝑖). The goal is to select 𝑘 points out of 𝑛 as centers. Once we select 𝑘 such centers 𝐶1,…,𝐶𝑘 from among the points 𝑃1,…,𝑃𝑛, we define for every point 𝑃𝑖 the distance 𝑟𝑖 as the distance from 𝑃𝑖 to its nearest center:
𝑟𝑖 = min(𝑗=1..𝑘) 𝖽𝗂𝗌𝗍𝖺𝗇𝖼𝖾(𝑃𝑖, 𝐶𝑗).

Here we use Euclidean distance: 𝖽𝗂𝗌𝗍𝖺𝗇𝖼𝖾((𝑥1,𝑦1),(𝑥2,𝑦2)) = sqrt((𝑥2−𝑥1)² + (𝑦2−𝑦1)²). Also note that the distance 𝑟𝑖 depends on which points we choose as centers. For instance, if a point 𝑃𝑖 is chosen as one of the centers, then its distance 𝑟𝑖=0.

Having chosen 𝑘 centers 𝐶1,…,𝐶𝑘, we define 𝑅(𝐶1,…,𝐶𝑘) = max(𝑟1,…,𝑟𝑛) as the maximum distance from any point to its nearest center. It is clear then that if we placed a circle of radius 𝑅(𝐶1,…,𝐶𝑘) around every center, then all points belong to the circle.

Our goal is to choose 𝑘 centers such that we minimize the value of 𝑅 as defined above.
𝖿𝗂𝗇𝖽 𝖼𝖾𝗇𝗍𝖾𝗋𝗌 𝐶1,…,𝐶𝑘 𝗌.𝗍. 𝑅(𝐶1,…,𝐶𝑘) 𝗂𝗌 𝗆𝗂𝗇𝗂𝗆𝗂𝗓𝖾𝖽
'''

'''
Example
Suppose we have 10 points 𝑃1,…,𝑃10 with the coordinates:
𝑃1:(1,2), 𝑃2:(3,5), 𝑃3:(4,7), 𝑃4:(8,14), 𝑃5:(9,3), 𝑃6:(7,7), 𝑃7:(6,5), 𝑃8:(4,6), 𝑃9:(5,2), 𝑃10:(1,8).

We choose 𝑘=2 centers whose indices are in the list center_indices. In this instance, we have chosen 𝑃3 and 𝑃7. The calculation of 𝑅(𝐶1,𝐶2) proceeds as shown below to obtain the value 𝑅=8.062.
'''

from math import sqrt 
from matplotlib import pyplot as plt 


def euclidean_distance(a, b):
    (xa, ya) = a
    (xb, yb) = b
    return sqrt( (xb - xa)**2 + (yb - ya)**2)

def calculate_R(coords, center_indices):
    n = len(coords)
    assert all( 0 <= j < n for j in center_indices)
    rj_values = [ min([euclidean_distance(xj, coords[j]) for j in center_indices]) for xj in coords]
    return max(rj_values)

def plot_coords(coords, center_indices):
    R = calculate_R(coords, center_indices)
    coords_x = [x for (x,y) in coords]
    coords_y = [y for (x, y) in coords]
    centers_x = [coords_x[j] for j in center_indices]
    centers_y = [coords_y[j] for j in center_indices]
    figure, axes = plt.subplots()
    axes.axis('equal')
    for k in center_indices:
        c = plt.Circle(coords[k], R, fill=True, alpha=0.5, facecolor='lightblue', clip_on=False, edgecolor='black', linewidth=1, linestyle='dashed')
        axes.add_artist(c)
    plt.scatter(coords_x, coords_y, s=30, marker='x' )
    plt.scatter(centers_x, centers_y, s=50, marker='o')
    plt.show()
    
coords = [(1,2), (3,5), (4,7), (8, 14), (9,3), (7,7), (6,5), (4, 6), (5,2), (1,8)]
center_indices = [2, 6] # remember indexing starts from 0 in python arrays
R = calculate_R(coords, center_indices)
print(f'R = {R}')
plot_coords(coords, center_indices)

'''
coords = [(1,2), (3,5), (4,7), (8, 14), (9,3), (7,7), (6,5), (4, 6), (5,2), (1,8)]
center_indices = [1, 5] # remember indexing starts from 0 in python arrays
R = calculate_R(coords, center_indices)
print(f'R = {R}')
plot_coords(coords, center_indices)
'''

'''
In the example above, we ask which set of k=2 centers yields the minimum radius R.

## Solving the k-center problem

The k-center problem is NP-complete. The obvious algorithm — trying all
combinations of k points out of n — has complexity O(n^k), exponential in k.

A simple greedy algorithm:

  1. C = { P_1 }                         # start with the first point as a center
  2. for j = 2 to k:
       a. (P_j, r_j) = find_farthest_point_from_current_centers([P_1,...,P_n], C)
       b. C = C ∪ { P_j }
  3. (P_{k+1}, R) = find_farthest_point_from_current_centers([P_1,...,P_n], C)
  4. return centers C, radius R

find_farthest_point_from_current_centers goes over all points and returns the
point P_j whose distance to its closest center (r_j) is the largest among all
points. It returns both P_j and r_j. The final call after the loop isn't needed
to build C, but it gives us R and is useful for the analysis later.
'''

def euclidean_distance(a, b):
    (xa, ya) = a
    (xb, yb) = b
    return sqrt( (xb - xa)**2 + (yb - ya)**2)


# Function find_farthest_point_from_current_centers
# returns a pair (j, rj) where 
# - 0 <= j < len(coords) is the index of the farthest point P_j
# - rj is the distance of the point P_j from its nearest center
def find_farthest_point_from_current_centers(coords, center_indices):
    n = len(coords)
    assert all( 0 <= j < n for j in center_indices)
    rj_values = [ (min([euclidean_distance(xi, coords[j]) for j in center_indices]), i) for (i, xi) in enumerate(coords)]
    (rj, j) = max(rj_values)
    return (j, rj)

## Implement a function greedy_k_centers that given a list of coordinates `coords`, returns center_list, R
##   - centers_list is a list of indices [j1,..., jk]. Note that coords[j1], ..., coords[jk] will yield coordinates of the actual centetr.
##   - R is the radius resulting from the choice of the k centers
## Please use the implementation of find_farthest_point_from_current_centers above.
def greedy_k_centers(coords, k, debug=True): ## Please print messages from this function only if debug flag is True
    centers = [0] # Add the very first point 
    if debug:
        print(f'Initial center: {coords[0]}')
    # your code here

    # 2. for j = 2 to k:
    while len(centers) < k:
        # a. (P_j, r_j) = find_farthest_point_from_current_centers([P_1,...,P_n], C)
        (P_j, r_j) = find_farthest_point_from_current_centers(coords, centers)
        # b. C = C ∪ { P_j }
        centers.append(P_j)

    # 3. (P_{k+1}, R) = find_farthest_point_from_current_centers([P_1,...,P_n], C)
    (P_j, R) = find_farthest_point_from_current_centers(coords, centers)

    # 4. return centers C, radius R
    return centers, R
    