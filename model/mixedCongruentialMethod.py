import math

class MixedCongruentialMethod:

    def __init__(self, X0, a, c, m):
        self.intValues = []
        self.doubleValues = []
        self.Xn = X0
        self.a = a
        self.c = c
        self.m = m


    def generateNumbers(self):
        for _ in range(0,self.m):
            number = ((self.a * self.Xn) + self.c) % self.m
            self.intValues.append(number)  
            self.doubleValues.append(round((number/self.m), 4))
            self.Xn = number
