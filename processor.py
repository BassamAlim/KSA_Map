import itertools
import json
import math
import queue
import random
import time

import geopy.distance

from models import Node
from models import Output
from models import Chromosome
from Algorithms import Algorithms


algorithm = Algorithms.Empty

tie_breaker = itertools.count()

x2 = 0.0
y2 = 0.0

with open('Cities.json', encoding='utf-8') as file:
    data = json.load(file)
with open('table.json', encoding='utf-8') as file:
    table = json.load(file)


def bfs(cities, visualize):
    global algorithm
    algorithm = Algorithms.BFS
    start_time = time.time()
    start_node = Node(cities[0], 0)
    fringe = queue.Queue()
    visited = []
    output = Output()
    fringe.put(start_node)
    visited.append(cities[0])
    while not fringe.empty():
        node = remove_first(fringe)
        current = list(node.predecessors)
        current.append(node.cid)
        visualize('Current:', current, node.path_cost, 0)

        if goal_test(cities[1], node.cid):
            output.distance = node.path_cost
            node.predecessors.append(node.cid)
            output.route = node.predecessors
            output.run_time = time.time() - start_time
            return output
        expand(node, fringe, visited, output)


def ucs(cities, visualize):
    global algorithm
    algorithm = Algorithms.UCS
    start_time = time.time()
    fringe = queue.PriorityQueue()
    visited = []
    output = Output()
    fringe.put((0, 0, Node(cities[0], 0)))
    visited.append((cities[0], 0))
    while not fringe.empty():
        node = remove_first(fringe)
        current = list(node.predecessors)
        current.append(node.cid)
        visualize('Current:', current, node.path_cost, 0)

        if goal_test(cities[1], node.cid):
            output.distance = node.path_cost
            node.predecessors.append(node.cid)
            output.route = node.predecessors
            output.run_time = time.time() - start_time
            return output
        expand(node, fringe, visited, output)


def ids(cities, visualize):
    global algorithm
    algorithm = Algorithms.IDS
    start_time = time.time()
    output = Output()
    start_node = Node(cities[0], 0, depth=1)
    depth = 1
    while True:
        result = dls(start_node, cities[1], output, depth, visualize)
        if result[0] != 'cutoff':
            output.distance = result[1].path_cost
            result[1].predecessors.append(result[1].cid)
            output.route = result[1].predecessors
            output.run_time = time.time() - start_time
            return output
        depth += 1


def greedy(cities, visualize):
    global x2, y2, algorithm
    algorithm = Algorithms.Greedy
    start_time = time.time()
    x2 = data[cities[1]]['x']
    y2 = data[cities[1]]['y']
    fringe = queue.PriorityQueue()
    visited = []
    output = Output()
    fringe.put((0, 0, Node(cities[0], 0)))
    visited.append(cities[0])
    while not fringe.empty():
        node = remove_first(fringe)
        visited.append(node.cid)
        current = list(node.predecessors)
        current.append(node.cid)
        visualize('Current:', current, node.path_cost, 0)

        if goal_test(cities[1], node.cid):
            output.distance = node.path_cost
            node.predecessors.append(node.cid)
            output.route = node.predecessors
            output.run_time = time.time() - start_time
            return output
        expand(node, fringe, visited, output)


def a_star(cities, visualize):
    global x2, y2, algorithm
    algorithm = Algorithms.A_Star
    start_time = time.time()
    x2 = data[cities[1]]['x']
    y2 = data[cities[1]]['y']
    fringe = queue.PriorityQueue()
    visited = []
    output = Output()
    fringe.put((0, 0, Node(cities[0], 0)))
    visited.append((cities[0], 0))
    while not fringe.empty():
        node = remove_first(fringe)
        current = list(node.predecessors)
        current.append(node.cid)
        visualize('Current:', current, node.path_cost, 0)

        if goal_test(cities[1], node.cid):
            output.distance = node.path_cost
            node.predecessors.append(node.cid)
            output.route = node.predecessors
            output.run_time = time.time() - start_time
            return output
        expand(node, fringe, visited, output)


