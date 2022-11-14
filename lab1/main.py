import datalib as dl
import solver

data = dl.PrepareData()
data.readTest("tests/test1")
data.print()

worker = solver.Solver(data.A, data.b)
worker.solve()