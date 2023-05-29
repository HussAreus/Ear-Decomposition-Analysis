# Investigate algorithms time efficiency with different graph sizes. Export results to csv
def timeEfficiency(N, edge_probability, delta, numberOfTests, graphGenerator=generators.generateConnected):
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
            earDec = generators.earDecomposition(G)
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


def timeEfficiencyEdgeProb(N, delta, numberOfTests, graphGenerator=generators.generateConnected):
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
            earDec = generators.earDecomposition(G)
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
            earDec = generators.earDecomposition(G)
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