def hill_climbing(cities, visualize):
    global algorithm
    algorithm = Algorithms.HC
    start_time = time.time()

    random.shuffle(cities)
    current_cost = calc_cost(cities)

    PERSISTENCE = pow(len(cities), 2)
    no_change = 0
    i = 0
    while i < PERSISTENCE and no_change < PERSISTENCE:
        old_cost = current_cost

        tries = 0
        while tries < PERSISTENCE:
            swap = find_swap(len(cities))
            swapped = list(cities)
            swapped[swap[0]], swapped[swap[1]] = swapped[swap[1]], swapped[swap[0]]  # swap
            new_cost = calc_cost(swapped)
            if new_cost < current_cost:
                cities = swapped
                current_cost = new_cost
                break
            tries += 1

        if current_cost == old_cost:
            no_change += 1
        else:
            no_change = 0
            perc = i / PERSISTENCE * 100
            visualize('Current:', cities, current_cost, perc)

        i += 1

    cities.append(cities[0])  # To return to start city
    return Output(cities, current_cost, time.time() - start_time)


def simulated_annealing(cities, visualize):
    global algorithm
    algorithm = Algorithms.SA
    start_time = time.time()

    random.shuffle(cities)
    current_cost = calc_cost(cities)
    best_sol = list(cities)
    best_sol_cost = current_cost

    PERSISTENCE = pow(len(cities), 2)
    temperature = pow(len(cities), 2)
    no_change = 0
    i = 0
    while i < PERSISTENCE and no_change < PERSISTENCE:
        old_cost = current_cost
        tries = 0
        while tries < len(cities):
            ss = find_swap(len(cities))
            swapped = list(cities)
            swapped[ss[0]], swapped[ss[1]] = swapped[ss[1]], swapped[ss[0]]  # swap
            new_cost = calc_cost(swapped)
            if current_cost - new_cost > 0 or random.random() < get_prob(current_cost, new_cost, temperature):
                cities = swapped
                current_cost = new_cost
                break
            tries += 1

        if current_cost < best_sol_cost:
            best_sol = cities
            best_sol_cost = current_cost

        if current_cost <= old_cost:
            no_change += 1
        else:
            no_change = 0
            perc = i / PERSISTENCE * 100
            visualize('Current:', cities, current_cost, perc)

        temperature = cooldown(temperature)
        i += 1

    best_sol.append(best_sol[0])
    return Output(best_sol, best_sol_cost, time.time() - start_time)


def genetic(cities, visualize):
    global algorithm
    algorithm = Algorithms.GA
    start_time = time.time()
    solution = list(cities)
    sol_cost = calc_cost(cities)

    GENERATIONS = pow(len(cities), 2)
    POP_SIZE = 10
    gen = 1

    population = []
    # Populating the GNOME pool.
    for i in range(POP_SIZE):
        gnome = list(cities)
        random.shuffle(cities)
        population.append(Chromosome(gnome, calc_cost(gnome)))

    temperature = pow(len(cities), 2)
    while temperature > 30 and gen <= GENERATIONS:
        population.sort()
        display_gen(gen, population)
        solution, sol_cost = get_best(solution, sol_cost, population)  # Python Stuff
        perc = gen / GENERATIONS * 100
        visualize('Current:', population[0].gnome, population[0].fitness, perc)

        new_population = []
        for i in range(POP_SIZE):
            tries = 0
            while True:
                new_g = mutate(population[i].gnome)
                new_gnome = Chromosome(new_g, calc_cost(new_g))
                if new_gnome.fitness <= population[i].fitness:
                    new_population.append(new_gnome)
                    break
                else:
                    prob = get_prob(population[i].fitness, new_gnome.fitness, temperature)
                    if prob > 0.5 or tries == pow(len(cities), 2):
                        new_population.append(new_gnome)
                        break
                    tries += 1

        temperature = cooldown(temperature)
        population = new_population
        gen += 1

    solution, sol_cost = get_best(solution, sol_cost, population)
    display_gen(gen, population)
    solution.append(solution[0])
    return Output(solution, sol_cost, time.time() - start_time)


def dls(start_node, destination_city, output, limit, visualize):
    cutoff = False
    fringe = []
    visited = []
    fringe.append(start_node)
    visited.append(start_node.cid)
    while len(fringe) != 0:
        node = remove_first(fringe)
        current = list(node.predecessors)
        current.append(node.cid)
        visualize('Current:', current, node.path_cost)

        if goal_test(destination_city, node.cid):
            return 'soln', node
        elif node.depth == limit:
            cutoff = True
        else:
            expand(node, fringe, visited, output)

    if cutoff:
        return 'cutoff', None
    else:
        return 'failure', None


