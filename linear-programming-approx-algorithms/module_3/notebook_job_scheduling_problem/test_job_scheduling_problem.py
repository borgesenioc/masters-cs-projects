from notebook_job_scheduling_problem import *

'''
# integer LP solution test

(A, mkSpan) = formulate_min_makespan([2,1,4,2,1], 2)
print('Assignment')
print('----------------------')
for i in range(5):
    print(f'Task # {i+1} assigned to processor # {A[i]+1}')
print(f'MakeSpan is {mkSpan}')



# greedy solution test

A = greedy_jobshop_scheduling([2,1,4,2,1], 2)

'''
# test greedy + sorting
A = greedy_jobshop_scheduling_sorted([1,1,1,1,1,1,1,1,1,1,1,1,1,1,5], 4)

# compare to the approach without sorting
A = greedy_jobshop_scheduling([1,1,1,1,1,1,1,1,1,1,1,1,1,1,5], 4)