import utils

from typing import List, Callable

import gc
import pandas as pd
import time
from datetime import datetime, timedelta


# Claculates function execution time
def withTimer(func: Callable):
    def wrapper(*args, **kwargs):
        gc.disable()
        start = time.perf_counter_ns()
        result = func(*args, **kwargs)
        end = time.perf_counter_ns()
        gc.enable()
        delta = (end - start)/1e9
        return result, delta
    return wrapper


class TimeInfoOptions:
    def __init__(self, start: float, end: float, delta: float, numberOfTests: int, filename: str, argumentsGenerator: Callable[..., List]):
        self.coeficient = [
            i * delta for i in range(int(end/delta) + 1) if i * delta >= start]
        self.numberOfTests = numberOfTests
        self.filename = filename
        self.argumentsGenerator = argumentsGenerator


# Calculates function execution time, prints progress, saves results to csv file, predicts time left till end of investigation
def withTimeInfo(func: Callable):
    def wrapper(options, *args, **kwargs):
        investigationStart = time.perf_counter_ns()
        lastDeltaTime = 0
        growth = []
        functionWithTimer = withTimer(func)
        results = []

        for i, coef in enumerate(options.coeficient):
            totalTime = 0
            for _ in range(options.numberOfTests):
                arguments = options.argumentsGenerator(coef, *args, **kwargs)
                result, delta = functionWithTimer(*arguments)
                totalTime += delta
            results.append({
                'coef': coef,
                'result': result,
                'time': totalTime / options.numberOfTests
            })

            # Calculate time left till end of investigation
            timePerTest = totalTime / options.numberOfTests
            if (lastDeltaTime > 0):
                growth.append(timePerTest / lastDeltaTime)
            lastDeltaTime = timePerTest

            # Average time growth
            if (len(growth) > 0):
                averageGrowth = sum(growth) / len(growth)
                timeLeft = 0.0
                currentGrowth = averageGrowth

                for n in range(i+1, len(options.coeficient)):
                    timeLeft += totalTime * currentGrowth
                    currentGrowth *= averageGrowth
                print(f"Time left: " + (str(timedelta(seconds=timeLeft)) if timeLeft < 1e14 else "Too long"))

            print(
                f"Time elapsed: {str(timedelta(seconds=(time.perf_counter_ns() - investigationStart)/1e9))} seconds")
            print(
                f"Completed: {round(100 * (i+1)/len(options.coeficient))}%\n")
        # Export to csv
        pd.DataFrame(results).to_csv(utils.getPath(options.filename + '-' +
                                                   str(datetime.now().strftime("%Y%m%d%H%M%S")) + '.csv'), index=False)
    return wrapper
