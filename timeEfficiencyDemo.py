import schmidts
import timeInfo
import utils
import networkx as nx

# Reuslt generator demo. <result> here is function function result
def resultGenerator(results):
    totalBlocks = 0
    for result in results:
        blocks = list(result)
        totalBlocks += len(blocks)
        
    avgNumberOfBlocks = totalBlocks / len(results)
    return {
        "avgNumberOfBlocks": avgNumberOfBlocks,
    }

# Generate results for different graph sizes. Using Complete graph generator
def size():
    graphSizeAnalysis = timeInfo.withTimeInfo(nx.connected_components)
    options = timeInfo.TimeInfoOptions(
        1, 100, 1, 100, "Complete", lambda N: [nx.complete_graph(N)], resultGenerator=resultGenerator)
    graphSizeAnalysis(options)


# Display analysis resuls
utils.displayBasicDiagrams("Complete-20230530203539.json", "Different density graphs", grouped=True)


# Generate results for different edge probabilities
def density():
    graphDensityAnalysis = timeInfo.withTimeInfo(schmidts.earDecomposition)
    options = timeInfo.TimeInfoOptions(
        0, 1, 0.01, 100, "Density", lambda p, N: [nx.erdos_renyi_graph(N, p)], resultGenerator=schmidts.generateResult)
    graphDensityAnalysis(options, 75)