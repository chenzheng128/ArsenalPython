from gurobipy import *

# Example data for problem
cost = [100, 100, 100, 100, 200, 200];
value = [50, 150, 150, 150, 300, 50];
edges = [[4,0], [4,1], [4,2], [5,1], [5,2], [5,3]];

m = Model()
n = len(cost) # number of blocks

# Indicator variable for each block
x = {}
for i in range(n):
   x[i] = m.addVar(vtype=GRB.BINARY, name="x%d" % i)

m.update()

# Set objective
m.setObjective(quicksum((value[i] - cost[i])*x[i] for i in range(n)), GRB.MAXIMIZE)

# Add constraints
for edge in edges:
   u = edge[0]
   v = edge[1]
   m.addConstr(x[u] <= x[v])

m.optimize()

for v in m.getVars():
    if v.X != 0:
        print("%s %f" % (v.Varname, v.X))
