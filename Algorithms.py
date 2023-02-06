from enum import Enum


class Algorithms(Enum):
    Empty = 'Pick an Algorithm'
    BFS = 'Breadth First Search'
    UCS = 'Uniform Cost Search'
    IDS = 'Iterative Deepening Search'
    Greedy = 'Greedy'
    A_Star = 'A*'
    HC = 'Hill Climbing'
    SA = 'Simulated Annealing'
    GA = 'Genetic Algorithm'
