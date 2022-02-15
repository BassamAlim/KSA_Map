class Node:
    cid = -1
    name = ''
    parent = object
    path_cost = 0

    def __init__(self, cid, cname, parent, path_cost):
        self.cid = cid
        self.name = cname
        self.parent = parent
        self.path_cost = path_cost


class Result:
    route = []
    distance = 0
    nodes_num = 0
    fringe_max_size = 1
