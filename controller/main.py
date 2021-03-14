from model.mixedCongruentialMethod import MixedCongruentialMethod
import model.kolmogorovSmirnov as kolmogorovSmirnov
import model.kolmogorovSmirnovTable as tableValue
import numpy

class Control:
    
    def __init__(self):
        self.run = None

    def getRandomNumbers(self, x0, a, c, m):
        mixedCongruentialMethod = MixedCongruentialMethod(x0,a,c,m)
        mixedCongruentialMethod.generateNumbers()
        mixedCongruentialMethod.roundNumbers()
        return mixedCongruentialMethod
        
    def getKolmogorovSmirnovRes(self, values):
        return kolmogorovSmirnov.calculate(values)


    def getDifferenceMaxValue(self, values):
        arr = values[:, numpy.shape(values)[1] - 1]
        return max(arr)

    def getKolmogorovTableValue(self, alpha, n):
        return tableValue.getTableValue(alpha,n)