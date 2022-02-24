import itertools
import json
import queue
from enum import Enum
import models


class Algorithms(Enum):
    BFS = 'BFS'
    UCS = 'UCS'
    IDS = 'IDS'


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
        if goal_test(destination_city, node.cid):
            return pack_output(node, output)
        expand(node, fringe, visited, output, Algorithms.UCS)


def ids(start_city, destination_city):
    start_node = make_node(start_city, 0, None)
    output = models.Output()
    depth = 0
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


tie_breaker = itertools.count()


def expand(node, fringe, visited, output, algo):
    for neighbor in successor_function(node.cid, visited):
        path_cost = node.path_cost + neighbor[1]
        if algo == Algorithms.BFS:
            fringe.put(make_node(neighbor[0], path_cost, node, node.depth+1))
        elif algo == Algorithms.UCS:
            fringe.put((path_cost, next(tie_breaker), make_node(neighbor[0], path_cost, node)))
        else:
            fringe.append(make_node(neighbor[0], path_cost, node, node.depth+1))
        visited.append(neighbor[0])
        output.nodes_num += 1
    if algo == Algorithms.IDS:
        output.fringe_max_size = max(output.fringe_max_size, len(fringe))
    else:
        output.fringe_max_size = max(output.fringe_max_size, fringe.qsize())


def successor_function(cid, visited):
    neighbors = []
    for neighbor in cities[cid]['neighbors']:
        if not in_history(neighbor['cid'], visited):
            neighbors.append((neighbor['cid'], neighbor['distance']))
    return neighbors


def remove_first(fringe, algo):
    if algo == Algorithms.BFS:
        return fringe.get()
    elif algo == Algorithms.UCS:
        return fringe.get()[2]
    else:
        return fringe.pop()


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
