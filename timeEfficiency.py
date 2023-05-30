import generators
import schmidts
import timeInfo
import utils
import networkx as nx
import matplotlib.pyplot as plt
import json

# Investigate algorithms time efficiency with different graph sizes. Export results to csv


def size():
    graphSizeAnalysis = timeInfo.withTimeInfo(schmidts.earDecomposition)
    connectedGraphGenerator = generators.ensureConnectivity(
        nx.erdos_renyi_graph)
    options = timeInfo.TimeInfoOptions(
        1, 100, 1, 100, "Complete", lambda N: [nx.complete_graph(N)], resultGenerator=schmidts.generateResult)
    graphSizeAnalysis(options)

# Investigate algorithms time efficiency with different edge probabilities. Export results to csv

def density():
    graphDensityAnalysis = timeInfo.withTimeInfo(schmidts.earDecomposition)
    options = timeInfo.TimeInfoOptions(
        0, 1, 0.01, 100, "Density", lambda p, N: [nx.erdos_renyi_graph(N, p)], resultGenerator=schmidts.generateResult)
    graphDensityAnalysis(options, 75)

utils.displayBasicDiagrams("Complete-20230530203539.json", "Different density graphs", grouped=True)
