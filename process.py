import json
import queue

import models


def retrieve_data():
    with open('Cities.json', encoding='utf-8') as file:
        cities = json.load(file)
    return cities


class Process:

    cities = ''
    start = ''
    destination = ''
    fringe = queue.Queue()

    def __init__(self, start_city, end_city):
        self.start = start_city
        self.destination = end_city

        self.cities = retrieve_data()
        self.begin()

    def begin(self):
        result = self.goal_test(self.start)
        if result:
            return models.Result('', 0, 0, 1)
        else:
            neighbors = []
            for neighbor in self.cities[self.start]['neighbors']:
                neighbors.append(neighbor['cid'])

            start_node = models.Node(self.start, self.cities[self.start]['name'], -1, neighbors, 0)
            self.expand(start_node)



    def graph_search(self):
        a = models.Node
        type(a)  # checks for the data type
        pass

    def goal_test(self, state):
        if state == self.destination:
            return True
        return False

    def expand(node):  # returns a set of nodes
        successors = list

        #for action in successor_function():
        #    pass

    def successor_function(self, State):
        return list

    def bfs(self):
        route = list
        distance = 0
        nodes_num = 0
        fringe_max_size = 0

    def ucs(self):
        route = list
        distance = 0
        nodes_num = 0
        fringe_max_size = 0

    def ids(self):
        route = list
        distance = 0
        nodes_num = 0
        fringe_max_size = 0




