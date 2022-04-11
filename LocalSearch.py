import json
import math
import time
from enum import Enum

import IGUI
import process

processor = process


class Algorithms(Enum):
    Empty = 'nothing'
    HC = 'Hill Climbing'
    SA = 'Simulated Annealing'
    GA = 'Genetic Algorithms'


algorithm = Algorithms.Empty

with open('Cities.json', encoding='utf-8') as file:
    data = json.load(file)


def hill_climbing(cities):
    global algorithm
    algorithm = Algorithms.HC
    start_time = time.time()
    while True:
        formulate_route(cities)
        current_cost = calc_cost(cities)
        result = find_best_swap(cities, current_cost, 0)
        if result == -1:
            break
        else:
            swap(cities, result)
            print('swap: ' + str(current_cost - calc_cost(cities)))
    print('Time: ' + str(time.time() - start_time))
    return cities


def simulated_annealing(cities):
    global algorithm
    algorithm = Algorithms.SA
    start_time = time.time()
    iterations = 0
    best_sol = list(cities)
    best_sol_cost = calc_cost(cities)
    while True:
        tmp = schedule(iterations)
        iterations += 1
        formulate_route(cities)
        current_cost = calc_cost(cities)
        result = find_best_swap(cities, current_cost, tmp)
        if result == -1 or tmp == 1:
            break
        else:
            swap(cities, result)
            new_cost = calc_cost(cities)
            print('swap: ' + str(current_cost - new_cost))
            if new_cost < best_sol_cost:
                best_sol = list(cities)
                best_sol_cost = new_cost
    print('Time: ' + str(time.time() - start_time))
    return best_sol


def genetic(cities):
    global algorithm
    algorithm = Algorithms.GA


def find_best_swap(ls, current_cost, tmp=0):
    best_swap = -1
    best_cost = current_cost
    for i in range(0, len(ls) - 1):  # range: upper is exclusive
        swapped = list(ls)
        swap(swapped, i)
        new_cost = calc_cost(swapped)
        print('current cost: ' + str(current_cost) + ', new cost: ' + str(new_cost))
        diff = best_cost - new_cost
        if algorithm == Algorithms.HC:
            if diff > 0:
                best_swap = i
                best_cost = new_cost
        elif algorithm == Algorithms.SA:
            prob = math.exp(diff/tmp)
            print('E ' + str(prob))
            if diff > 0 or prob > 0.3:
                best_swap = i
                best_cost = new_cost
    return best_swap


def calc_cost(route):
    cost = 0
    for i in range(0, len(route) - 1):
        a_star_solution = processor.a_star(route[i], route[i + 1])[1]
        cost += a_star_solution.distance
    return cost


def swap(ls, i1):
    i2 = i1 + 1
    ls[i1], ls[i2] = ls[i2], ls[i1]  # swap


def schedule(t):
    return 30 - t


def formulate_route(route):
    string = str()
    for element in route:
        string += data[element]['name'] + ' ← '
    print(string[:-3])


r = [53, 93, 28, 149, 0, 85, 49]
#IGUI.visualize(r)
sol = simulated_annealing(r)
print('Best Cost: ' + str(calc_cost(sol)))
IGUI.visualize(sol)
