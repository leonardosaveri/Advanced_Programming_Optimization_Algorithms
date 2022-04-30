from pulp import *

"""
payOffMatrix = [[0, -2, 1, 1, 1, 1],
                [2, 0, -2, 1, 1, 1],
                [-1, 2, 0, -2, 1, 1],
                [-1, -1, 2, 0, -2, 1],
                [-1, -1, -1, 2, 0, -2],
                [-1, -1, -1, -1, 2, 0]
                ]
"""

# creating the LpVariables
x = LpVariable("x")
x1 = LpVariable("x1", 0, 1)
x2 = LpVariable("x2", 0, 1)
x3 = LpVariable("x3", 0, 1)
x4 = LpVariable("x4", 0, 1)
x5 = LpVariable("x5", 0, 1)
x6 = LpVariable("x6", 0, 1)

# creating the problem
prob = LpProblem("Random_Number", LpMaximize)

# adding the constraints
prob += x1+x2+x3+x4+x5+x6 == 1, "P"
prob += 0*x1 - 2*x2 + x3 + x4 + x5 + x6 >= x, "1"
prob += 2*x1 + 0*x2 - 2*x3 + x4 + x5 + x6 >= x, "2"
prob += -1*x1 + 2*x2 + 0*x3 - 2*x4 + x5 + x6 >= x, "3"
prob += -1*x1 - 1*x2 + 2*x3 + 0*x4 - 2*x5 + x6 >= x, "4"
prob += -1*x1 - 1*x2 - 1*x3 + 2*x4 + 0*x5 - 2*x6 >= x, "5"
prob += -1*x1 - 1*x2 - 1*x3 + -1*x4 + 2*x5 + 0*x6 >= x, "6"

# the objective
prob += x

# solving the linear programming
status = prob.solve(PULP_CBC_CMD(msg=False))

# output
print(f"x1: {value(x1)} x2: {value(x2)} x3: {value(x3)} x4: {value(x4)} x5: {value(x5)} x6: {value(x6)}")
# x1: 0.0 x2: 0.0625 x3: 0.3125 x4: 0.25 x5: 0.3125 x6: 0.0625