def expand(node, fringe, visited, output):
    for neighbor in successor_function(node, visited):
        path_cost = node.path_cost + neighbor[1]
        current = list(node.predecessors)
        current.append(node.cid)

        if algorithm == Algorithms.BFS:
            fringe.put(Node(neighbor[0], path_cost, current, node.depth + 1))
            visited.append(neighbor[0])

        elif algorithm == Algorithms.UCS:
            fringe.put((path_cost, next(tie_breaker), Node(neighbor[0], path_cost, current, node.depth + 1)))
            visited.append((neighbor[0], path_cost))

        elif algorithm == Algorithms.IDS:
            fringe.append(Node(neighbor[0], path_cost, current, node.depth + 1))
            visited.append(neighbor[0])

        elif algorithm == Algorithms.Greedy:
            h = calc_heuristic(data[neighbor[0]]['x'], data[neighbor[0]]['y'])
            fringe.put((h, next(tie_breaker), Node(neighbor[0], path_cost, current, node.depth + 1)))

        elif algorithm == Algorithms.A_Star:
            h = calc_heuristic(data[neighbor[0]]['x'], data[neighbor[0]]['y'])
            fringe.put((path_cost + h, next(tie_breaker), Node(neighbor[0], path_cost, current, node.depth + 1)))
            visited.append((neighbor[0], path_cost))

        output.nodes_num += 1
    if algorithm == Algorithms.IDS:
        output.fringe_max_size = max(output.fringe_max_size, len(fringe))
    else:
        output.fringe_max_size = max(output.fringe_max_size, fringe.qsize())


def successor_function(parent, visited):
    neighbors = []
    for neighbor in data[parent.cid]['neighbors']:
        cost = parent.path_cost + neighbor['distance']
        if algorithm == Algorithms.A_Star or algorithm == Algorithms.UCS:
            if not in_history(neighbor['cid'], visited, cost):
                neighbors.append((neighbor['cid'], neighbor['distance']))
        elif not in_history(neighbor['cid'], visited, cost):
            neighbors.append((neighbor['cid'], neighbor['distance']))
    return neighbors


def calc_heuristic(x1, y1):
    return geopy.distance.distance((x1, y1), (x2, y2)).km


def remove_first(fringe):
    if algorithm == Algorithms.BFS:
        return fringe.get()
    elif algorithm == Algorithms.IDS:
        return fringe.pop()
    else:
        return fringe.get()[2]


def in_history(cid, visited, cost):
    counter = 0
    for city in visited:
        if algorithm == Algorithms.A_Star or algorithm == Algorithms.UCS:
            if city[0] == cid:
                if cost > city[1]:
                    return True
                else:
                    visited.pop(counter)
        else:
            if city == cid:
                return True
        counter += 1
    return False


def find_swap(length):
    while True:
        r1 = random.randint(0, length - 1)
        r2 = random.randint(0, length - 1)
        if r1 != r2:
            return r1, r2


def goal_test(destination, cid):
    if cid == destination:
        return True
    return False


def mutate(gnome):
    gnome = list(gnome)
    while True:
        r1 = random.randint(1, len(gnome) - 1)
        r2 = random.randint(1, len(gnome) - 1)
        if r1 != r2:
            gnome[r1], gnome[r2] = gnome[r2], gnome[r1]  # swap
            break
    return gnome


def cooldown(temp):
    return temp * 0.995


def get_best(old, old_cost, pop):
    best = list(old)
    best_cost = old_cost
    for i in range(len(pop)):
        if pop[i].fitness < best_cost:
            best = pop[i].gnome
            best_cost = pop[i].fitness
    return best, best_cost


def display_gen(gen, population):
    print("Generation", gen)
    print("GNOME \t\t\t\t\t FITNESS VALUE")
    for i in range(len(population)):
        print(population[i].gnome, population[i].fitness)


def get_prob(old, new, tmp):
    return math.exp(-abs(new - old) / tmp)


def calc_cost(route):
    cost = 0
    for i in range(0, len(route) - 1):
        cost += table[route[i]][route[i + 1]]
    cost += table[route[len(route) - 1]][route[0]]  # To return to the start city
    return cost
