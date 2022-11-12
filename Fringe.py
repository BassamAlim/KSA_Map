import queue

from Algorithms import Algorithms


class Fringe:
    container = None
    algorithm = Algorithms.Empty

    def __init__(self, algo):
        self.algorithm = algo
        match algo:
            case Algorithms.BFS:
                self.container = queue.Queue()
            case Algorithms.UCS | Algorithms.Greedy | Algorithms.A_Star:
                self.container = queue.PriorityQueue()
            case Algorithms.IDS:
                self.container = []
            case _:
                self.container = None

    def put(self, node):
        if self.algorithm == Algorithms.IDS:
            self.container.append(node)
        else:
            self.container.put(node)

    def remove_first(self):
        match self.algorithm:
            case Algorithms.BFS:
                return self.container.get()
            case Algorithms.IDS:
                return self.container.pop()
            case _:
                return self.container.get()[2]

    def size(self):
        if self.algorithm == Algorithms.IDS:
            return len(self.container)
        else:
            return self.container.qsize()

    def empty(self):
        if self.algorithm == Algorithms.IDS:
            return len(self.container) == 0
        else:
            return self.container.empty()
