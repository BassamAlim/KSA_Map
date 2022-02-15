class Node:
    cid = -1
    city_name = ''
    parent = ''
    neighbors = []
    path_cost = 0

    def __init__(self, cid, cname, parent, neighbors, path_cost):
        self.cid = cid
        self.city_name = cname
        self.parent_id = parent
        self.neighbors = neighbors
        self.path_cost = path_cost


class Result:
    route = 0
    distance = 0
    nodes_num = 0
    fringe_max_size = 0

    def __init__(self, route, distance, nodes_num, fringe_max_size):
        self.route = route
        self.distance = distance
        self.nodes_num = nodes_num
        self.fringe_max_size = fringe_max_size
