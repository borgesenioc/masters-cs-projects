from pulp import *

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