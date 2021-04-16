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
        for i in range(0, self.m + 1):
            number = ((self.a * self.Xn) + self.c) % self.m
            doubleNumber = number/self.m
            self.doubleValues.append(doubleNumber)
            self.Xn = number

        first_duplicate = self.firstDuplicate(self.doubleValues)
        self.period.append(self.doubleValues.index(first_duplicate))
        self.period.append(self.doubleValues.index(first_duplicate,self.period[0] + 1, len(self.doubleValues)))
        self.doubleValues.pop()

    def firstDuplicate(self,a):
        set_ = set()
        for item in a:
            if item in set_:
                return item
            set_.add(item)
        return None
