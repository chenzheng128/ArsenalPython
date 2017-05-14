from gurobipy import *

# tested with Python 3.5.2 & Gurobi 7.0.1

time_periods = ["January", "February", "March", "April", "May", "June"]

oils = ["VEG1", "VEG2", "OIL1", "OIL2", "OIL3"]

prices = tupledict({
	('January', 'VEG1'): 110,
	('January', 'VEG2'): 120,
	('January', 'OIL1'): 130,
	('January', 'OIL2'): 110,
	('January', 'OIL3'): 115,
	('February', 'VEG1'): 130,
	('February', 'VEG2'): 130,
	('February', 'OIL1'): 110,
	('February', 'OIL2'): 90,
	('February', 'OIL3'): 115,
	('March', 'VEG1'): 110,
	('March', 'VEG2'): 140,
	('March', 'OIL1'): 130,
	('March', 'OIL2'): 100,
	('March', 'OIL3'): 95,
	('April', 'VEG1'): 120,
	('April', 'VEG2'): 110,
	('April', 'OIL1'): 120,
	('April', 'OIL2'): 120,
	('April', 'OIL3'): 125,
	('May', 'VEG1'): 100,
	('May', 'VEG2'): 120,
	('May', 'OIL1'): 150,
	('May', 'OIL2'): 110,
	('May', 'OIL3'): 105,
	('June', 'VEG1'): 90,
	('June', 'VEG2'): 100,
	('June', 'OIL1'): 140,
	('June', 'OIL2'): 80,
	('June', 'OIL3'): 135
})


hardness = {"VEG1": 8.8, "VEG2": 6.1, "OIL1": 2.0, "OIL2": 4.2, "OIL3": 5.0}

price = 150
IStore = 500
vegCapa = 200
oilCapa = 250

hardness_lb = 3
hardness_ub = 6
store_pricing = 5

model = Model('Food Manufacture I')

 # Quantity of food produced in each period
food = model.addVars(time_periods, name = "Food")
# Quantity bought of each product in each period
buy = model.addVars(time_periods, oils, name = "Buy")
# Quantity used of each product  in each period
use = model.addVars(time_periods, oils, name = "Use")
# Quantity stored of each product  in each period
store = model.addVars(time_periods, oils, name = "Store")


#Initial Balance
model.addConstrs((IStore + buy[time_periods[0], oil] ==
     use[time_periods[0], oil] + store[time_periods[0], oil] for oil in oils), "Initial_Balance")

#Balance
model.addConstrs(
	(store[time_periods[time_periods.index(time_period)-1], oil] + buy[time_period, oil] ==
     use[time_period, oil] + store[time_period, oil]
     for oil in oils for time_period in time_periods if time_period != time_periods[0]), "Balance")

#End Store
model.addConstrs((store[time_periods[-1], oil] == IStore for oil in oils),
				 "End_Balance")

# Capacity1 & Capacity2
model.addConstrs(
	(quicksum(use[time_period, oil] for oil in oils if "VEG" in oil) <= vegCapa
	 for time_period in time_periods), "Capacity_Veg")
model.addConstrs(
	(quicksum(use[time_period, oil] for oil in oils if "OIL" in oil) <= oilCapa
	 for time_period in time_periods), "Capacity_Oil")

# Hardness
model.addConstrs(
	(quicksum(hardness[oil] * use[time_period, oil] for oil in oils)
	 >= hardness_lb * food[time_period] for time_period in time_periods),
	"Hardness_lower")
model.addConstrs(
	(quicksum(hardness[oil] * use[time_period, oil] for oil in oils)
	 <= hardness_ub * food[time_period] for time_period in time_periods),
	"Hardness_upper")

# Conserve
model.addConstrs((use.sum(time_period) == food[time_period]
				  for time_period in time_periods), "Conserve")

# Objective
obj = price*food.sum() - buy.prod(prices) - store_pricing*store.sum()
model.setObjective(obj, GRB.MAXIMIZE) # maximize profit

model.optimize()


# Display solution (print the name of each variable and the solution value)
for v in model.getVars():
    if v.X != 0:
        print("%s %f" % (v.Varname, v.X))
