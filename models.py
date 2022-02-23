class Node:
    cid = -1
    name = ''
    path_cost = 0
    parent = object
    depth = 0

    def __init__(self, cid, cname, path_cost, parent, depth=0):
        self.cid = cid
        self.name = cname
        self.path_cost = path_cost
        self.parent = parent
        self.depth = depth


class Output:
    route = []
    distance = 0
    nodes_num = 1
    fringe_max_size = 1
