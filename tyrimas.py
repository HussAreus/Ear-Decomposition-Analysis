import algoritmai
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from datetime import datetime, timedelta
import os

# Graph config
nodes = 'abcdef'
edge_probability = 0.2

# Display config
layout = nx.spring_layout
font_color = "white"
width = 5
font_size = 20
node_size = 700
font_weight = "bold"

# Paths
file_dir = os.path.dirname(os.path.abspath(__file__))
csv_folder = 'data'


def getPath(filename):
    return os.path.join(file_dir, csv_folder, filename)


# Generate graph
def displayDemo(G):
    print(nx.adjacency_matrix(G))
    pos = layout(G)

    # Display DFS of a graph
    dfs, dfsArray = algoritmai.dfs(G, list(G.nodes)[0])
    print("DFS:", dfsArray)
    nx.draw(dfs, pos=pos, with_labels=True, font_color=font_color, node_color="black",
            width=width, font_size=font_size, node_size=node_size, font_weight=font_weight)
    plt.show()

    # Print ear decomposition of a graph
    earDec = algoritmai.earDecomposition(G)
    print("Ear Decomposition: ", earDec)

    # Display graph
    nx.draw(G, pos=pos, with_labels=True, font_color=font_color, node_color="black",
            width=width, font_size=font_size, node_size=node_size, font_weight=font_weight)
    plt.show()


# Investigate algorithms time efficiency with different graph sizes. Export results to csv
def timeEfficiency(N, edge_probability, delta, numberOfTests, graphGenerator=algoritmai.generateConnected):
    data = []
    investigationTime = datetime.now()
    lastUpdate = datetime.now()
    for n in range(1, N, delta):
        sum = 0
        numberOfEarsPerBlock = 0
        numberOfBlocks = 0
        for i in range(numberOfTests):
            G = graphGenerator(n, edge_probability)
            start = datetime.now()
            earDec = algoritmai.earDecomposition(G)
            end = datetime.now()
            time = end - start
            numberOfBlocks += len(earDec)
            for block in earDec:
                numberOfEarsPerBlock += len(block)
            sum += time.total_seconds()
        data.append({'n': n, 'blocks': numberOfBlocks / numberOfTests,
                    'ears per block': numberOfEarsPerBlock / numberOfTests, 'time': sum / numberOfTests})
        print("Completed: ", n, " out of ", N, " Time lapsed: ",
              (datetime.now() - investigationTime).total_seconds(), "s", " Last update: ", (datetime.now() - lastUpdate).total_seconds(), "s")
        lastUpdate = datetime.now()
    pd.DataFrame(data).to_csv(getPath(
        'deltaN-' + str(datetime.now().strftime("%Y%m%d%H%M%S")) + '.csv'), index=False)


# Investigate algorithms time efficiency with different edge probabilities. Export results to csv
def timeEfficiencyEdgeProb(N, delta, numberOfTests, graphGenerator=algoritmai.generateConnected):
    data = []
    investigationTime = datetime.now()
    lastUpdate = datetime.now()
    lastUpdateDeltatime = 0
    multipliers = []

    probabilities = []
    i = 0
    while round(i, 5) <= 1:
        probabilities.append(round(i, 5))
        i += delta

    for index, p in enumerate(probabilities):
        suma = 0
        numberOfEarsPerBlock = 0
        numberOfBlocks = 0
        for i in range(numberOfTests):
            G = graphGenerator(N, p)
            start = datetime.now()
            earDec = algoritmai.earDecomposition(G)
            end = datetime.now()
            time = end - start
            numberOfBlocks += len(earDec)
            for block in earDec:
                numberOfEarsPerBlock += len(block)
            suma += time.total_seconds()

        data.append({'p': p, 'blocks': numberOfBlocks / numberOfTests,
                    'ears per block': numberOfEarsPerBlock / numberOfTests, 'time': suma / numberOfTests})

        # Calculate time left till end of investigation
        if lastUpdateDeltatime > 0:
            multipliers.append(
                (datetime.now() - lastUpdate).total_seconds()/lastUpdateDeltatime)
        averageMultiplier = sum(multipliers) / \
            len(multipliers) if len(multipliers) > 0 else 1
        timeleft = 0
        for j in range(index+1, len(probabilities)):
            timeleft += lastUpdateDeltatime * pow(averageMultiplier, j-index)

        # Update times and print progress
        lastUpdateDeltatime = (datetime.now() - lastUpdate).total_seconds()
        lastUpdate = datetime.now()
        print("Completed: ", round(100 * (index+1)/len(probabilities)),
              "%\nTime lapsed: ", round(
                  (datetime.now() - investigationTime).total_seconds(), 2),
              "s\nLast update: ", round(lastUpdateDeltatime, 2),
              "s\nTime left: ", str(timedelta(seconds=round(timeleft, 2))), "\n")

    pd.DataFrame(data).to_csv(getPath(
        'deltaP-' + str(datetime.now().strftime("%Y%m%d%H%M%S"))) + '.csv', index=False)


def differentGraphAnalysis(N, numberOfTests):
    data = []
    investigationTime = datetime.now()
    lastUpdate = datetime.now()
    for n in range(1, N):
        sum = 0
        numberOfEarsPerBlock = 0
        numberOfBlocks = 0
        for i in range(numberOfTests):
            G = nx.generators.grid_2d_graph(n, n)
            start = datetime.now()
            earDec = algoritmai.earDecomposition(G)
            end = datetime.now()
            time = end - start
            numberOfBlocks += len(earDec)
            for block in earDec:
                numberOfEarsPerBlock += len(block)
            sum += time.total_seconds()
        data.append({'n': n, 'blocks': numberOfBlocks / numberOfTests,
                    'ears per block': numberOfEarsPerBlock / numberOfTests, 'time': sum / numberOfTests})
        print("Completed: ", n, " out of ", N, " Time lapsed: ",
              (datetime.now() - investigationTime).total_seconds(), "s", " Last update: ", (datetime.now() - lastUpdate).total_seconds(), "s")
        lastUpdate = datetime.now()
    pd.DataFrame(data).to_csv(getPath(
        'whele-' + str(datetime.now().strftime("%Y%m%d%H%M%S")) + '.csv'), index=False)


#differentGraphAnalysis(100, 10)
#

earDecompositionTest = algoritmai.withTimeInfo(algoritmai.earDecomposition)
def random_regular_graph(n, d):
    return nx.random_regular_graph(d, n)
earDecompositionTest(200, 50, 2, nx.erdos_renyi_graph, "erdos", 0, 0.2)

def biconnected_components(G):
    return list(nx.biconnected_components(G))
biconnectedTest = algoritmai.withTimeInfo(biconnected_components)
biconnectedTest(200, 50, 2, nx.erdos_renyi_graph, "erdos_nx", 0, 0.2)