from model.mixedCongruentialMethod import MixedCongruentialMethod

class Control:
    
    def __init__(self):
        self.run = None

    def runProgram(self):
        mixedCongruentialMethod = MixedCongruentialMethod(4,5,7,8)
        mixedCongruentialMethod.generateNumbers()
        print(mixedCongruentialMethod.intValues)
        print(mixedCongruentialMethod.doubleValues)
