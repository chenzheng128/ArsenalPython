from gurobipy import *

# tested with
#  Python 2.7.13 :: Anaconda 4.3.1 (x86_64) Gurobi 7.0.2
#  Python 3.5.2 & Gurobi 7.0.1

mines = range(3+1)
years = range(4+1)

Royalties = [5e6, 4e6, 4e6, 5e6]
ExtractLimit = [2e6, 2.5e6, 1.3e6, 3e6]
OreQuality  = [1, .7, 1.5, .5]
BlendedQuality = [0.9, 0.8, 1.2, 0.6, 1.0]
discount = [(1/(1+1/10.0)) ** year for year in years]

mines_limit = 3
sell_price = 10

model = Model('Mining')

out = model.addVars(mines, years, name="output")
quan = model.addVars(years, name="quantity")
work = model.addVars(mines, years, vtype=GRB.BINARY, name="working")
open = model.addVars(mines, years, vtype=GRB.BINARY, name="open")

# At most three mines open
model.addConstrs((work.sum('*',year) <= mines_limit for year in years),"AtMost3Mines")

# Maintain Quality
model.addConstrs(
    (quicksum(OreQuality[mine]*out[mine, year] for mine in mines) == BlendedQuality[year]*quan[year]
     for year in years), "Quality")

# Quantity produced equals output
model.addConstrs((out.sum('*',year) == quan[year] for year in years), "OutQty")

# Restrict ExtractLimit
#Modeled as described in the HP Williams book
#model.addConstrs(
#    (out[mine, year] <= ExtractLimit[mine]*work[mine, year]
#     for mine, year in out), "ExtractLimit")
#Modeled using Gurobi General Constraints
for year in years:
    for mine in mines:
        out[mine, year].ub= ExtractLimit[mine]
        model. addGenConstrIndicator(work[mine, year], 0, out[mine, year] == 0, name="ExtractLimit" )

# Mine Working => Mine Open
#Modeled as described in the HP Williams book
#model.addConstrs(
#    (work[mine, year] <= open[mine, year] for mine, year in open), "WorkingOpen")

#Modeled using Gurobi General Constraints
for year in years:
    for mine in mines:
        model. addGenConstrIndicator(work[mine, year], 1, open[mine, year] == 1, name="ExtractLimit" )

# Mine Open in Year+1 => Mine was also open in Year
#Modeled as described in the HP Williams book
#model.addConstrs(
#    (open[mine, year+1] <= open[mine, year]
#     for mine, year in open if year < years[-1]), "SubsequentOpen")
#Modeled using Gurobi General Constraints
years2 = (year for year in years if year < years[-1])
for year in years2:
    for mine in mines:
        model. addGenConstrIndicator(open[mine, year + 1], 1, open[mine, year] == 1, name="SubsequentOpen" )

# Maximize Profit
obj = quicksum(sell_price*discount[year]*quan[year] for year in years) \
      - quicksum(Royalties[mine] * discount[year] * open[mine, year]
                 for mine, year in open)

model.setObjective(obj, GRB.MAXIMIZE)

model.optimize()

# Display solution (print the name of each variable and the solution value)
for v in model.getVars():
    if v.X != 0:
        print("%s %f" % (v.Varname, v.X))
