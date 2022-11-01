import numpy as np

class Solver:
    def __init__(self, A, b, max_x, max_var):
        self.A = A
        self.b = b
        self.max_x = max_x
        self.max_var = max_var
        self.used_basises = []
        self.iteration = 0

    def solve(self):
        basis = []
        while(self.iteration == 0 or not optimal):
            basis, optimal = self._step()
            self.iteration += 1
            print("basis:", basis)

        values_for_basis = []
        for item in basis:
            for i in range(len(self.A)):
                if self.A[i][item-1] != 0:
                    values_for_basis.append(self.b[i])
        print("basis_values:", values_for_basis)
        print("count values for x by hands")

    def _step(self):
        basis = self.chooseBasis()
        optimal, column = self.isOptimalBasis()
        if optimal:
            return basis, optimal
        row = self.divideBOnColumn(column)
        self.makeSolveElementPossibleBasis(column, row)
        return basis, False

    def chooseBasis(self):
        if self.used_basises == []:
            basis = []
            for i in range(self.max_x + 1, self.max_var + 1):
                basis.append(i)
            self.used_basises.append(basis)
            return basis
        else:
            possible_basises = []
            element = 0
            for i in range(len(self.A[0])):
                good = True
                count = 0
                for j in range(len(self.A)):
                    if self.A[j][i] != 0:
                        good = False
                        element = self.A[j][i]
                        count += 1
                if count != 1:
                    good = False
                if good:
                    for j in range(len(self.A)):
                        self.A[j][i] /= element
                        self.b[i] /= element
                    possible_basises.append(i)

            if len(possible_basises) == self.max_var - self.max_x and possible_basises not in self.used_basises:
                self.used_basises.append(possible_basises)
                return possible_basises
            return possible_basises

    def isOptimalBasis(self):
        min_item = self.A[-1][0]
        column = -1
        for i, item in enumerate(self.A[-1]):
            min_item = min(min_item, item)
            if min_item > item:
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
        for i in range(len(self.A)):
            if i != row:
                self.A[i] -= self.A[row] * self.A[i][column]
                self.b[i] -= self.b[row] * self.A[i][column]
