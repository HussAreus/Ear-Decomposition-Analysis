# imports and Constants
import networkx as nx
import random
from typing import List
from datetime import datetime, timedelta
import pandas as pd
import os

# Paths
file_dir = os.path.dirname(os.path.abspath(__file__))
csv_folder = 'data'


def getPath(filename):
    return os.path.join(file_dir, csv_folder, filename)

# Graph generators


def generateGraph(labels: List[any], edgeProbability=0.2):
    G = nx.Graph()
    G.add_nodes_from(labels)
    for l1 in labels:
        for l2 in labels:
            if l1 != l2 and random.random() < edgeProbability:
                G.add_edge(l1, l2)
    return G


def generateConnected(labels: List[any], edgeProbability=0.2):
    G = generateGraph(labels, edgeProbability)
    while not nx.is_connected(G):
        G = generateGraph(labels, edgeProbability)
    return G


def generateConnected(n: int, edgeProbability=0.2):
    G = nx.generators.random_graphs.erdos_renyi_graph(n, edgeProbability)
    while not nx.is_connected(G):
        G = nx.generators.random_graphs.erdos_renyi_graph(n, edgeProbability)
    return G


def dfs(graph: nx.Graph, root: any):
    dfsTree = nx.DiGraph()
    dfsTree.add_nodes_from(graph)
    dfsArray = [root]
    dfsRecursive(graph, root, dfsArray, dfsTree)
    return dfsTree, dfsArray


def dfsRecursive(graph: nx.Graph, root: any, dfsArray: List[any], dfsTree: nx.DiGraph):
    for (u, v) in graph.edges([root]):
        if v not in dfsArray:
            dfsArray.append(v)
            dfsTree.add_edge(u, v)
            dfsRecursive(graph, v, dfsArray, dfsTree)


def earDecomposition(graph: nx.Graph):
    nodes = list(graph.nodes)
    if len(nodes) <= 0:
        return []
    visited = []
    visited_edges = []
    blockList = []
    for root in nodes:
        # If graph is not connected we'll need more than one root
        if root in visited:
            continue
        visited.append(root)
        # Based on root, generates DFS tree. Dfs array will contain DFS as a node list
        dfsTree, dfsArray = dfs(graph, root)

        block = []
        # Go through DFS
        for node in dfsArray:
            # Go through edges that contain node
            for (u, v) in graph.edges([node]):
                # Checking if it's a direct edge
                if v in dfsTree.successors(node) or v in dfsTree.predecessors(node):
                    continue
                # ELSE: It's a backedge
                if (u, v) in visited_edges or (v, u) in visited_edges:
                    continue

                visited_edges.append((u, v))
                # Backedge means we found an ear. We traverse it:
                ear = [node]
                x = v
                while True:
                    ear.append(x)
                    if x in visited:
                        break
                    visited.append(x)
                    x = list(dfsTree.predecessors(x))[0]
                    visited_edges.append((x, visited[len(visited)-1]))
                block.append(ear)
        blockList.append(block)
    return blockList


def withTimer(func):
    def wrapper(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        end = datetime.now()
        time = end - start
        return result, time

    return wrapper


def withTimeInfo(func):
    def wrapper(N, numberOfTests, delta=1, generator=nx.generators.erdos_renyi_graph, filename="graph", start=0, *args, **kwargs):
        data = []
        investigationStart = datetime.now()
        lastUpdateDeltatime = 0
        multipliers = []
        timerFunc = withTimer(func)

        Ns = [i * delta for i in range(int(N/delta) + 1) if i * delta >= start]
        for index, n in enumerate(Ns):
            totalTime = 0
            numberOfEarsPerBlock = 0
            numberOfBlocks = 0
            for i in range(numberOfTests):
                G = generator(n, *args, **kwargs)
                earDec, time = timerFunc(G)

                numberOfBlocks += len(earDec)
                for block in earDec:
                    numberOfEarsPerBlock += len(block)
                totalTime += time.total_seconds()

            timePerTest = totalTime / numberOfTests
            data.append({'n': n, 'blocks': numberOfBlocks / numberOfTests,
                         'ears per block': numberOfEarsPerBlock / numberOfTests, 'time': timePerTest})

            # Calculate time left till end of investigation
            if (lastUpdateDeltatime > 0):
                multipliers.append(timePerTest / lastUpdateDeltatime)
            averageMultiplier = sum(
                multipliers) / len(multipliers) if len(multipliers) > 0 else 1
            timeleft = 0.0
            if (averageMultiplier > 0):
                for j in range(index+1, len(Ns)):
                    timeleft += lastUpdateDeltatime * \
                        numberOfTests * pow(averageMultiplier, j-index)
                    # If timeleft is too big, stop calculating
                    if timeleft > 60 * 60 * 24 * 365 * 10:
                        break

            # Update times
            lastUpdateDeltatime = timePerTest
            print("Completed: ", round(100 * (index+1)/len(Ns)),
                  "%\nTime lapsed: ", round(
                (datetime.now() - investigationStart).total_seconds(), 2),
                "s\nLast update: ", round(
                    lastUpdateDeltatime * numberOfTests, 2),
                "s\nTime left: ", str(timedelta(seconds=timeleft)) if timeleft >= 0 else "Unknown", "\n")
        pd.DataFrame(data).to_csv(getPath(
            filename + '-' + str(datetime.now().strftime("%Y%m%d%H%M%S")) + '.csv'), index=False)
    return wrapper
