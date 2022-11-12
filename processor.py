import itertools
import json
import math
import time

import geopy.distance
import numpy as np  # A library that provides fast and efficient methods for arrays, random, ...

from Algorithms import Algorithms
from Fringe import Fringe
from models import Chromosome, Node, Output


algorithm = Algorithms.Empty

tie_breaker = itertools.count()

x2 = 0.0
y2 = 0.0

with open('Cities.json', encoding='utf-8') as file:
    data = json.load(file)
with open('table.json', encoding='utf-8') as file:
    table = json.load(file)


def bfs(cities, visualize, stop):
    global algorithm
    algorithm = Algorithms.BFS
    start_time = time.time()
    start_node = Node(cities[0], 0)
    fringe = Fringe(algorithm)
    visited = []
    output = Output()
    fringe.put(start_node)
    visited.append(cities[0])
    while not fringe.empty():
        if stop():
            return finish(None, 0, 0)

        node = fringe.remove_first()
        current = list(node.predecessors)
        current.append(node.cid)
        visualize(current, node.path_cost, len(visited) / len(data) * 100)

        if goal_test(cities[1], node.cid):
            output.distance = node.path_cost
            node.predecessors.append(node.cid)
            output.route = node.predecessors
            output.run_time = time.time() - start_time
            return output
        expand(node, fringe, visited, output)


def ucs(cities, visualize, stop):
    global algorithm
    algorithm = Algorithms.UCS
    start_time = time.time()
    fringe = Fringe(algorithm)
    visited = []
    output = Output()
    fringe.put((0, 0, Node(cities[0], 0)))
    visited.append((cities[0], 0))
    while not fringe.empty():
        if stop():
            return finish(None, 0, 0)

        node = fringe.remove_first()
        current = list(node.predecessors)
        current.append(node.cid)
        visualize(current, node.path_cost, len(visited) / len(data) * 100)

        if goal_test(cities[1], node.cid):
            output.distance = node.path_cost
            node.predecessors.append(node.cid)
            output.route = node.predecessors
            output.run_time = time.time() - start_time
            return output
        expand(node, fringe, visited, output)


def ids(cities, visualize, stop):
    global algorithm
    algorithm = Algorithms.IDS
    start_time = time.time()
    output = Output()
    start_node = Node(cities[0], 0, depth=1)
    depth = 1
    while True:
        result = dls(start_node, cities[1], output, depth, visualize, stop)
        if result is not None:
            output.distance = result.path_cost
            result.predecessors.append(result.cid)
            output.route = result.predecessors
            output.run_time = time.time() - start_time
            return output
        depth += 1


def greedy(cities, visualize, stop):
    global x2, y2, algorithm
    algorithm = Algorithms.Greedy
    start_time = time.time()
    x2 = data[cities[1]]['x']
    y2 = data[cities[1]]['y']
    fringe = Fringe(algorithm)
    visited = []
    output = Output()
    fringe.put((0, 0, Node(cities[0], 0)))
    visited.append(cities[0])
    while not fringe.empty():
        if stop():
            return finish(None, 0, 0)

        node = fringe.remove_first()
        visited.append(node.cid)
        current = list(node.predecessors)
        current.append(node.cid)
        visualize(current, node.path_cost, len(visited) / len(data) * 100)

        if goal_test(cities[1], node.cid):
            output.distance = node.path_cost
            node.predecessors.append(node.cid)
            output.route = node.predecessors
            output.run_time = time.time() - start_time
            return output
        expand(node, fringe, visited, output)


def a_star(cities, visualize, stop):
    global x2, y2, algorithm
    algorithm = Algorithms.A_Star
    start_time = time.time()
    x2 = data[cities[1]]['x']
    y2 = data[cities[1]]['y']
    fringe = Fringe(algorithm)
    visited = []
    output = Output()
    fringe.put((0, 0, Node(cities[0], 0)))
    visited.append((cities[0], 0))
    while not fringe.empty():
        if stop():
            return finish(None, 0, 0)

        node = fringe.remove_first()
        current = list(node.predecessors)
        current.append(node.cid)
        visualize(current, node.path_cost, len(visited) / len(data) * 100)

        if goal_test(cities[1], node.cid):
            output.distance = node.path_cost
            node.predecessors.append(node.cid)
            output.route = node.predecessors
            output.run_time = time.time() - start_time
            return output
        expand(node, fringe, visited, output)


def hill_climbing(cities, visualize, stop):
    global algorithm
    algorithm = Algorithms.HC
    start_time = time.time()

    np.random.shuffle(cities)
    current_cost = get_fitness(cities)

    PERSISTENCE = pow(len(cities), 2)
    no_change = 0
    i = 0
    while i < PERSISTENCE and no_change < PERSISTENCE:
        old_cost = current_cost

        tries = 0
        while tries < PERSISTENCE:
            if stop():
                return finish(cities, current_cost, start_time)
            swap = find_swap(len(cities))
            swapped = list(cities)
            swapped[swap[0]], swapped[swap[1]] = swapped[swap[1]], swapped[swap[0]]  # swap
            new_cost = get_fitness(swapped)
            if new_cost < current_cost:
                cities = swapped
                current_cost = new_cost
                break
            tries += 1

        perc = i / PERSISTENCE * 100
        if current_cost == old_cost:
            no_change += 1
            visualize(None, current_cost, perc)
        else:
            no_change = 0
            visualize(cities, current_cost, perc)

        i += 1

    return finish(cities, current_cost, start_time)


