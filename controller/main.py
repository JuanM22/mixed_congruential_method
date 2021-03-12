from model.mixedCongruentialMethod import MixedCongruentialMethod
import model.kolmogorovSmirnov as kolmogorovSmirnov

class Control:
    
    def __init__(self):
        self.run = None

    def getRandomNumbers(self, x0, a, c, m):
        mixedCongruentialMethod = MixedCongruentialMethod(x0,a,c,m)
        mixedCongruentialMethod.generateNumbers()
        return mixedCongruentialMethod.doubleValues
        
    def getKolmogorovSmirnovRes(self, values):
        return kolmogorovSmirnov.calculate(values)