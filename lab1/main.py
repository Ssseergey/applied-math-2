import datalib as dl
import solver

data = dl.PrepareData()
data.readTest("tests/example")
data.print()

worker = solver.Solver(data.A, data.b, data.max_x, data.max_var)
worker.solve()