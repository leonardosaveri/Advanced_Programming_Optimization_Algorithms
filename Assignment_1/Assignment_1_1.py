from pulp import *

# creating variables and constraints
x = LpVariable("x", lowBound=-10)
y = LpVariable("y", upBound=10)

# creating the minimization LP problem
prob = LpProblem("myProblem", LpMinimize)

# setting the constraints
prob += (3*x + 2*y <= 10, "1")
prob += (12*x + 14*y >= -12.5, "2")
prob += (2*x + 3*y >= 3, "3")
prob += (5*x - 6*y >= -100, "4")
prob += 122*x + 143*y

# To check constraints and problem
# print(prob)

# solving the problem
status = prob.solve(PULP_CBC_CMD(msg=False))

# output
print(f"Optimal solution: x = {value(x)} y = {value(y)}")
print(f"Objective value: {value(prob.objective)}")
print(f"Tight constraints:")
for name, constraint in prob.constraints.items():
    if constraint.value():
        print(name)

x1 = value(x)
y1 = value(y)

# to check if optimal solution is unique
prob += (122*x + 143*y == -122.0, "5")
prob += x + y

status1 = prob.solve(PULP_CBC_CMD(msg=False))
print(f"Unique optimal solution: {'YES' if x1 == value(x) and y1 == value(y) else 'NO'}")

# Optimal solution: x = -9.9375 y = 7.625
# Objective value: -122.0
# Tight constraints:
# 1
# 4
# Unique optimal solution: YES
