import datalib as dl
import solver
from colorama import Fore, Style

data = dl.PrepareData()

# "example":-13,

tests = {
    "test1": -6.5,
    "test2": -6,
    "test3": -11,
    "test4": -10,
    "test5": -4,
    "test6": -3,
    "test7":  10,
}

for test, value in tests.items():
    data.readTest("tests/" + test)
    worker = solver.Solver(data.A, data.b, data.type)
    result = worker.solve()
    if round(result, 2) == value:
        print(Fore.GREEN + test + " Passed!")
    else:
        print(Fore.RED + test + " Failed!")
    print(Style.RESET_ALL)
