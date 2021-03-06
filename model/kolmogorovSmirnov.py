import numpy as np

def __ranges(val):
   return [(val >= 0.0 and val < 0.1), (val >= 0.1 and val < 0.2), (val >= 0.2 and val < 0.3), (val >= 0.3 and val < 0.4),
        (val >= 0.4 and val < 0.5), (val >= 0.5 and val < 0.6), (val >= 0.6 and val < 0.7), (val >= 0.7 and val < 0.8),
        (val >= 0.8 and val < 0.9), (val >= 0.9 and val < 1.0)]


def calculate(arr):
    table = __createEmptyTable(10, 7)
    __calculateFrequency(arr, table)  # Primera columna llena
    __calculateEarnedFrequencyAcumulated(table)  # Segunda columna llena
    __probabilityEarnedAcumulated(table, len(arr))  # Tercera columna llena
    __expectedFrequency(table, len(arr), 10)  # Cuarta columna llena
    __expectedFrequencyAcumulated(table)  # Quinta columna llena
    __expectedProbabilityAcumulated(table, len(arr))  # Sexta columna llena
    __difference(table)  # Séptima columna llena
    print(table)

def __createEmptyTable(rows, columns):
    return np.zeros((rows, columns))


def __calculateFrequency(arr, table):
    for i in range(0, len(arr)):
        ranges = __ranges(arr[i])
        rowIndex = ranges.index(True)
        table[rowIndex][0] += 1


def __calculateEarnedFrequencyAcumulated(table):
    table[0][1] = table[0][0]
    for i in range(1, np.shape(table)[0]):
        table[i][1] = table[i-1][1] + table[i][0]


def __probabilityEarnedAcumulated(table, n):
    for i in range(0, np.shape(table)[0]):
        table[i][2] =  "{:.4f}".format(round(table[i][1] / n, 4))  


def __expectedFrequency(table, n, intervals):
    for i in range(0, np.shape(table)[0]):
        table[i][3] = n / intervals


def __expectedFrequencyAcumulated(table):
    table[0][4] = table[0][3]
    for i in range(1, np.shape(table)[0]):
        table[i][4] = table[i-1][4] + table[i][3]


def __expectedProbabilityAcumulated(table, n):
    for i in range(0, np.shape(table)[0]):
        table[i][5] = "{:.4f}".format(round(table[i][4] / n, 4))  


def __difference(table):
    for i in range(0, np.shape(table)[0]):
        table[i][6] = table[i][2] - table[i][5]
