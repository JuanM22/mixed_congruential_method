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
        return mixedCongruentialMethod
        
    def getKolmogorovSmirnovRes(self, values):
        return kolmogorovSmirnov.calculate(values)


    def getDifferenceMaxValue(self, values):
        arr = values[:, numpy.shape(values)[1] - 1]
        return max(arr)

    def getKolmogorovTableValue(self, alpha, n):
        return tableValue.getTableValue(alpha,n)


    def validateData(self, X0, a, c, m):
        messages = ''
        if(X0 <= 0):
            messages += "El valor de 'X0' debe ser mayor que cero\n"
        if(a <= 0):
            messages += "El valor de 'a' debe ser mayor que cero\n"
        if(c <= 0):
            messages += "El valor de 'c' debe ser mayor que cero\n"
        if(m <= 0):
            messages += "El valor de 'm' debe ser mayor que cero\n"

        return messages

