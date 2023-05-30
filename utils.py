import generators
import schmidts
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from datetime import datetime, timedelta
import random
import os

# Graph config
nodes = 'abcdefghijklmnoprstuvz'  # length - 22
edge_probability = 0.2

# Display config
layout = nx.spring_layout
font_color = "white"
width = 5
font_size = 20
node_size = 700
font_weight = "bold"

# Path config
file_dir = os.path.dirname(os.path.abspath(__file__))
csv_folder = 'data'

######## Utils ########

# Return path to a file


def getPath(filename):
    return os.path.join(file_dir, csv_folder, filename)


# Generate random color
def randomColor():
    return (round(random.random() * 255), round(random.random() * 255), round(random.random() * 255))


# Convert rgb to hex
def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


# Display how algorithm works on a graph
def displayDemo(G):
    print(nx.adjacency_matrix(G))
    pos = layout(G)

    # Display DFS of a graph
    dfs, dfsArray = schmidts.dfs(G, list(G.nodes)[0])
    print("DFS:", dfsArray)
    nx.draw(dfs, pos=pos, with_labels=True, font_color=font_color, node_color="black",
            width=width, font_size=font_size, node_size=node_size, font_weight=font_weight)
    plt.show()

    # Print ear decomposition of a graph
    earDec = schmidts.earDecomposition(G)
    print("Ear Decomposition: ", earDec)

    # Display graph
    nx.draw(G, pos=pos, with_labels=True, font_color=font_color, node_color="black",
            width=width, font_size=font_size, node_size=node_size, font_weight=font_weight)
    plt.show()

    # Display ear decomposition of a graph. Each ear has a different color
    edges = list(G.edges())
    for (u, v) in edges:
        G.add_edge(u, v, color="white")

    for block in earDec:
        for ear in block:
            i = 0
            earColor = rgb_to_hex(randomColor())
            while i + 1 < len(ear):
                G.add_edge(ear[i], ear[i+1], color=earColor)
                i += 1

    colors = [G[u][v]['color'] for u, v in edges]

    nx.draw(G, pos=pos, edge_color=colors, with_labels=True, font_color=font_color,
            width=width, font_size=font_size, node_size=node_size, font_weight=font_weight)
    plt.show()


# Plot CSV data
def plotCSV(filename: str, title: str, xLabel="Coeficient", yLabel="Time (s)", xColumn="coef", yColumn="time", convertY=lambda y: y):
    df = pd.read_csv(getPath(filename))
    plt.plot(df[xColumn], [convertY(i) for i in df[yColumn]], label=title)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(title)
    plt.legend()
    plt.show()

# Plot JSON data


def plotJSON(filename: str, title: str, xLabel="Coeficient", yLabel="Time (s)", xColumn="coef", yColumn="time", convertY=lambda y: y):
    df = pd.read_json(getPath(filename))
    plt.plot(df[xColumn], [convertY(i) for i in df[yColumn]], label=title)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(title)
    plt.legend()
    plt.show()


def displayBasicDiagrams(filename, xLabel, titlePrefix="", grouped=False):
    plotJSON(filename, titlePrefix + " (Time)", xLabel=xLabel,
             yColumn=("timePerTest" if grouped else "time"))
    plotJSON(filename, titlePrefix + " (Blocks in graph)", xLabel=xLabel,
             yLabel="Number of Blocks", yColumn="result", convertY=lambda y: y["avgNumberOfBlocks"])
    plotJSON(filename, titlePrefix + " (Ears per Block)", xLabel=xLabel,
             yLabel="Number of Ears", yColumn="result", convertY=lambda y: y["avgEarsPerBlock"])
    plotJSON(filename, titlePrefix + " (Average Ear Size)", xLabel=xLabel,
             yLabel="Ear size (nodes)", yColumn="result", convertY=lambda y: y["avgEarSize"])
    plotJSON(filename, titlePrefix + " (Max Block Size)", xLabel=xLabel,
             yLabel="Block size (ears)", yColumn="result", convertY=lambda y: y["maxBlock"])
    plotJSON(filename, titlePrefix + " (Max Ear Size)", xLabel=xLabel,
             yLabel="Ear size (nodes)", yColumn="result", convertY=lambda y: y["maxEar"])
