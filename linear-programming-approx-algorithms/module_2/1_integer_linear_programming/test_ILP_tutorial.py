from ILP_tutorial_on_pulp import *

n = 5
candy_number_limits = [10, 12, 10, 11, 10]
candy_prices = [0.2, 0.5, 0.1, 0.4, 0.8]
candy_calories = [25, 12, 22, 14, 33]
solve_candy_knapsack(5, candy_number_limits, candy_prices, candy_calories, 12, 250, 500)