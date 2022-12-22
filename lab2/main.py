import datalib as dl
import solver
from colorama import Fore, Style

def countPossibilities(game_cost, values):
    pi = []
    for i in range(len(values)):
        try:
            # print("P[", i, "] = ", game_cost * values[str(i)])
            pi.append(game_cost * values[str(i)])
        except:
            # print("P[", i, "] = ", 0)
            pi.append(0)

    return pi

def countM(A, P, Q):
    M = 0
    for i in range(len(A) - 1):
        for j in range(len(P)):
            try:
                M += A[i][j] * P[i] * Q[j]
            except:
                pass
    return M


data = dl.PrepareData()


lineral_tests = {
    "task2": 298,
    "task3": 480000,
}

matrix_tests = {
    "task4": 0.75,
    "task5": 0.5,
    "task6": 0.28,
}


for test, value in lineral_tests.items():
    data.readTest("tests/" + test)
    worker = solver.Solver(data.A, data.b, data.type, data.max_x, data.max_var, False)
    result = worker.solve()
    if round(result, 2) == value:
        print(Fore.GREEN + test + " Passed!")
    else:
        print(Fore.RED + test + " Failed!")
    print(Style.RESET_ALL)


for test, value in matrix_tests.items():
    data.readTest("tests/" + test + "1")
    worker = solver.Solver(data.A, data.b, data.type, data.max_x, data.max_var, True)
    resultPlayer1, valuesPlayer1 = worker.solve()

    data.readTest("tests/" + test + "2")
    worker = solver.Solver(data.A, data.b, data.type, data.max_x, data.max_var, True)
    result, valuesPlayer2 = worker.solve()

    P = countPossibilities(1 / resultPlayer1, valuesPlayer2)
    Q = countPossibilities(1 / resultPlayer1, valuesPlayer1)
    print("Possibilities for player1 = ", P)
    print("Possibilities for player2 = ", Q)

    M = countM(data.A, P, Q)
    print("M = ", M)

    if round(result, 2) == value:
        print(Fore.GREEN + test + " Passed!")
    else:
        print(Fore.RED + test + " Failed!")
    print(Style.RESET_ALL)
