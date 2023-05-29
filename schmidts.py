import networkx as nx
from typing import List

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
