from pulp import *

# getting the contracts
with open('hw1-03.txt') as f:
    contracts = [tuple(map(int, i.split(' '))) for i in f]

# creating the LpVariables for the number of representatives
representatives = [LpVariable("{}".format(i+1.0), lowBound=0) for i in range(69)]

# creating the LpProblem
prob = LpProblem("Contracts_Problem", LpMinimize)

# adding the objective
prob += sum(representatives)

# adding the constraints
for i in contracts:
    prob += representatives[i[0]-1] + representatives[i[1]-1] >= 2

# solving the constraints
status = prob.solve(PULP_CBC_CMD(msg=False))

# output
c = 0
for i in range(69):
    print(f"representatives from company {i+1}: {value(representatives[i])}")
    c += value(representatives[i])

print(f"Total number of representatives involved: {int(c)}")

"""
representatives from company 1: 1.0
representatives from company 2: 1.0
representatives from company 3: 1.0
representatives from company 4: 2.0
representatives from company 5: 1.0
representatives from company 6: 1.0
representatives from company 7: 1.0
representatives from company 8: 1.0
representatives from company 9: 1.0
representatives from company 10: 1.0
representatives from company 11: 1.0
representatives from company 12: 1.0
representatives from company 13: 1.0
representatives from company 14: 0.0
representatives from company 15: 1.0
representatives from company 16: 1.0
representatives from company 17: 1.0
representatives from company 18: 1.0
representatives from company 19: 1.0
representatives from company 20: 1.0
representatives from company 21: 1.0
representatives from company 22: 1.0
representatives from company 23: 1.0
representatives from company 24: 0.0
representatives from company 25: 1.0
representatives from company 26: 1.0
representatives from company 27: 1.0
representatives from company 28: 1.0
representatives from company 29: 1.0
representatives from company 30: 1.0
representatives from company 31: 1.0
representatives from company 32: 1.0
representatives from company 33: 1.0
representatives from company 34: 0.0
representatives from company 35: 1.0
representatives from company 36: 1.0
representatives from company 37: 1.0
representatives from company 38: 1.0
representatives from company 39: 1.0
representatives from company 40: 1.0
representatives from company 41: 1.0
representatives from company 42: 1.0
representatives from company 43: 1.0
representatives from company 44: 0.0
representatives from company 45: 1.0
representatives from company 46: 1.0
representatives from company 47: 1.0
representatives from company 48: 1.0
representatives from company 49: 1.0
representatives from company 50: 1.0
representatives from company 51: 1.0
representatives from company 52: 1.0
representatives from company 53: 1.0
representatives from company 54: 0.0
representatives from company 55: 1.0
representatives from company 56: 1.0
representatives from company 57: 1.0
representatives from company 58: 1.0
representatives from company 59: 1.0
representatives from company 60: 1.0
representatives from company 61: 1.0
representatives from company 62: 1.0
representatives from company 63: 1.0
representatives from company 64: 0.0
representatives from company 65: 0.0
representatives from company 66: 0.0
representatives from company 67: 0.0
representatives from company 68: 0.0
representatives from company 69: 2.0
Total number of representatives involved: 61
"""
