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

    def roundNumbers(self):
        for i, number in enumerate(self.doubleValues):
            self.doubleValues[i] = round(number,4)


# mixedCongruentialMethod = MixedCongruentialMethod(X0, a, c, m)
# mixedCongruentialMethod.generateNumbers()
# mixedCongruentialMethod.roundNumbers()
# print(mixedCongruentialMethod.doubleValues)
# print(mixedCongruentialMethod.period)
# print('')

# start = mixedCongruentialMethod.period[0]
# end = mixedCongruentialMethod.period[1]

# print(mixedCongruentialMethod.period)
# print('Periodo -> ', (end - start))
# for i in range(start, end):
#     print(mixedCongruentialMethod.doubleValues[i])
