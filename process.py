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
    return models.Node(cid, cities[cid]['name'], path_cost, parent, depth)


def goal_test(destination, cid):
    if cid == destination:
        return True
    return False


def bfs(start_city, destination_city):
    start_node = make_node(start_city, 0, None)
    fringe = queue.Queue()
    visited = []
    output = models.Output
    fringe.put(start_node)
    while True:
        if fringe.empty():
            return pack_output(None, output)
        new_node = fringe.get()  # RemoveFirst
        if goal_test(destination_city, new_node.cid):
            return pack_output(new_node, output)
        visited.append(new_node.cid)
        expand(new_node, fringe, visited, output, Algorithms.BFS)


def ucs(start_city, destination_city):
    start_node = make_node(start_city, 0, None)
    fringe = queue.PriorityQueue()
    visited = []
    output = models.Output
    fringe.put((0, 0, start_node))
    while True:
        if fringe.empty():
            return pack_output(None, output)
        new_node = fringe.get()[2]  # RemoveFirst
        if goal_test(destination_city, new_node.cid):
            return pack_output(new_node, output)
        visited.append(new_node.cid)
        expand(new_node, fringe, visited, output, Algorithms.UCS)


def ids(start_city, destination_city):
    start_node = make_node(start_city, 0, None)
    output = models.Output
    depth = 0
    while True:
        result = dls(start_node, destination_city, output, depth)
        if result[0] != 'cutoff':
            return pack_output(result[1], result[2])
        depth += 1


def dls(start_node, destination_city, output, limit):
    fringe = []
    visited = []
    fringe.append(start_node)
    cutoff = False
    while True:
        if len(fringe) == 0:
            if cutoff:
                return 'cutoff', None, output
            else:
                return 'failure', None, output
        current_node = fringe.pop()
        visited.append(current_node.cid)
        if goal_test(destination_city, current_node.cid):
            return 'soln', current_node, output
        elif current_node.depth == limit:
            cutoff = True
        else:
            expand(current_node, fringe, visited, output, Algorithms.IDS)


tie_breaker = itertools.count()


def expand(node, fringe, visited, output, algo):
    counter = -1
    for neighbor_cid in successor_function(node.cid):
        counter += 1
        if in_history(neighbor_cid, visited) or (node.parent is not None and node.parent == neighbor_cid):
            continue
        path_cost = node.path_cost + cities[node.cid]['neighbors'][counter]['distance']
        if algo == Algorithms.BFS:
            fringe.put(make_node(neighbor_cid, path_cost, node, node.depth + 1))
        elif algo == Algorithms.UCS:
            new_node = make_node(neighbor_cid, path_cost, node)
            fringe.put((path_cost, next(tie_breaker), new_node))
        else:
            fringe.append(make_node(neighbor_cid, path_cost, node, node.depth + 1))
        output.nodes_num += 1
    if algo == Algorithms.IDS:
        output.fringe_max_size = max(output.fringe_max_size, len(fringe))
    else:
        output.fringe_max_size = max(output.fringe_max_size, fringe.qsize())


def successor_function(cid):
    neighbors = []
    for neighbor in cities[cid]['neighbors']:
        neighbors.append(neighbor['cid'])
    return neighbors


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
        calc_route(node, output)
        return 'success', output


def calc_route(node, output):
    if node is None:
        return
    calc_route(node.parent, output)
    output.route.append(node)


"""
class Process:

    def old_dls(self, node, output, limit):
        fringe = queue.Queue()
        visited = []
        fringe.put(node)
        output.nodes_num += 1
        return self.rec_dls(node, fringe, visited, output, limit)

    def rec_dls(self, node, fringe, visited, output, limit):
        cutoff_occurred = False
        if goal_test(node.cid):
            return 'soln', node, output
        elif node.depth == limit:
            return 'cutoff', node, output
        else:
            expand(node, fringe, visited, output, Algorithms.IDS)
            while not fringe.empty():
                successor = fringe.get()  # RemoveFirst
                visited.append(successor.cid)
                result = self.rec_dls(successor, fringe, visited, output, limit)
                if result[0] == 'cutoff':
                    cutoff_occurred = True
                elif result[0] == 'soln':
                    return result
        if cutoff_occurred:
            return 'cutoff', node, output
        else:
            return 'failure', node, output
"""
