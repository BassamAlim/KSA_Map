import itertools
import json
import queue
from enum import Enum

import geopy.distance

import models


class Algorithms(Enum):
    BFS = 'Breadth First Search'
    UCS = 'Uniform Cost Search'
    IDS = 'Iterative Deepening Search'
    Greedy = 'Greedy'
    A_Star = 'A*'


with open('Cities.json', encoding='utf-8') as file:
    cities = json.load(file)


def make_node(cid, path_cost, parent, depth=0):
    return models.Node(cid, path_cost, parent, depth)


def goal_test(destination, cid):
    if cid == destination:
        return True
    return False


def bfs(start_city, destination_city):
    start_node = make_node(start_city, 0, None)
    fringe = queue.Queue()
    visited = []
    output = models.Output()
    fringe.put(start_node)
    visited.append(start_city)
    while True:
        if fringe.empty():
            return pack_output(None, output)
        node = remove_first(fringe, Algorithms.BFS)
        if goal_test(destination_city, node.cid):
            return pack_output(node, output)
        expand(node, fringe, visited, output, Algorithms.BFS)


def ucs(start_city, destination_city):
    fringe = queue.PriorityQueue()
    visited = []
    output = models.Output()
    fringe.put((0, 0, make_node(start_city, 0, None)))
    visited.append(start_city)
    while True:
        if fringe.empty():
            return pack_output(None, output)
        node = remove_first(fringe, Algorithms.UCS)
        visited.append(node.cid)
        if goal_test(destination_city, node.cid):
            return pack_output(node, output)
        expand(node, fringe, visited, output, Algorithms.UCS)


def ids(start_city, destination_city):
    output = models.Output()
    start_node = make_node(start_city, 0, None, 1)
    depth = 1
    while True:
        result = dls(start_node, destination_city, output, depth)
        if result[0] != 'cutoff':
            return pack_output(result[1], result[2])
        depth += 1


def dls(start_node, destination_city, output, limit):
    cutoff = False
    fringe = []
    visited = []
    fringe.append(start_node)
    visited.append(start_node.cid)
    while True:
        if len(fringe) == 0:
            if cutoff:
                return 'cutoff', None, output
            else:
                return 'failure', None, output
        node = remove_first(fringe, Algorithms.IDS)
        if goal_test(destination_city, node.cid):
            return 'soln', node, output
        elif node.depth == limit:
            cutoff = True
        else:
            expand(node, fringe, visited, output, Algorithms.IDS)


x2 = 0.0
y2 = 0.0


def greedy(start_city, destination_city):
    global x2
    global y2
    x2 = cities[destination_city]['latitude']
    y2 = cities[destination_city]['longitude']
    fringe = queue.PriorityQueue()
    visited = []
    output = models.Output()
    fringe.put((0, 0, make_node(start_city, 0, None)))
    visited.append(start_city)
    while True:
        if fringe.empty():
            return pack_output(None, output)
        node = remove_first(fringe, Algorithms.Greedy)
        visited.append(node.cid)
        if goal_test(destination_city, node.cid):
            return pack_output(node, output)
        expand(node, fringe, visited, output, Algorithms.Greedy)


def a_star(start_city, destination_city):
    global x2
    global y2
    x2 = cities[destination_city]['latitude']
    y2 = cities[destination_city]['longitude']
    fringe = queue.PriorityQueue()
    visited = []
    output = models.Output()
    fringe.put((0, 0, make_node(start_city, 0, None)))
    visited.append(start_city)
    while True:
        if fringe.empty():
            return pack_output(None, output)
        node = remove_first(fringe, Algorithms.A_Star)
        visited.append(node.cid)
        if goal_test(destination_city, node.cid):
            return pack_output(node, output)
        expand(node, fringe, visited, output, Algorithms.A_Star)


tie_breaker = itertools.count()


def expand(node, fringe, visited, output, algo):
    for neighbor in successor_function(node, visited):
        path_cost = node.path_cost + neighbor[1]
        if algo == Algorithms.BFS:
            fringe.put(make_node(neighbor[0], path_cost, node, node.depth + 1))
            visited.append(neighbor[0])
        elif algo == Algorithms.UCS:
            fringe.put((path_cost, next(tie_breaker), make_node(neighbor[0], path_cost, node)))
        elif algo == Algorithms.IDS:
            fringe.append(make_node(neighbor[0], path_cost, node, node.depth + 1))
            visited.append(neighbor[0])
        elif algo == Algorithms.Greedy:
            h = calc_heuristic(cities[neighbor[0]]['latitude'], cities[neighbor[0]]['longitude'])
            fringe.put((h, next(tie_breaker), make_node(neighbor[0], path_cost, node)))
        elif algo == Algorithms.A_Star:
            h = calc_heuristic(cities[neighbor[0]]['latitude'], cities[neighbor[0]]['longitude'])
            fringe.put((path_cost + h, next(tie_breaker), make_node(neighbor[0], path_cost, node)))
        output.nodes_num += 1
    if algo == Algorithms.IDS:
        output.fringe_max_size = max(output.fringe_max_size, len(fringe))
    else:
        output.fringe_max_size = max(output.fringe_max_size, fringe.qsize())


def successor_function(parent, visited):
    neighbors = []
    for neighbor in cities[parent.cid]['neighbors']:
        if (parent.parent is not None and neighbor['cid'] == parent.parent.cid) or in_history(neighbor['cid'], visited):
            continue
        neighbors.append((neighbor['cid'], neighbor['distance']))
    return neighbors


def calc_heuristic(x1, y1):
    coords1 = (x1, y1)
    coords2 = (x2, y2)
    return geopy.distance.distance(coords1, coords2).km


def remove_first(fringe, algo):
    if algo == Algorithms.BFS:
        return fringe.get()
    elif algo == Algorithms.IDS:
        return fringe.pop()
    else:
        return fringe.get()[2]


def in_history(cid, visited):
    for h in visited:
        if h == cid:
            return True
    return False


def pack_output(node, output):
    if node is None:
        return 'failure', output
    else:
        output.distance = node.path_cost
        output.route = []
        calc_route(node, output)
        return 'success', output


def calc_route(node, output):
    if node is None:
        return
    calc_route(node.parent, output)
    output.route.append(node)
