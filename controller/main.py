from model.mixedCongruentialMethod import MixedCongruentialMethod
import model.kolmogorovSmirnov as kolmogorovSmirnov

class Control:
    
    def __init__(self):
        self.run = None

    def runProgram(self):
        mixedCongruentialMethod = MixedCongruentialMethod(4,5,7,8)
        mixedCongruentialMethod.generateNumbers()
        return kolmogorovSmirnov.calculate(mixedCongruentialMethod.doubleValues)
        

    
