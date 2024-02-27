from pyvis.network import Network
import json
import random

def to_tuple(edges):
    res = []
    for i, adj in enumerate(edges):
        for j in adj:
            res.append((i, j))
    return res

class Visualizer:
    def __init__(self, nodes, edges, special=[]) -> None:
        self.nodes = nodes
        self.edges = edges
        self.network = Network(height='600px', width='1500px', directed=True)

        node_list = list(nodes.keys()) 
        titles = [node.get_description() for node in node_list if node]
        generated_colors = ["#"+''.join([random.choice('abcdef0123456789') for i in range(6)]) for j in range(50)]
        # print(generated_colors)
        colors = [generated_colors[list(node.test_id)[0]] if node.test_id else generated_colors[-1] for node in node_list]
        # colors = ['#0000ff' if self.nodes[node] not in special else '#ff0000' for node in node_list]
        self.network.add_nodes(list(nodes.values()), title=titles, color=colors)
        edges = to_tuple(edges)
        self.network.add_edges(edges)

        for n in self.network.nodes:
            n.update({'physics': False})
        
        self.network.barnes_hut()
        # self.network.force_atlas_2based()
        # self.network.repulsion()
        # self.network.hrepulsion()

    
    def show(self, name='final.html'):

        self.network.show(name)

