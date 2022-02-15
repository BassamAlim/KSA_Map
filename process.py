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
        calc_and_display_route(node, result)
        print('Fringe Max Size: ' + str(result.fringe_max_size))
        print('Number Of Nodes: ' + str(result.nodes_num))
        print('Distance: ' + str(result.distance) + " km")


def calc_and_display_route(node, result):
    if node is None:
        return
    calc_and_display_route(node.parent, result)
    result.route.append(node)
    result.distance += node.path_cost
    print("CID: " + str(node.cid) + ", Name: " + node.name)


def make_node(cid, parent, path_cost):
    return models.Node(cid, cities[cid]['name'], parent, path_cost)


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


def insert_all(neighbors, fringe, result):
    for neighbor in neighbors:
        fringe.put_nowait(neighbor)
    result.fringe_max_size = max(result.fringe_max_size, fringe.qsize())


def expand(node, visited, algo):
    successors = []
    neighbors = successor_function(node.cid)
    counter = -1
    for neighbor_cid in neighbors:
        counter += 1
        if in_history(neighbor_cid, visited) or (node.parent is not None and node.parent == neighbor_cid):

            continue
        successors.append(make_node(neighbor_cid, node, cities[node.cid]['neighbors'][counter]['distance']))
    return successors


class Process:
    cities = []
    start = -1
    destination = -1

    def __init__(self, start_city, end_city):
        self.start = start_city
        self.destination = end_city
        start_node = make_node(start_city, None, 0)
        self.bfs(start_node)
        #self.ucs(start_node)
        #self.ids(start_node)

    def bfs(self, node):
        result = models.Result
        fringe = queue.Queue()
        visited = []
        fringe.put_nowait(node)
        while True:
            if fringe.empty():
                return_result(None, result, Algorithms.BFS)
                break
            new_node = fringe.get_nowait()  # RemoveFirst
            result.nodes_num += 1
            if self.goal_test(new_node.cid):
                return_result(new_node, result, Algorithms.BFS)
                break
            visited.append(new_node.cid)
            insert_all(expand(new_node, visited, Algorithms.BFS), fringe, result)

    def ucs(self, node):
        result = models.Result
        fringe = queue.PriorityQueue
        visited = []
        fringe.put_nowait(node, 0)
        """""
        while True:
            if fringe.empty():
                return_result(None, result, Algorithms.BFS)
                break
            new_node = fringe.get_nowait()  # RemoveFirst
            result.nodes_num += 1
            if self.goal_test(new_node.cid):
                return_result(new_node, result, Algorithms.BFS)
                break
            visited.append(new_node.cid)
            insert_all(expand(new_node, visited, Algorithms.BFS), fringe, result)
            """""

    def ids(self, node):
        result = models.Result
        fringe = queue.Queue()
        visited = []
        fringe.put_nowait(node)
        """""
        while True:
            if fringe.empty():
                return_result(None, result, Algorithms.BFS)
                break
            new_node = fringe.get_nowait()  # RemoveFirst
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
