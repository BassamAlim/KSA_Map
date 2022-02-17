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


def return_result(node, result, algo):
    if node is None:
        print('Failure')
    else:
        if algo == Algorithms.BFS:
            print('//////////   BFS   //////////')
        elif algo == Algorithms.UCS:
            print('//////////   UCS   //////////')
        else:
            print('//////////   IDS   //////////')
        print('Route:')
        result.distance = node.path_cost
        calc_and_display_route(node, result)
        print('Fringe Max Size: ' + str(result.fringe_max_size))
        print('Number Of Nodes: ' + str(result.nodes_num))
        print('Distance: ' + str(result.distance) + " km")


def calc_and_display_route(node, result):
    if node is None:
        return
    calc_and_display_route(node.parent, result)
    result.route.append(node)
    print('CID: ' + str(node.cid) + ', Name: ' + node.name + ', Path Cost: ' + str(node.path_cost))


def make_node(cid, path_cost, parent):
    return models.Node(cid, cities[cid]['name'], path_cost, parent)


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


tie_breaker = itertools.count()


def expand(node, fringe, visited, result, algo):
    counter = -1
    for neighbor_cid in successor_function(node.cid):
        counter += 1
        if in_history(neighbor_cid, visited) or (node.parent is not None and node.parent == neighbor_cid):
            continue
        path_cost = node.path_cost + cities[node.cid]['neighbors'][counter]['distance']
        if algo == Algorithms.BFS:
            fringe.put(make_node(neighbor_cid, path_cost, node))
        elif algo == Algorithms.UCS:
            new_node = make_node(neighbor_cid, path_cost, node)
            count = next(tie_breaker)
            fringe.put((path_cost, count, new_node))
        else:
            pass
        result.nodes_num += 1
    result.fringe_max_size = max(result.fringe_max_size, fringe.qsize())


class Process:
    start = -1
    destination = -1

    def __init__(self, start_city, end_city):
        self.start = start_city
        self.destination = end_city
        start_node = make_node(start_city, 0, None)
        self.bfs(start_node)
        self.ucs(start_node)
        # self.ids(start_node)

    def bfs(self, node):
        result = models.Result
        fringe = queue.Queue()
        visited = []
        fringe.put(node)
        result.nodes_num += 1
        while True:
            if fringe.empty():
                return_result(None, result, Algorithms.BFS)
                break
            new_node = fringe.get()  # RemoveFirst
            if self.goal_test(new_node.cid):
                return_result(new_node, result, Algorithms.BFS)
                break
            visited.append(new_node.cid)
            expand(new_node, fringe, visited, result, Algorithms.BFS)

    def ucs(self, node):
        result = models.Result
        fringe = queue.PriorityQueue()
        visited = []
        fringe.put((0, 0, node))
        result.nodes_num += 1
        while True:
            if fringe.empty():
                return_result(None, result, Algorithms.UCS)
                break
            new_node = fringe.get()[2]  # RemoveFirst
            if self.goal_test(new_node.cid):
                return_result(new_node, result, Algorithms.UCS)
                break
            visited.append(new_node.cid)
            expand(new_node, fringe, visited, result, Algorithms.UCS)

    def ids(self, node):
        result = models.Result
        fringe = queue.Queue()
        visited = []
        fringe.put(node)
        """""
        while True:
            if fringe.empty():
                return_result(None, result, Algorithms.BFS)
                break
            new_node = fringe.get()  # RemoveFirst
            result.nodes_num += 1
            if self.goal_test(new_node.cid):
                return_result(new_node, result, Algorithms.BFS)
                break
            visited.append(new_node.cid)
            insert_all(expand(new_node, visited, Algorithms.BFS), fringe, result)
            """""

    def goal_test(self, cid):
        if cid == self.destination:
            return True
        return False
