import networkx as nx
import matplotlib.pyplot as plt
import json
from bidi.algorithm import get_display
import arabic_reshaper


with open('Cities.json', encoding='utf-8') as file:
    data = json.load(file)


class Network:

    def __init__(self):
        self.G = nx.DiGraph()
        self.lats = [city['x'] for city in data]
        self.lons = [city['y'] for city in data]
        self.labels = {i: get_display(arabic_reshaper.reshape(city['name'])) for i, city in enumerate(data)}
        self.names = [city['name'] for city in data]
        self.regions = [city['rid'] for city in data]
        self.pos = {i: (self.lons[i], self.lats[i]) for i in range(len(data))}

    def buildGraph(self):
        self.add_nodes()
        self.add_edges()
        return self.G

    def add_nodes(self):
        for city in data:
            self.G.add_node(city['cid'], name=city['name'], region=city['rid'], lat=city['x'], lon=city['y'])

    def add_edges(self):
        for city in data:
            for neighbor in city['neighbors']:
                self.G.add_edge(city['cid'], neighbor['cid'], weight=neighbor['distance'])

    def plot(self):
        nx.draw(self.G, pos=self.pos, labels=self.labels, with_labels=True, node_color=self.regions, font_size=8)

        ax = plt.gca()
        ax.margins(0.08)
        plt.axis("off")
        plt.tight_layout()
        plt.show()