def simulated_annealing(cities, visualize, stop):
    global algorithm
    algorithm = Algorithms.SA
    start_time = time.time()

    np.random.shuffle(cities)
    current_cost = get_fitness(cities)
    best_sol = list(cities)
    best_sol_cost = current_cost

    PERSISTENCE = pow(len(cities), 2)
    temperature = pow(len(cities), 2)
    no_change = 0
    i = 0
    while i < PERSISTENCE and no_change < PERSISTENCE:
        old_cost = current_cost
        tries = 0
        while tries < PERSISTENCE:
            if stop():
                return finish(best_sol, best_sol_cost, start_time)

            ss = find_swap(len(cities))
            swapped = list(cities)
            swapped[ss[0]], swapped[ss[1]] = swapped[ss[1]], swapped[ss[0]]  # swap
            new_cost = get_fitness(swapped)
            if current_cost - new_cost > 0 or np.random.random() < get_prob(current_cost, new_cost, temperature):
                cities = swapped
                current_cost = new_cost
                break
            tries += 1

        if current_cost < best_sol_cost:
            best_sol = cities
            best_sol_cost = current_cost

        perc = i / PERSISTENCE * 100
        if current_cost == old_cost:
            no_change += 1
            visualize(None, current_cost, perc)
        else:
            no_change = 0
            visualize(cities, current_cost, perc)

        temperature = cooldown(temperature)
        i += 1

    return finish(best_sol, best_sol_cost, start_time)


def genetic(cities, visualize, stop):
    global algorithm
    algorithm = Algorithms.GA
    start_time = time.time()
    solution = Chromosome(list(cities), get_fitness(cities))

    GENERATIONS = pow(len(cities), 2)
    POP_SIZE = len(cities)
    temperature = pow(len(cities), 2)

    population = populate(cities, POP_SIZE)

    no_change = 0
    gen = 1
    while gen <= GENERATIONS and no_change < int(GENERATIONS / pow(gen, 1/3)):
        if stop():
            return finish(solution.gnome, solution.fitness, start_time)

        population = selection(cities, population, POP_SIZE, temperature)
        minimum = min(population)
        if minimum.fitness < solution.fitness:
            solution = minimum
            no_change = 0
        else:
            no_change += 1

        visualize(minimum.gnome, minimum.fitness, perc=gen / GENERATIONS * 100)

        temperature = cooldown(temperature)
        gen += 1

    return finish(solution.gnome, solution.fitness, start_time)


def dls(start_node, destination_city, output, limit, visualize, stop):
    fringe = Fringe(algorithm)
    visited = []
    fringe.put(start_node)
    visited.append(start_node.cid)
    while not fringe.empty():
        if stop():
            finish(None, 0, 0)

        node = fringe.remove_first()
        current = list(node.predecessors)
        current.append(node.cid)
        visualize(current, node.path_cost, len(visited) / len(data) * 100)

        if goal_test(destination_city, node.cid):
            return node
        elif node.depth != limit:
            expand(node, fringe, visited, output)

    return None


def expand(node, fringe, visited, output):
    for neighbor in successor_function(node, visited):
        path_cost = node.path_cost + neighbor[1]
        current = list(node.predecessors)
        current.append(node.cid)

        match algorithm:
            case Algorithms.BFS | Algorithms.IDS:
                fringe.put(Node(neighbor[0], path_cost, current, node.depth + 1))
                visited.append(neighbor[0])
            case Algorithms.UCS:
                fringe.put((path_cost, next(tie_breaker), Node(neighbor[0], path_cost, current, node.depth + 1)))
                visited.append((neighbor[0], path_cost))
            case Algorithms.Greedy:
                h = calc_heuristic(data[neighbor[0]]['x'], data[neighbor[0]]['y'])
                fringe.put((h, next(tie_breaker), Node(neighbor[0], path_cost, current, node.depth + 1)))
            case Algorithms.A_Star:
                h = calc_heuristic(data[neighbor[0]]['x'], data[neighbor[0]]['y'])
                fringe.put((path_cost + h, next(tie_breaker), Node(neighbor[0], path_cost, current, node.depth + 1)))
                visited.append((neighbor[0], path_cost))

        output.nodes_num += 1
        output.fringe_max_size = max(output.fringe_max_size, fringe.size())


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
        r1 = np.random.randint(0, length - 1)
        r2 = np.random.randint(0, length - 1)
        if r1 != r2:
            return r1, r2


def goal_test(destination, cid):
    if cid == destination:
        return True
    return False


def get_prob(old, new, tmp):
    return math.exp(-abs(new - old) / tmp)


def cooldown(temp):
    return temp * 0.995


def mutate(gnome):
    gnome = list(gnome)
    swap = find_swap(len(gnome))
    gnome[swap[0]], gnome[swap[1]] = gnome[swap[1]], gnome[swap[0]]
    return gnome


def get_fitness(route):
    cost = 0
    for i in range(0, len(route) - 1):
        cost += table[route[i]][route[i + 1]]
    cost += table[route[len(route) - 1]][route[0]]  # To return to the start city
    return cost


def populate(cities, pop_size):
    population = []
    # Populating the GNOME pool.
    for i in range(pop_size):
        gnome = list(cities)
        np.random.shuffle(gnome)
        population.append(Chromosome(gnome, get_fitness(gnome)))
    return population


def selection(cities, population, pop_size, temperature):
    new_population = []
    for i in range(pop_size):
        tries = 0
        while True:
            new_g = mutate(population[i].gnome)
            new_gnome = Chromosome(new_g, get_fitness(new_g))
            if new_gnome.fitness <= population[i].fitness:
                new_population.append(new_gnome)
                break
            else:
                prob = get_prob(population[i].fitness, new_gnome.fitness, temperature)
                if prob > 0.5 or tries == pow(len(cities), 2):
                    new_population.append(new_gnome)
                    break
                tries += 1
    return new_population


def finish(cities, cost, start_time):
    if cities is not None:
        cities.append(cities[0])  # To return to start city
    return Output(cities, cost, time.time() - start_time)
