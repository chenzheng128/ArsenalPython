from gurobipy import *

# tested with
#  Python 2.7.13 :: Anaconda 4.3.1 (x86_64) Gurobi 7.0.2
#  Python 3.5.2 & Gurobi 7.0.1

products = ["Prod1", "Prod2", "Prod3", "Prod4", "Prod5", "Prod6", "Prod7"]
machines = ["grinder", "vertDrill", "horiDrill", "borer", "planer"]
time_periods = ["January", "February", "March", "April", "May", "June"]

profit_contribution = {"Prod1":10, "Prod2":6, "Prod3":8, "Prod4":4, "Prod5":11, "Prod6":9, "Prod7":3}

time_table = {
    "grinder": {    "Prod1": 0.5, "Prod2": 0.7, "Prod5": 0.3,
                    "Prod6": 0.2, "Prod7": 0.5 },
    "vertDrill": {  "Prod1": 0.1, "Prod2": 0.2, "Prod4": 0.3,
                    "Prod6": 0.6 },
    "horiDrill": {  "Prod1": 0.2, "Prod3": 0.8, "Prod7": 0.6 },
    "borer": {      "Prod1": 0.05,"Prod2": 0.03,"Prod4": 0.07,
                    "Prod5": 0.1, "Prod7": 0.08 },
    "planer": {     "Prod3": 0.01,"Prod5": 0.05,"Prod7": 0.05 }
}


# number of machines down
down = {("January","grinder"): 1, ("February", "horiDrill"): 2, ("March", "borer"): 1,
        ("April", "vertDrill"): 1, ("May", "grinder"): 1, ("May", "vertDrill"): 1,
        ("June", "planer"): 1, ("June", "horiDrill"): 1}

qMachine = {"grinder":4, "vertDrill":2, "horiDrill":3, "borer":1, "planer":1} # number of each machine available
qMaintenance = {"grinder":2, "vertDrill":2, "horiDrill":3, "borer":1, "planer":1} # number of machines that need to be under maintenance

# market limitation of sells
upper = {
    ("January", "Prod1") : 500,
    ("January", "Prod2") : 1000,
    ("January", "Prod3") : 300,
    ("January", "Prod4") : 300,
    ("January", "Prod5") : 800,
    ("January", "Prod6") : 200,
    ("January", "Prod7") : 100,
    ("February", "Prod1") : 600,
    ("February", "Prod2") : 500,
    ("February", "Prod3") : 200,
    ("February", "Prod4") : 0,
    ("February", "Prod5") : 400,
    ("February", "Prod6") : 300,
    ("February", "Prod7") : 150,
    ("March", "Prod1") : 300,
    ("March", "Prod2") : 600,
    ("March", "Prod3") : 0,
    ("March", "Prod4") : 0,
    ("March", "Prod5") : 500,
    ("March", "Prod6") : 400,
    ("March", "Prod7") : 100,
    ("April", "Prod1") : 200,
    ("April", "Prod2") : 300,
    ("April", "Prod3") : 400,
    ("April", "Prod4") : 500,
    ("April", "Prod5") : 200,
    ("April", "Prod6") : 0,
    ("April", "Prod7") : 100,
    ("May", "Prod1") : 0,
    ("May", "Prod2") : 100,
    ("May", "Prod3") : 500,
    ("May", "Prod4") : 100,
    ("May", "Prod5") : 1000,
    ("May", "Prod6") : 300,
    ("May", "Prod7") : 0,
    ("June", "Prod1") : 500,
    ("June", "Prod2") : 500,
    ("June", "Prod3") : 100,
    ("June", "Prod4") : 300,
    ("June", "Prod5") : 1100,
    ("June", "Prod6") : 500,
    ("June", "Prod7") : 60,
}


storeCost = 0.5
storeCapacity = 100
endStock = 50
hoursPerMonth = 2*8*24

model = Model('Factory Planning II')


manu = model.addVars(time_periods, products, name="Manu") # quantity manufactured
held = model.addVars(time_periods, products, ub=storeCapacity, name="Held") # quantity stored
sell = model.addVars(time_periods, products, ub=upper, name="Sell") # quantity sold
d = model.addVars(time_periods, machines,vtype=GRB.INTEGER, name="d") # number of machines down



#Initial Balance
model.addConstrs((manu[time_periods[0], product] == sell[time_periods[0], product]
                  + held[time_periods[0], product] for product in products), name="Initial_Balance")

#Balance
model.addConstrs((held[time_periods[time_periods.index(time_period) -1], product] + manu[time_period, product] ==
                    sell[time_period, product] + held[time_period, product]
                    for product in products for time_period in time_periods if time_period != time_periods[0]), name="Balance")

#End store
model.addConstrs((held[time_periods[-1], product] == endStock for product in products),  name="End_Balance")


#Capacity
model.addConstrs((quicksum(time_table[machine][product] * manu[time_period, product] for product in time_table[machine])
                            <= hoursPerMonth * (qMachine[machine] - d[time_period, machine])
                            for machine in machines for time_period in time_periods), name = "Capacity")
#Maintenance
model.addConstrs((d.sum('*', machine) == qMaintenance[machine] for machine in machines), "Maintenance")



#Objective
obj = quicksum(profit_contribution[product] * sell[time_period, product] -  storeCost * held[time_period, product]  for time_period in time_periods
                    for product in products)

model.setObjective(obj, GRB.MAXIMIZE)


model.optimize()


# Display solution (print the name of each variable and the solution value)
for v in model.getVars():
    if v.X != 0:
        print("%s %f" % (v.Varname, v.X))
