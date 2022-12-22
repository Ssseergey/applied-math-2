class Solver:
    def __init__(self, A, b, type, max_x, max_var, matrix=False, start_basis=None):
        self.A = A
        self.b = b
        self.used_basises = []
        self.iteration = 0
        self.basis = []
        self.type = type
        self.delta = []
        self.start_basis = start_basis
        self.max_x = max_x
        self.max_var = max_var
        self.matrix = matrix

    def solve(self):
        if self.start_basis == None:
            rows = []
            if self.max_var - self.max_x >= len(self.b) - 1:
                self.start_basis = []
                for i in range(self.max_x, self.max_x + min(self.max_var - self.max_x, len(self.b) -1)):
                    self.start_basis.append(i)

                for i in range(len(self.b) - 1):
                    for j in range(len(self.A[0])):
                        if self.A[i][j] != 0 and j not in self.basis and j in self.start_basis:
                            rows.append(i)
                            self.makeSolveElementPossibleBasis(j, i)
                            break
                self.basis = self.start_basis
            else:
                for i in range(len(self.b) - 1):
                    for j in range(len(self.A[0])):
                        if self.A[i][j] != 0 and j not in self.basis:
                            self.basis.append(j)
                            rows.append(i)
                            self.makeSolveElementPossibleBasis(j, i)
                            break

            self.used_basises.append(self.basis.copy())
        else:
            rows = []
            self.basis = self.start_basis
            for i in range(len(self.b) - 1):
                for j in range(len(self.A[0])):
                    if self.A[i][j] != 0 and j not in self.basis and j in self.start_basis:
                        rows.append(i)
                        self.makeSolveElementPossibleBasis(j, i)
                        break

            self.used_basises.append(self.basis.copy())

        while True:
            flag, row = self.isMinusInB()
            if flag:
                max_min_column = self.findMaxMinInRow(row)
                temp = self.basis.copy()
                temp[row] = max_min_column
                if temp not in self.used_basises:
                    self.basis[row] = max_min_column
                    self.used_basises.append(self.basis.copy())
                else:
                    print('HERE')

                self.makeSolveElementPossibleBasis(max_min_column, row)
            else:
                break

        while(self.iteration == 0 or not optimal):
            self.iteration += 1
            optimal = self._step()

        self.values_for_basis = {}
        for item in self.basis:
            for i in range(len(self.A) - 1):
                if self.A[i][item] != 0:
                    self.values_for_basis[str(item)] = self.b[i]

        print("basis_values:", self.values_for_basis)
        # print("function value = ", self.function())
        if self.matrix:
            return self.function(), self.values_for_basis

        # print(self.used_basises)
        return self.function()

    def isMinusInB(self):
        row = -1
        min_val = 0
        for i in range(len(self.b) - 1):
            if min_val > self.b[i]:
                row = i
                min_val = self.b[i]
        return row != -1, row

    def findMaxMinInRow(self, row):
        column = -1
        max_min = 0
        for i in range(len(self.A[row])):
            if max_min > self.A[row][i]:
                column = i
                max_min = self.A[row][i]
        return column

    def _step(self):
        # print("basis = ", self.basis)
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
            # print('HERE')
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
        # print(self.A)

    def countDelta(self):
        self.delta = []
        for i in range(len(self.A[0])):
            sum = 0
            for j in range(len(self.basis)):
                sum += self.A[-1][self.basis[j]] * self.A[j][i]
            sum -= self.A[-1][i]
            self.delta.append(sum)
        # print(self.delta)

    def function(self):
        sum = 0
        for i in range(len(self.A[-1])):
            try:
                sum += self.A[-1][i] * self.values_for_basis[str(i)]
            except:
                pass
        return sum
