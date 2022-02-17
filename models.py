class Node:
    cid = -1
    name = ''
    path_cost = 0
    parent = object

    def __init__(self, cid, cname, path_cost, parent):
        self.cid = cid
        self.name = cname
        self.path_cost = path_cost
        self.parent = parent


class Result:
    route = []
    distance = 0
    nodes_num = 0
    fringe_max_size = 1
