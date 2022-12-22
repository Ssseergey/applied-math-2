import matplotlib.pyplot as plt
import datalib as dl
import solver
import markov

data = dl.PrepareData()


P = [
#     1     2     3     4     5     6     7     8
    [0.2,  0.5,  0.,   0.,   0.3,  0.,   0.,   0.],
    [0.3,  0.3,  0.4,  0.,   0.,   0.,   0.,   0.],
    [0.,   0.6,  0.2,  0.2,  0.,   0.,   0.,   0.],
    [0.,   0.,   0.,   0.3,  0.,   0.,   0.2,  0.5],
    [0.,   0.,   0.,   0.,   0.5,  0.2,  0.3,  0.],
    [0.,   0.,   0.,   0.,   0.1,  0.6,  0.3,  0.],
    [0.,   0.,   0.4,  0.,   0.,   0.,   0.5,  0.1],
    [0.,   0.,   0.,   0.4,  0.,   0.,   0.,   0.6]
]

S_1 = [
     0.1,  0.2,  0.2,  0.1,  0.1,  0.1,  0.1,  0.1
]

S_2 = [
     0.1,  0.1,  0.1,  0.1,  0.1,  0.1,  0.3,  0.1
]

markovWorker_1 = markov.Markov(P, S_1)
S_result_1, diff_1 = markovWorker_1.compute(0.0000000001)
print("Start possibilities")
print(S_1)
print("Result")
print(S_result_1, len(diff_1))
print()

markovWorker_2 = markov.Markov(P, S_2)
S_result_2, diff_2 = markovWorker_2.compute(0.0000000001)
print("Start possibilities")
print(S_2)
print("Результат")
print(S_result_2, len(diff_2))
print()

markovWorker_1.createLineralProblem()

data.readTest("tests/test1")
worker = solver.Solver(data.A, data.b, data.type, data.max_x, data.max_var, False)
result = worker.solve()

fig = plt.figure("График отклонения от итерации")
plt.ylabel("Отклонение")
plt.xlabel("Номер итерации")
plt.plot(diff_1)

plt.plot(diff_2)
plt.show()