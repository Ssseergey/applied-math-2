import numpy as np

class Solver:
    def __init__(self, A, b):
        self.A = A
        self.b = b
        self.used_basises = []
        self.iteration = 0
        self.basis = []

    def solve(self):
        self.basis = [i for i in range(len(self.b) - 1)]
        rows = [i for i in range(len(self.b) - 1)]
        columns = rows.copy()
        self.findFirstBasis(rows, columns)
        self.used_basises.append(self.basis.copy())

        while(self.iteration == 0 or not optimal):
            print("basis:", self.basis)
            print("used_basises", self.used_basises)
            self.iteration += 1
            optimal = self._step()

        self.values_for_basis = {}
        for item in self.basis:
            for i in range(len(self.A) - 1):
                if self.A[i][item] != 0:
                    self.values_for_basis[str(item)] = self.b[i]

        print(self.A)
        print(self.b)
        print("basis_values:", self.values_for_basis)
        print("function value = ", self.function())

    def _step(self):
        optimal, column = self.isOptimalBasis()
        if optimal:
            return optimal

        row = self.divideBOnColumn(column)
        temp = self.basis.copy()
        temp[row] = column
        if temp not in self.used_basises:
            self.basis[row] = column
            self.used_basises.append(self.basis.copy())
        else:
            return True

        self.makeSolveElementPossibleBasis(column, row)
        return False

    def findFirstBasis(self, rows, columns):
        for j in range(len(rows)):
            self.makeSolveElementPossibleBasis(columns[j], rows[j])

    def isOptimalBasis(self):
        min_item = self.A[-1][0]
        column = 0
        for i, item in enumerate(self.A[-1]):
            if item < min_item:
                min_item = item
                column = i
        return min_item >= 0, column

    def divideBOnColumn(self, column):
        solve_column = []
        min_item = 0
        row = -1
        for i in range(len(self.A) - 1):
            if self.A[i][column] == 0:
                value = -1
            else:
                value = self.b[i] / self.A[i][column]
            solve_column.append(value)
            if value >= 0 and value > min_item:
                value = min_item
                row = i
        return row

    def makeSolveElementPossibleBasis(self, column, row):
        element = self.A[row][column]
        if element != 1:
            self.A[row] /= element
            self.b[row] /= element
        for i in range(len(self.A) - 1):
            if i != row:
                multiplier = self.A[i][column]
                self.A[i] -= self.A[row] * multiplier
                self.b[i] -= self.b[row] * multiplier

    def function(self):
        sum = 0
        for i in range(len(self.A[-1])):
            try:
                sum -= self.A[-1][i] * self.values_for_basis[str(i)]
            except:
                pass
        return sum
