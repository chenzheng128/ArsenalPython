from gurobipy import *

# tested with Python 3.5.2 & Gurobi 7.0.1

crude_numbers = range(1,2+1)
petrols = ["Premium_fuel", "Regular_fuel"]
end_product_names = ["Premium_fuel", "Regular_fuel", "Jet_fuel", "Fuel_oil", "Lube_oil"]
distillation_products_names = ["Light_naphtha", "Medium_naphtha", "Heavy_naphtha", "Light_oil", "Heavy_oil", "Residuum"]
naphthas = ["Light_naphtha", "Medium_naphtha", "Heavy_naphtha"]
intermediate_oils = ["Light_oil", "Heavy_oil"]
cracking_products_names = ["Cracked_gasoline", "Cracked_oil"]
used_for_motor_fuel_names = ["Light_naphtha", "Medium_naphtha", "Heavy_naphtha", "Reformed_gasoline", "Cracked_gasoline"]
used_for_jet_fuel_names = ["Light_oil", "Heavy_oil", "Residuum", "Cracked_oil"]

crude_bounds = {1:20000, 2:30000}
lb_lube_oil = 500
ub_lube_oil = 1000

max_crude = 45000
max_reform = 10000
max_cracking = 8000

distillation_splitting_coefficients = {"Light_naphtha": (0.1, 0.15),
                          "Medium_naphtha": (0.2, 0.25),
                         "Heavy_naphtha": (0.2, 0.18),
                         "Light_oil": (0.12, 0.08),
                         "Heavy_oil": (0.2, 0.19),
                         "Residuum": (0.13, 0.12)}

cracking_splitting_coefficients = {("Light_oil","Cracked_oil"): 0.68,
                                   ("Heavy_oil","Cracked_oil"): 0.75,
                                   ("Light_oil","Cracked_gasoline"): 0.28,
                                   ("Heavy_oil","Cracked_gasoline"): 0.2}

reforming_splitting_coefficients = {"Light_naphtha": 0.6, "Medium_naphtha":0.52, "Heavy_naphtha":0.45}
end_product_profit = {"Premium_fuel":7, "Regular_fuel":6, "Jet_fuel":4, "Fuel_oil":3.5, "Lube_oil":1.5}
blending_coefficients = {"Light_oil": 0.55, "Heavy_oil": 0.17, "Cracked_oil": 0.22, "Residuum": 0.055}

lube_oil_factor = 0.5
pmf_rmf_ratio = 0.4

octance_number_coefficients = {
    "Light_naphtha":90,
    "Medium_naphtha":80,
    "Heavy_naphtha":70,
    "Reformed_gasoline":115,
    "Cracked_gasoline":105,
}
octance_number_fuel = {"Premium_fuel": 94,"Regular_fuel": 84}

vapor_pressure_constants = [0.6, 1.5, 0.05]


model = Model('Refinery_Optimization')

# Variables
crudes = model.addVars(crude_numbers, ub=crude_bounds, name="cr")
end_products = model.addVars(end_product_names, name="end_prod")
end_products["Lube_oil"].lb= lb_lube_oil
end_products["Lube_oil"].ub= ub_lube_oil
distillation_products = model.addVars(distillation_products_names, name="dist_prod")
reform_usage = model.addVars(naphthas, name="napthas_to_reformed_gasoline")
reformed_gasoline = model.addVar(name="reformed_gasoline")
cracking_usage = model.addVars(intermediate_oils,name="intermediate_oils_to_cracked_gasoline")
cracking_products = model.addVars(cracking_products_names,  name="cracking_prods")
used_for_regular_motor_fuel = model.addVars(used_for_motor_fuel_names, name="motor_fuel_to_regular_motor_fuel")
used_for_premium_motor_fuel = model.addVars(used_for_motor_fuel_names, name="motot_fuel_to_premium_motor_fuel")
used_for_jet_fuel = model.addVars(used_for_jet_fuel_names, name="jet_fuel")
used_for_lube_oil = model.addVar(vtype=GRB.CONTINUOUS,name="residuum_used_for_lube_oil")

# Constraints

# Max Crude
model.addConstr(crudes.sum() <= max_crude, "max_crude")

# Reforming Capacity
model.addConstr(reform_usage.sum() <= max_reform, "max_reform")
model.addConstr(cracking_usage.sum() <= max_cracking, "max_cracking")


