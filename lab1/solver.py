from tracemalloc import start


class Solver:
    def __init__(self, A, b, type, start_basis=None):
        self.A = A
        self.b = b
        self.used_basises = []
        self.iteration = 0
        self.basis = []
        self.type = type
        self.delta = []
        self.start_basis = start_basis

    def solve(self):
        if self.start_basis == None:
            rows = []
            for i in range(len(self.b) - 1):
                for j in range(len(self.A - 1)):
                    if self.A[i][j] != 0 and j not in self.basis:
                        self.basis.append(j)
                        print("i, j I AM BASIS NOW", self.basis)
                        rows.append(i)
                        self.makeSolveElementPossibleBasis(j, i)
                        break

            self.used_basises.append(self.basis.copy())
        else:
            print("IMPLEMENT ME")

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
        return self.function()

    def _step(self):
        print(self.A)
        print(self.b)
        optimal, column = self.isOptimalBasis()
        if optimal:
            return optimal

        row = self.divideBOnColumn(column)
        print("col, row = ", column, row)
        temp = self.basis.copy()
        temp[row] = column
        if temp not in self.used_basises:
            self.basis[row] = column
            self.used_basises.append(self.basis.copy())
        else:
            print('HERE')
            return True

        self.makeSolveElementPossibleBasis(column, row)
        return False

    def isOptimalBasis(self):
        self.countDelta()
        column = 0
        if self.type:
            min_item = self.delta[0]
            for i, item in enumerate(self.delta):
                if item < min_item:
                    min_item = item
                    column = i
            return min_item >= 0, column
        else:
            max_item = self.delta[0]
            for i, item in enumerate(self.delta):
                if item > max_item:
                    max_item = item
                    column = i
            return max_item <= 0, column

    def divideBOnColumn(self, column):
        min_item = None
        row = -1
        for i in range(len(self.A) - 1):
            if self.A[i][column] == 0:
                value = -1
            else:
                value = self.b[i] / self.A[i][column]

            if value >= 0 and (min_item == None or value < min_item):
                min_item = value
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
            # if self.b[i] < 0:
            #     self.b[i] *= -1
            #     self.A[i] *= -1

    def countDelta(self):
        self.delta = []
        for i in range(len(self.A[-1])):
            sum = 0
            for j in range(len(self.basis)):
                sum += self.A[-1][self.basis[j]] * self.A[j][i]
            sum -= self.A[-1][i]
            self.delta.append(sum)

        sum = 0
        for j in range(len(self.basis)):
            sum += self.A[-1][self.basis[j]] * self.b[j]
        sum -= self.b[-1]
        self.delta.append(sum)
        print("DELTAS =", self.delta)

    def function(self):
        sum = 0
        for i in range(len(self.A[-1])):
            try:
                sum += self.A[-1][i] * self.values_for_basis[str(i)]
            except:
                pass
        return sum
