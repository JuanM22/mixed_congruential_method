import math

class MixedCongruentialMethod:

    def __init__(self, X0, a, c, m):
        self.period = []
        self.doubleValues = []
        self.Xn = X0
        self.a = a
        self.c = c
        self.m = m

    def generateNumbers(self):
        periodFounded = False
        for i in range(0, self.m + 1):
            number = ((self.a * self.Xn) + self.c) % self.m
            if(not(periodFounded)):
                doubleNumber = (number/self.m)
                if(doubleNumber in self.doubleValues):
                    self.period.append(self.doubleValues.index(
                        doubleNumber))  # Inicio de periodo
                    self.period.append(i)  # Fin de periodo
                    periodFounded = True
            self.doubleValues.append(number/self.m)
            self.Xn = number
        self.doubleValues.pop()

    def roundNumbers(self):
        for i, number in enumerate(self.doubleValues):
            self.doubleValues[i] = round(number,4)
