import numpy as np

def __ranges(val):
   return [(val >= 0.0 and val < 0.1), (val >= 0.1 and val < 0.2), (val >= 0.2 and val < 0.3), (val >= 0.3 and val < 0.4),
        (val >= 0.4 and val < 0.5), (val >= 0.5 and val < 0.6), (val >= 0.6 and val < 0.7), (val >= 0.7 and val < 0.8),
        (val >= 0.8 and val < 0.9), (val >= 0.9 and val < 1.0)]

def calculate(arr):
    table = __createEmptyTable(10, 7)
    __calculateFrequency(arr, table)
    __calculateAccumulatedFrequency(table, 1)
    __accumulatedProbability(table, len(arr), 2)
    __expectedFrequency(table, len(arr), 10)
    __calculateAccumulatedFrequency(table, 4)
    __accumulatedProbability(table, len(arr), 5)
    __difference(table)
    return table

def __createEmptyTable(rows, columns):
    return np.zeros((rows, columns))

def __calculateFrequency(arr, table):
    for i in range(0, len(arr)):
        ranges = __ranges(arr[i])
        rowIndex = ranges.index(True)
        table[rowIndex][0] += 1

def __calculateAccumulatedFrequency(table, col):
    table[0][col] = table[0][col - 1]
    for i in range(1, np.shape(table)[0]):
        table[i][col] = table[i-1][col] + table[i][col - 1]

def __accumulatedProbability(table, n, col):
    for i in range(0, np.shape(table)[0]):
        table[i][col] =  round(table[i][col - 1] / n, 4)  

def __expectedFrequency(table, n, intervals):
    for i in range(0, np.shape(table)[0]):
        table[i][3] = n / intervals

def __difference(table):
    for i in range(0, np.shape(table)[0]):
        table[i][6] = table[i][2] - table[i][5]
