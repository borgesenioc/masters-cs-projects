class Stats:
    def __init__(self):
        self.max_depth = 0
        self.num_lps = 0
        self.num_infeas = 0
        self.best_obj = -float('inf')
        self.best_solution = None
        
    def print(self):
        print('Statistics')
        print('---------------------------------')
        print(f'Number of LPs Solved: {self.num_lps}')
        print(f'Number of infeasible LPs: {self.num_infeas}')
        print(f'Max. Recursion Depth: {self.max_depth}')
        print(f'Best objective: {self.best_obj}')
        print(f'Best solution: {self.best_solution}')
        print('---------------------------------')