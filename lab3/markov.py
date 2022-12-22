import numpy as np

class Markov:
    def __init__(self, P, S):
        self.P = np.array(P)
        self.S_start = np.array(S)
        self.S = np.array(S)

    def step(self):
        return self.S @ self.P

    def compute(self, eps):
        diff = []
        while(True):
            S_next = self.step()
            norm = np.linalg.norm(self.S - S_next)
            if norm < eps:
                break
            self.S = S_next
            diff.append(norm)
        return self.S, diff

    def createLineralProblem(self):
        with open("tests/test1", 'w') as f:
            print("max", file=f)
            print("f = ", end='', file=f)
            for i in range(len(self.P)):
                print("x", i+1, end=' ', sep='', file=f)
            print(file=f)

            for j in range(len(self.P) - 1):
                for i in range(len(self.P)):
                    if self.P[i][j] == 0. and i != j:
                        continue
                    elif i == j:
                        print(self.P[i][j] - 1, "x", i+1, end=' ', sep='', file=f)
                    else:
                        print(self.P[i][j], "x", i+1, end=' ', sep='', file=f)
                print("= 0", file=f)

            for i in range(len(self.P)):
                print("x", i+1, end=' ', sep='', file=f)
            print("= 1", file=f)
