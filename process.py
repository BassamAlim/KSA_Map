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


def show_output(node, output, algo):
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
        output.distance = node.path_cost
        calc_and_display_route(node, output)
        print('Fringe Max Size: ' + str(output.fringe_max_size))
        print('Number Of Nodes: ' + str(output.nodes_num))
        print('Distance: ' + str(output.distance) + " km")


def calc_and_display_route(node, output):
    if node is None:
        return
    calc_and_display_route(node.parent, output)
    output.route.append(node)
    print('CID: ' + str(node.cid) + ', Name: ' + node.name + ', Path Cost: ' + str(node.path_cost))


def make_node(cid, path_cost, parent, depth=0):
    return models.Node(cid, cities[cid]['name'], path_cost, parent, depth)


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


def expand(node, fringe, visited, output, algo):
    counter = -1
    for neighbor_cid in successor_function(node.cid):
        counter += 1
        if in_history(neighbor_cid, visited) or (node.parent is not None and node.parent == neighbor_cid):
            continue
        path_cost = node.path_cost + cities[node.cid]['neighbors'][counter]['distance']
        if algo == Algorithms.UCS:
            new_node = make_node(neighbor_cid, path_cost, node)
            fringe.put((path_cost, next(tie_breaker), new_node))
        else:
            fringe.put(make_node(neighbor_cid, path_cost, node, node.depth+1))
        output.nodes_num += 1
    output.fringe_max_size = max(output.fringe_max_size, fringe.qsize())


class Process:
    start = -1
    destination = -1

    def __init__(self, start_city, end_city):
        self.start = start_city
        self.destination = end_city
        start_node = make_node(start_city, 0, None)
        self.bfs(start_node)
        self.ucs(start_node)
        self.ids(start_node)

    def bfs(self, node):
        fringe = queue.Queue()
        visited = []
        output = models.Output
        fringe.put(node)
        output.nodes_num += 1
        while True:
            if fringe.empty():
                show_output(None, output, Algorithms.BFS)
                break
            new_node = fringe.get()  # RemoveFirst
            if self.goal_test(new_node.cid):
                show_output(new_node, output, Algorithms.BFS)
                break
            visited.append(new_node.cid)
            expand(new_node, fringe, visited, output, Algorithms.BFS)

    def ucs(self, node):
        fringe = queue.PriorityQueue()
        visited = []
        output = models.Output
        fringe.put((0, 0, node))
        output.nodes_num += 1
        while True:
            if fringe.empty():
                show_output(None, output, Algorithms.UCS)
                break
            new_node = fringe.get()[2]  # RemoveFirst
            if self.goal_test(new_node.cid):
                show_output(new_node, output, Algorithms.UCS)
                break
            visited.append(new_node.cid)
            expand(new_node, fringe, visited, output, Algorithms.UCS)

    def ids(self, node):
        output = models.Output
        depth = 0
        while True:
            result = self.new_dls(node, output, depth)
            if result[0] != 'cutoff':
                show_output(result[1], result[2], Algorithms.IDS)
                break
            depth += 1

    def dls(self, node, output, limit):
        fringe = queue.Queue()
        visited = []
        fringe.put(node)
        output.nodes_num += 1
        return self.rec_dls(node, fringe, visited, output, limit)

    def rec_dls(self, node, fringe, visited, output, limit):
        cutoff_occurred = False
        if self.goal_test(node.cid):
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

    def new_dls(self, start_node, output, limit):
        fringe = queue.Queue()
        visited = []
        fringe.put(start_node)
        output.nodes_num += 1
        while True:
            if fringe.empty():
                return 'failure', None, output
            current_node = fringe.get()
            visited.append(current_node.cid)
            if self.goal_test(current_node.cid):
                return 'soln', current_node, output
            elif current_node.depth == limit:
                return 'cutoff', current_node, output
            else:
                expand(current_node, fringe, visited, output, Algorithms.IDS)

    def goal_test(self, cid):
        if cid == self.destination:
            return True
        return False