# Splitting
model.addConstrs((quicksum(distillation_splitting_coefficients[dpn][crude-1]*crudes[crude] for crude in crudes) ==
                    distillation_products[dpn] for dpn in distillation_products_names),
                    "splitting_distillation")

# Reforming
model.addConstr(reform_usage.prod(reforming_splitting_coefficients) == reformed_gasoline,
                    "splitting_reforming")

# Cracking
model.addConstrs((quicksum(cracking_splitting_coefficients[oil, crack_prod]*cracking_usage[oil] for oil in intermediate_oils) ==
                    cracking_products[crack_prod] for crack_prod in cracking_products_names),
                    name="splitting_cracking")

# Continuity
model.addConstrs((reform_usage[naphtha] +
                    used_for_regular_motor_fuel[naphtha] +
                    used_for_premium_motor_fuel[naphtha] ==
                    distillation_products[naphtha] for naphtha in naphthas), "continuity")


model.addConstr(used_for_regular_motor_fuel["Cracked_gasoline"] +
                used_for_premium_motor_fuel["Cracked_gasoline"] ==
                cracking_products["Cracked_gasoline"], "continuity_cracked_gasoline")

model.addConstr(used_for_regular_motor_fuel["Reformed_gasoline"] +
                used_for_premium_motor_fuel["Reformed_gasoline"] ==
                reformed_gasoline, "continuity_reformed_gasoline")

model.addConstr(used_for_premium_motor_fuel.sum() == end_products["Premium_fuel"], "continuity_premium_fuel")

model.addConstr(used_for_regular_motor_fuel.sum() == end_products["Regular_fuel"], "continuity_regular_fuel")

model.addConstr(used_for_jet_fuel.sum() == end_products["Jet_fuel"], "continuity_jet_fuel")

# Blending

model.addConstr(cracking_usage["Light_oil"]+
                used_for_jet_fuel["Light_oil"]+
                blending_coefficients["Light_oil"]*end_products["Fuel_oil"] ==
                distillation_products["Light_oil"], "fixed_proportion_light_oil_for_blending")

model.addConstr(cracking_usage["Heavy_oil"]+
                used_for_jet_fuel["Heavy_oil"]+
                blending_coefficients["Heavy_oil"]*end_products["Fuel_oil"] ==
                distillation_products["Heavy_oil"], "fixed_proportion_heavy_oil_for_blending")

model.addConstr(used_for_jet_fuel["Cracked_oil"]+
                blending_coefficients["Cracked_oil"]*end_products["Fuel_oil"] ==
                cracking_products["Cracked_oil"], "fixed_proportion_cracked_oil_for_blending")

model.addConstr(used_for_lube_oil +
                used_for_jet_fuel["Residuum"]+
                blending_coefficients["Residuum"]*end_products["Fuel_oil"] ==
                distillation_products["Residuum"], "fixed_proportion_residuum_for_blending")



#  lube-oil is 0.5 of residuum used
model.addConstr(lube_oil_factor*used_for_lube_oil == end_products["Lube_oil"],"lube-oil_is_0.5_of_residuum_used")

# pmf/rmf must be 40%
model.addConstr(end_products["Premium_fuel"] >= pmf_rmf_ratio*end_products["Regular_fuel"], "pmf/rmf_must_be_40%")


# octane numbers
model.addConstr(used_for_regular_motor_fuel.prod(octance_number_coefficients) >=
                octance_number_fuel["Regular_fuel"] * end_products["Regular_fuel"],
                "Octane_number_regular_fuel")

model.addConstr(used_for_premium_motor_fuel.prod(octance_number_coefficients) >=
                octance_number_fuel["Premium_fuel"] * end_products["Premium_fuel"],
                "Octane_number_premium_fuel")

# Vapour pressure
model.addConstr(used_for_jet_fuel["Light_oil"] + 
                vapor_pressure_constants[0]*used_for_jet_fuel["Heavy_oil"] + 
                vapor_pressure_constants[1]*used_for_jet_fuel["Cracked_oil"] + 
                vapor_pressure_constants[2]*used_for_jet_fuel["Residuum"] <= end_products["Jet_fuel"],"vapour_pressure")

# Profit
model.setObjective(end_products.prod(end_product_profit), GRB.MAXIMIZE)

model.optimize()


# Display solution (print the name of each variable and the solution value)
for v in model.getVars():
    if v.X != 0:
        print("%s %f" % (v.Varname, v.X))
