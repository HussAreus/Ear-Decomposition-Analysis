# imports and Constants
import networkx as nx
import random
from typing import List, Callable


def generateGraph(labels: List[any], edgeProbability=0.2) -> nx.Graph:
    G = nx.Graph()
    G.add_nodes_from(labels)
    for l1 in labels:
        for l2 in labels:
            if l1 != l2 and random.random() < edgeProbability:
                G.add_edge(l1, l2)
    return G


def ensureConnectivity(func: Callable[..., nx.Graph]):
    def wrapper(*args, **kwargs):
        G = func(*args, **kwargs)
        while not nx.is_connected(G):
            G = func(*args, **kwargs)
        return G
    return wrapper


def ensureBiconnectivity(func: Callable[..., nx.Graph]):
    def wrapper(*args, **kwargs):
        G = func(*args, **kwargs)
        while not nx.is_biconnected(G):
            G = func(*args, **kwargs)
        return G
    return wrapper
