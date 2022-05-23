class Node:
    cid = -1
    path_cost = 0
    predecessors = []
    depth = 0

    def __init__(self, cid, path_cost, predecessors=None, depth=0):
        self.cid = cid
        self.path_cost = path_cost
        if predecessors is not None:
            self.predecessors = list(predecessors)
        self.depth = depth


class Chromosome:
    def __init__(self, gnome, fitness):
        self.gnome = gnome
        self.fitness = fitness

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __gt__(self, other):
        return self.fitness > other.fitness


class Output:
    route = []
    distance = 0
    nodes_num = 1
    fringe_max_size = 1

    def __init__(self, route=None, distance=0):
        if route is not None:
            self.route = list(route)
            self.distance = distance
