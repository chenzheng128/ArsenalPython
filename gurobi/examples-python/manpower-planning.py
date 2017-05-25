from gurobipy import *

# tested with
#  Python 2.7.13 :: Anaconda 4.3.1 (x86_64) Gurobi 7.0.2
#  Python 3.5.2 & Gurobi 7.0.1

years = tuplelist(range(2+1))
skill_levels = [0, 1, 2]  # 0 = Unskilled, 1 = Semiskilled, 2 = Skilled
Unskilled = 0
Semiskilled = 1
Skilled = 2

CurrentStrength = [2000, 1500, 1000]
Requirement = [[1000, 1400, 1000],
               [500, 2000, 1500],
               [0, 2500, 2000]]
LeaveFirstYear = [0.25, 0.20, 0.10]
LeaveEachYear = [0.10, 0.05, 0.05]
ContinueFirstYear = [1 - a for a in LeaveFirstYear]
ContinueEachYear = [1 - a for a in LeaveEachYear]
LeaveDownGraded = 0.50
ContinueDownGraded = 1 - LeaveDownGraded
MaxRecruit = [500, 800, 500]
MaxRetrainUnskilled = 200
MaxOverManning = 150
MaxShortTimeWorking = 50
RetrainSemiSkilled = 0.25
ShortTimeUsage = 0.50

RetrainCost = [400, 500, 0]
RedundantCost = [200, 500, 500]
ShortTimeCost = [500, 400, 400]
OverManningCost = [1500, 2000, 3000]

MaxRecruit2 = {(level, year) : MaxRecruit[level] for level in skill_levels for year in years}

model = Model('Manpower planning')

Recruit = model.addVars(skill_levels, years, ub= MaxRecruit2, name="Recruit")
ShortTime = model.addVars(skill_levels, years, ub=MaxShortTimeWorking,
                          name="ShortTime")
LaborForce = model.addVars(skill_levels, years, name="LaborForce")
Redundant = model.addVars(skill_levels, years, name="Redundant")
OverManned = model.addVars(skill_levels, years, name="OverManned")
Retrain = model.addVars(skill_levels, skill_levels, years, name="Retrain")

# Continuity
model.addConstrs(
    (LaborForce[level, year] + Redundant[level, year]
    - ContinueFirstYear[level] * Recruit[level, year]
    + quicksum(Retrain[level, level2, year]
               - ContinueEachYear[level] * Retrain[level2, level, year]
               for level2 in skill_levels if level2 < level)
    + quicksum(Retrain[level, level2, year]
               - 0.5 * Retrain[level2, level, year]
               for level2 in skill_levels if level2 > level)
    == ContinueEachYear[level] * (
        CurrentStrength[level] if year == years[0]
        else LaborForce[level, years[years.index(year)-1]])
    for year in years
    for level in skill_levels),
    "Continuity")


# RetainMaxUnskilled
model.addConstrs(
    (Retrain[Unskilled, Semiskilled, year] <= MaxRetrainUnskilled
    for year in years), "RetrainMaxUnskilled")
model.addConstrs(
    (Retrain[Unskilled, Skilled, year] <= 0
    for year in years), "ForbidRetrainUnskilledToSkilled")

# RetrainingSemiSkilled
model.addConstrs(
    (Retrain[Semiskilled, Skilled, year] <=
     RetrainSemiSkilled * LaborForce[Skilled, year]
    for year in years), "RetrainingSemiSkilled")

# Overmanning
model.addConstrs(
    (OverManned.sum('*', year) <= MaxOverManning for year in years),
    "Overmanning")

# Requirements
model.addConstrs(
    (LaborForce[level, year] ==
     Requirement[year][level] +
     OverManned[level, year] +
     ShortTimeUsage * ShortTime[level, year]
    for year in years
    for level in skill_levels), "Requirements")



# Minimize TotalRedundantMen
obj = Redundant.sum()


# # Minimize TotalCost
# obj = quicksum(
#     RetrainCost[level]*(Retrain[level, level+1, year] if level < 2 else 0)
#     + RedundantCost[level] * Redundant[level, year]
#     + ShortTimeCost[level] * ShortTime[level, year]
#     + OverManningCost[level] * OverManned[level, year]
#     for year in years
#     for level in skill_levels)

model.setObjective(obj)
model.optimize()


# Display solution (print the name of each variable and the solution value)
for v in model.getVars():
    if v.X != 0:
        print("%s %f" % (v.Varname, v.X))
