import math

class MixedCongruentialMethod:

    def __init__(self, X0, a, c, m):
        self.period = []
        self.doubleValues = set()
        self.Xn = X0
        self.a = a
        self.c = c
        self.m = m

    def generateNumbers(self):
        for i in range(0, self.m + 1):
            number = ((self.a * self.Xn) + self.c) % self.m
            doubleNumber = (number/self.m)
            if(len(self.period) == 0):
                if(doubleNumber in self.doubleValues):
                    self.period.append(list(self.doubleValues).index(doubleNumber))
                    self.period.append(i)
            self.doubleValues.add(doubleNumber)
            self.Xn = number
