import datalib as dl
import solver

from colorama import Fore, Style

data = dl.PrepareData()
data.readTest("tests/test4")
data.print()

tests = {
    # "example":-13,
    # "test1":  -6.5,
    # "test2":  -6,
    # "test3":  -11,
    # "test4":   10,
    "test5":1,
    # "test6":1,
    # "test7":1,
    # "test8":1,
    # "test9":1,
    # "test10":1,
}

for test, value in tests.items():
    data.readTest("tests/" + test)
    worker = solver.Solver(data.A, data.b, data.type)
    result = worker.solve()
    if result == value:
        print(Fore.GREEN + test + " Passed!")
    else:
        print(Fore.RED + test + " Failed!")
    print(Style.RESET_ALL)
