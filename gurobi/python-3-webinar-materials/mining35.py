import sys
import random
import heapq
import math
import time
import argparse
from pandas import DataFrame
import colorama as pycol
from gurobipy import *

lineseparator = '----------------------------------------------------------------------'

def line_distance(x, y, z, Xmax, Ymax, Zmax, La, Lb, Lc):
  '''
  Compute the (minimum L2) distance from (x,y,z) to the line defined by
  (x,y,z) = t*(La, Lb, Lc) +  (Xmax, Ymax, Zmax) / 2
  '''
  x -= Xmax/2
  y -= Ymax/2
  z -= Zmax/2
  norm = (La**2 + Lb**2 + Lc**2) ** 0.5
  if norm >= 1:
    # actual line exists, otherwise use distance to center
    t = (x * La + y * Lb + z * Lc) / norm
    x -= t * La
    y -= t * Lb
    z -= t * Lc
  #normalize distances
  x /= (Xmax / 2)
  y /= (Ymax / 2)
  z /= (Zmax / 2)
  return (x**2 + y**2 + z**2) ** 0.5

def obj_val(x, y, z, Xmax, Ymax, Zmax, La, Lb, Lc):
  '''
  Compute objective value for a given block position; this value
  decreases with the square distance to the `ore line' defined by (x,
  y, z) = t * (La, Lb, Lc) + (Xmax, Ymax, Zmax) / 2 and also linearly
  with the depth of the deposit, plus a uniform random factor of +-
  10%
  '''
  # obj 1 / |dist|
  varObj  = line_distance(x, y, z, Xmax, Ymax, Zmax, La, Lb, Lc)
  varObj += 1
  varObj  = 5.0 / (varObj * varObj);
  # discount on depth
  varObj -= (2.0 - 2.0 * z / Zmax)
  # random factor +- 10%
  varObj *= 0.9 + 0.2 * random.random()
  return varObj

def objpre_process_blocks(model:Model):
  '''
  Eliminate blocks at the bottom of the pit with negative objective
  value.  Once a block is eliminated, we update the precedences (by
  subtracting one) of blocks above him, which may trigger some blocks
  to be at the bottom of the pit (and thus be candidates for
  elimination).
  '''
  nBlocks = len(model._Blocks)
  InDegree = { x : 0 for x in model._Blocks}
  for d in model._Precedences:
    for x in model._Blocks:
      z = (x[0] - d[0], x[1] - d[1], x[2] - d[2])
      if z in model._Blocks:
        InDegree[x] += 1
  h = []
  for x in model._Blocks:
    if InDegree[x] == 0:
      heapq.heappush(h, (model._Obj[x], x))
  while len(h)>0:
    (val, x) = heapq.heappop(h)
    if val > 0:
      break
    model._Blocks.remove(x)
    for d in model._Precedences:
      z = (x[0]+d[0],x[1]+d[1],x[2]+d[2])
      if z in model._Blocks:
        InDegree[z] -= 1
        if InDegree[z] == 0:
          heapq.heappush(h,(model._Obj[z],z))
  newlen = len(model._Blocks)
  if newlen < nBlocks:
    print('Preprocessing removed %d blocks %d vars' % (nBlocks - newlen, model._Tmax * (nBlocks - newlen) ))
  return None

def timepre_process_blocks(model:Model):
  '''
  Compute the minimum `time` required to mine a block; this depend on
  the weight, the precedences, and the knapsack capacity; essentially,
  we compute the weight above any block, and divide it by the knapsack
  capacity; the round down of that number is the earliest time we can
  reach the given block.
  '''
  count = 0
  for x in model._Blocks:
    s=set()
    l=set()
    l.add(x)
    while len(l) > 0:
      y = l.pop()
      s.add(y)
      for d in model._Precedences:
        z = (y[0]+d[0], y[1]+d[1], y[2]+d[2])
        if z in model._Blocks:
          l.add(z)
    sumval = 0.0
    for y in s:
      sumval += model._Weight[y]
    sumval = math.floor(sumval / model._Extract)
    if sumval > model._Tlo[x]:
      count += sumval - model._Tlo[x]
      model._Tlo[x] = sumval
  if count > 0:
    print('Remove %d time-blocks' % count)
  return None

def greedy_heur(model:Model, Val, display):
  '''
  Build a greedy solution by putting in the best possible `available' block
  into the current solution and time
  '''
  # build heap of available blocks
  if display > 0:
    print('Building solution ... ', end='')
  sys.stdout.flush()
  objVal = 0
  OutDegree = { x : 0 for x in model._Blocks}
  for x in model._Blocks:
    for d in model._Precedences:
      z = (x[0] + d[0], x[1] + d[1], x[2] + d[2])
      if z in model._Blocks:
        OutDegree[x] += 1

  h = []
  for x in model._Blocks:
    if OutDegree[x] == 0:
      assert x in Val
      heapq.heappush(h, (Val[x], x))

  curx = { x : model._Tmax for x in model._Blocks}
  curt = 0
  curExtract = model._Extract
  curMining  = model._Mining
  # set the best available block to be extracted at the current time
  # if does not fit capacity, move to next time
  negative = set()
  negweight = 0
  while curt < model._Tmax and len(h) > 0:
    (val, x) = heapq.heappop(h)
    # update what is available
    for d in model._Precedences:
      z = (x[0]-d[0], x[1]-d[1], x[2]-d[2])
      if z not in model._Blocks:
        continue
      assert OutDegree[z] > 0
      OutDegree[z] -= 1
      if OutDegree[z] == 0:
        heapq.heappush(h,(Val[z],z))
    # see when we can add this block to the solution
    assert (model._Weight[x] < model._Extract and
            model._Weight[x] < model._Mining)
    if (model._Weight[x] > curExtract or
        (model._Weight[x] > curMining and model._Obj[x] > 0)):
      curt += 1
      if display > 1:
        if curt == 1:
          print('')
        print('Moving to time %d obj %g capacity %.2f%% %.2f%% ' %
              (curt, objVal, 100*(1 - curExtract / model._Extract),
              100*(1 - curMining/ model._Mining)))
      curExtract = model._Extract
      curMining  = model._Mining
    # stop when going over Tmax
    if curt >= model._Tmax:
      break
    # extract the block
    assert curt < model._Tmax
    assert model._Weight[x] <= curExtract
    curExtract -= model._Weight[x]
    curval = model._Obj[x] * (1.0 / (1 + model._DiscountRate)) ** curt
    if curval > 0:
      assert curMining >= model._Weight[x]
      curMining -= model._Weight[x]
      negative = set()
      negweight = 0
    else:
      negative.add(x)
      negweight += curval
    curx[x] = curt
    objVal += curval
  #get rid of the last batch of negative blocks
  for x in negative:
    curx[x] = model._Tmax
  objVal -= negweight
  # set initial solution
  for key in model._Vars:
    if curx[key[0:-1]] <= key[3]:
      model._greedyx[key] = 1
    else:
      model._greedyx[key] = 0
  if display > 0:
    print(pycol.Fore.RED)
    print(lineseparator)
    print('Greedy Heuristic done, value %g' % objVal)
    print(lineseparator)
    print(pycol.Style.RESET_ALL)
  return None

def rolling_heur(model:Model, display, deltaT=1):
  '''
  Given a model, build a solution using a rolling time heuristic
  deltaT   controls how many integer periods to consider
  display  controls output
  '''
  omethod = model.params.method
  ogap    = model.params.mipgap
  ooutput = model.params.outputflag
  oprep   = model.params.presolve
  # first time is faster barrier
  model.params.presolve = 1
  model.params.method   = 2
  model.params.mipgap   = 0.01
  if display < 3:
    model.params.outputflag = 0
  else:
    model.params.outputflag = 1

  extra = {}
  assert(deltaT > 0)
  # Loop in all time periods (minus deltaT)
  for curt in range(model._Tmax):
    # relax variables with time over curt+deltaT
    for x in model._Vars:
      if x[3] > curt:
        model._Vars[x].setAttr('VType',GRB.CONTINUOUS)
      else:
        model._Vars[x].setAttr('VType',GRB.BINARY)
    # these constraints collapse periods curt+deltaT..._Tmax-1 into one
    extra= model.addConstrs((model._Vars[(x[0],x[1],x[2],t)] - 
                             model._Vars[(x[0],x[1],x[2],t+1)] == 0
                              for x in model._Blocks
                              for t in range(max(curt + deltaT,model._Tlo[x]),
                                             model._Tmax-1)),
                            name='shrink')
    # solve model
    model.optimize()
    model.remove(extra)
    # no solution found
    if model.SolCount == 0:
      break;
    # display some info
    if display > 0:
      print('Rolling Horizon Period %d/%d current value %g bound %g %.2f seconds' % 
            (curt, model._Tmax-1, model.ObjVal, model.ObjBound,
             time.time() - model._start_time))
      sys.stdout.flush()
    # fix variables in current period
    for x in model._Vars:
      if x[3] == curt:
        model._Vars[x].lb = model._Vars[x].X
        model._Vars[x].ub = model._Vars[x].X
  # check status
  if model.SolCount == 0:
    print(pycol.Fore.RED)
    print(lineseparator)
    print('Rolling Horizon Heuristic failed')
    print(lineseparator)
    print(pycol.Style.RESET_ALL)
    sys.stdout.flush()
  else:
    print(pycol.Fore.RED)
    print(lineseparator)
    print('Rolling Horizon Heuristic done, value %g, %.2f seconds' % 
          (model.ObjVal, time.time() - model._start_time))
    print(lineseparator)
    print(pycol.Style.RESET_ALL)
    # save solution as mip-start and reset bounds
    for x in model._Vars:
      model._Vars[x].start = model._Vars[x].X
  # reset model
  for x in model._Vars:
    model._Vars[x].vtype = GRB.BINARY
    model._Vars[x].lb = 0
    model._Vars[x].ub = 1
  model.remove(extra)
  model.params.method     = omethod
  model.params.mipgap     = ogap
  model.params.outputflag = ooutput
  model.params.presolve   = oprep
  model.update()
  # done
  return None

def improve_heur(model:Model, curX, display, deltaT=1):
  '''
  Given a model-vars solution, do a Local Search heuristic forward
  and backward pass by fixing all but deltaT+1 time periods
  curX      starting (integer feasible) solution
  deltaT    controls how many periods to optimize
  display   controls output:
            0 for none
            1 for basic info
            2 for improving info along the way
            3 for full sub-mip output
  '''
  curt = 0
  BestBdStop = model._bestsolval
  copyModel = model.copy()
  copyModel.setParam(GRB.Param.Method, -1)
  copyModel.setParam('BestBdStop',BestBdStop)
  copyModel.setParam('NodeLimit',100)
  copyModel.setParam('MIPGap',0.005)
  if display < 3:
    copyModel.setParam('OutputFlag',0)
  mapVars = {x : copyModel.getVarByName(model._Vars[x].getAttr('VarName'))
                 for x in model._Vars}
  prevval = 0.0
  curval = 0.0
  if display > 0:
    print(lineseparator)
    print('Start Local Search Heuristic:')
    sys.stdout.flush()
  while curt + deltaT < model._Tmax:
    for x in model._Vars:
      mapVars[x].setAttr(GRB.Attr.Start, curX[x])
      if x[3] < curt:
        mapVars[x].setAttr('Ub', curX[x])
        mapVars[x].setAttr('Lb', curX[x])
      elif x[3] <= curt + deltaT:
        mapVars[x].setAttr('Ub', model._Vars[x].getAttr('Ub'))
        mapVars[x].setAttr('Lb', model._Vars[x].getAttr('Lb'))
      else:
        mapVars[x].setAttr('Ub', curX[x])
        mapVars[x].setAttr('Lb', curX[x])
    curt += 1
    copyModel.optimize()
    curval = copyModel.ObjVal
    if display > 1 and prevval + 1e-6 < curval:
      print('Improved solution value %g, Period %d, %.2f seconds' % (curval, curt, time.time() - model._start_time))
      sys.stdout.flush()
      prevval = curval
    for x in model._Vars:
      curX[x] = mapVars[x].getAttr('X')
  while curt > 0:
    curt -= 1
    for x in model._Vars:
      mapVars[x].setAttr(GRB.Attr.Start, curX[x])
      if x[3] < curt:
        mapVars[x].setAttr('Ub', curX[x])
        mapVars[x].setAttr('Lb', curX[x])
      elif x[3] <= curt + deltaT:
        mapVars[x].setAttr('Ub', model._Vars[x].getAttr('Ub'))
        mapVars[x].setAttr('Lb', model._Vars[x].getAttr('Lb'))
      else:
        mapVars[x].setAttr('Ub', curX[x])
        mapVars[x].setAttr('Lb', curX[x])
    copyModel.optimize()
    curval = copyModel.ObjVal
    if display > 1 and prevval + 1e-6 < curval:
      print('Improved solution value %g, Period %d, %.2f seconds' % (curval, curt, time.time() - model._start_time))
      sys.stdout.flush()
      prevval = curval
    for x in model._Vars:
      curX[x] = mapVars[x].getAttr('X')
  if display > 0:
    print(pycol.Fore.RED)
    print(lineseparator)
    print('Local Search Heuristic ended with value %g' % curval)
    print(lineseparator)
    print(pycol.Style.RESET_ALL)
    sys.stdout.flush()
  return None

def FormulateOpenPit(model:Model, UsePreprocess=1, UseGreedy=1, UseImprove=1,
                     UseCallback=1, UseRolling=1, Xmax=20, Ymax=20, Zmax=15, Tmax=15,
                     La=4, Lb=4, Lc=1, DiscountRate=0.15, deltaT=3, display=2):
  '''
  Create a mining model using the given blocks, time limits and discount rate
  '''
  model._bestsolval = -1e30
  model._Xmax = Xmax
  model._Ymax = Ymax
  model._Zmax = Zmax
  model._Tmax = Tmax
  model._La   = La
  model._Lb   = Lb
  model._Lc   = Lc
  model._DiscountRate = DiscountRate
  model._Precedences = [( 0, 0, 1),
                        ( 1, 0, 1),
                        ( 0, 1, 1),
                        ( 0,-1, 1),
                        (-1, 0, 1)]

  print('Building grid blocks ... ', end='')
  model._Blocks = {(x,y,z) for x in range(model._Xmax)
                           for y in range(model._Ymax)
                           for z in range(model._Zmax)}
  print('done (%d added)' % len(model._Blocks))
  model._Obj    = { x : obj_val(x[0], x[1], x[2], model._Xmax, model._Ymax,
                                model._Zmax, model._La, model._Lb, model._Lc)
                        for x in model._Blocks} 

  model._Extract = len(model._Blocks) * 1.0 / (model._Tmax * 2.2)
  model._Mining = model._Extract / 1.2

  if UsePreprocess:
    objpre_process_blocks(model)

  model._Weight = { x : 0.9 + 0.2 * random.random() for x in model._Blocks}
  model._Tlo    = { x : 0 for x in model._Blocks}
  if model._Mining < 1.1:
    model._Mining = 1.1
  if model._Extract < 1.1:
    model._Extract = 1.1

  if UsePreprocess:
    timepre_process_blocks(model)
  model.setAttr(GRB.Attr.ModelSense,GRB.MAXIMIZE)

  model._maxObj = -1e100
  model._minObj = 1e100
  print('Add variables and objective function ... ', end='')
  sys.stdout.flush()
  allKeys = {(x[0],x[1],x[2],t) for x in model._Blocks
                                for t in range(model._Tlo[x],model._Tmax)}
  model._Vars = model.addVars(allKeys, vtype=GRB.BINARY, name='B')
  model._greedyx = {x : 0 for x in model._Vars}
  for key in model._Vars:
    x = key[0:-1]
    t = key[3]
    objFct = 0
    ratio = 1.0 / (1 + model._DiscountRate)
    if t + 1 < model._Tmax:
      objFct = ratio ** t - ratio ** (t+1)
    else:
      objFct = ratio ** t
    model._Vars[key].setAttr(GRB.Attr.Obj,model._Obj[x] * objFct)
    if model._Obj[x] < model._minObj:
      model._minObj = model._Obj[x]
    if model._Obj[x] > model._maxObj:
      model._maxObj = model._Obj[x]
  print('done (added %d vars obj range [%g,%g])' % 
        (len(model._Vars), model._minObj, model._maxObj))
  model.update()
  
  # Add Precedences
  count = 0
  print('Adding precedences ... ', end='')
  sys.stdout.flush()
  for key in model._Vars:
    if key[3] + 1 < model._Tmax:
      y = (key[0], key[1], key[2], key[3]+1)
      model.addConstr(model._Vars[key] <= model._Vars[y])
      count += 1
    for d in model._Precedences:
      y = (key[0]+d[0], key[1]+d[1], key[2]+d[2], key[3])
      if y in model._Vars:
        model.addConstr(model._Vars[key] <= model._Vars[y])
        count += 1
  print('done (added %d precedences)' % count)

  # add capacity constraint
  linExpr = LinExpr()
  print('Adding knapsack capacities ... ', end='')
  sys.stdout.flush()
  count = 0
  for t in range(model._Tmax):
    t2 = t-1
    linExpr.clear()
    linExpr.add(quicksum(model._Vars[x] * model._Weight[x[0:-1]] for x in model._Vars
                                                   if x[3] == t), 1)
    linExpr.add(quicksum(model._Vars[x] * model._Weight[x[0:-1]] for x in model._Vars
                                                   if x[3] == t2), -1)
    model.addConstr(linExpr, GRB.LESS_EQUAL, model._Extract, 'Extract_'+str(t))
    count += 1
    linExpr.clear()
    linExpr.add(quicksum(model._Vars[x] * model._Weight[x[0:-1]] for x in model._Vars
                                                   if model._Obj[x[0:-1]] > 0
                                                   if x[3] == t), 1)
    linExpr.add(quicksum(model._Vars[x] * model._Weight[x[0:-1]] for x in model._Vars
                                                   if model._Obj[x[0:-1]] > 0
                                                   if x[3] == t2), -1)
    model.addConstr(linExpr, GRB.LESS_EQUAL,  model._Mining, 'Mine_'+str(t))
    count += 1
  print('done (added %d knapsack)' % count)
  model.update()
  #model.write('mine.lp')
  sys.stdout.flush()

  # Call greedy heuristic using as sorting value minus the objective function
  if UseGreedy:
    greedyval = {x : -model._Obj[x] for x in model._Blocks}
    greedy_heur(model, greedyval, display-1)
    if UseImprove:
      improve_heur(model, model._greedyx, display-1, deltaT=deltaT)
    # load model._greedyx into MipStart
    for key in model._Vars:
      model._Vars[key].setAttr(GRB.Attr.Start,model._greedyx[key])
  # Call rolling horizon
  if UseRolling:
    rolling_heur(model, display-1, deltaT=deltaT)

  # enable/disable callback use
  model._UseCallback = UseCallback
  # update time limit
  runlimit = model._runlimit - (time.time() - model._start_time)
  runlimit = max(runlimit,1)
  model.params.timelimit = runlimit

  return None

def OpenPitCallback(model:Model, where):
  if model._UseCallback == 0:
    return None
  if where == GRB.Callback.POLLING:
    pass
  elif where == GRB.Callback.PRESOLVE:
    pass
  elif where == GRB.Callback.SIMPLEX:
    pass
  elif where == GRB.Callback.MIP:
    pass
  elif where == GRB.Callback.MIPSOL:
    model._bestsolval = model.cbGet(GRB.Callback.MIPSOL_OBJBST)
  elif where == GRB.Callback.MIPNODE:
    if model.cbGet(GRB.Callback.MIPNODE_STATUS) == GRB.Status.OPTIMAL:
      nodex = model.cbGetNodeRel(model._Vars)
      greedyval = {x : model._Tmax - 
                       0.1* (model._Obj[x] - model._minObj) /
                            (model._maxObj - model._minObj + 1e-6)
                       for x in model._Blocks}
      for x in model._Vars:
        greedyval[x[0:-1]] -= (x[3]+1) * nodex[x]
      greedy_heur(model, greedyval, 0)
      #improve_heur(model, model._greedyx, 0, deltaT=2)
      model.cbSetSolution(model._Vars,model._greedyx)
  elif where == GRB.Callback.BARRIER:
    pass
  elif where == GRB.Callback.MESSAGE:
    pass
  return None

def print_stats(model:Model):
  '''
  Print solution bound and value (if feasible solution found) information
  '''
  print(lineseparator)
  print('Model Stats:')
  model.printStats()
  if model.Status == GRB.INFEASIBLE:
    print('Model is Infeasible')
  elif model.Status == GRB.LOADED:
    print('Problem not optimized')
  elif ((model.Status == GRB.OPTIMAL) or (model.Status == GRB.ITERATION_LIMIT) or
        (model.Status == GRB.NODE_LIMIT) or (model.Status == GRB.TIME_LIMIT) or
        (model.Status == GRB.SOLUTION_LIMIT) or (model.Status == GRB.INTERRUPTED)):
    if (model.SolCount > 0):
      print('Model bound: %.3f, Best Sol: %.3f Gap %.2f%%' % (model.ObjBound, model.ObjVal, 100.0 *abs(model.ObjVal - model.ObjBound)/ max(1,abs(model.ObjBound))))
      print(lineseparator)
      print('Solution Detail:')
      X=model.getAttr('x',model._Vars)
      Bt = {x: model._Tlo[x] for x in model._Blocks} # Time of extraction
      results = {'Time':range(model._Tmax), 'Obj':[0] * model._Tmax, 'Obj%':[0]*model._Tmax, 'Truck':[0] * model._Tmax, 'Plant':[0] * model._Tmax, 'Blocks':[0] * model._Tmax}
      # compute extraction time
      for x in model._Vars:
        if X[x] < 0.5:
          Bt[x[0:-1]] += 1
      # compute objective and usage
      for x in model._Vars:
        if X[x] > 0.5:
          results['Obj'][Bt[x[0:-1]]] += model._Vars[x].getAttr('Obj')
          results['Obj%'][Bt[x[0:-1]]] += 100 * model._Vars[x].getAttr('Obj') / model.ObjVal
          if x[3] == Bt[x[0:-1]]:
            results['Blocks'][x[3]] += 1
            results['Truck'][x[3]]  += model._Weight[x[0:-1]]
            if model._Obj[x[0:-1]] > 0:
              results['Plant'][x[3]]  += model._Weight[x[0:-1]]
      print(DataFrame(results).set_index('Time')[['Obj','Obj%','Truck','Plant','Blocks']])
      print('Capacities: %g %g Blocks: %d Time Periods: %d' % 
            (model._Extract, model._Mining, len(model._Blocks), model._Tmax))
    else:
      print('Model bound: %.3f, No solution found' % model.ObjBound)
  else:
    print('Unexpected status %d' % model.Status)
  print('Total Running time: %.2f' % (time.time() - model._start_time))
  return None

# Parse argument
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-C','--callback', help='Use Heuristic as Callbacks', default=0, action='count')
parser.add_argument('-G','--greedy', help='Enable initial greedy heuristic', default=0, action='count')
parser.add_argument('-I','--improve', help='Improve initial greedy heuristic with sub-mips', default=0, action='count')
parser.add_argument('-O','--optimize', type=int,help='Perform full problem optimization', default=1)
parser.add_argument('-P','--preprocess', help='Preprocess variables', default=0, action='count')
parser.add_argument('-R','--rollinghorizon', help='Enable initial rolling horizon heuristic', default=0, action='count')
parser.add_argument('-S','--submipsize', type=int,help='Periods in Time-Window heuristic', default=3)
parser.add_argument('-T','--timelimit', type=float,help='Time limit for optimization',default=1e100)
parser.add_argument('-v','--verbose', help='verbose output', action='count', default=0)
parser.add_argument('-Z','--minesize', type=int,help='Periods in Time-Window heuristic', default=10)

args = parser.parse_args()

start_time    = time.time()
usegreedy     = args.greedy
useimprove    = args.improve
submipsize    = args.submipsize
runlimit      = args.timelimit
verbose       = args.verbose
usepreprocess = args.preprocess
usecallback   = args.callback
minesize      = args.minesize
optimize      = args.optimize
rolling       = args.rollinghorizon

# init
pycol.init()

# just formulate and solve
print(lineseparator)
random.seed(0)
model = None
model = Model()
model._start_time = start_time
model._runlimit   = runlimit
FormulateOpenPit(model,
                 Xmax=minesize,
                 Ymax=minesize,
                 Zmax=int(3.0*minesize/4.0),
                 Tmax=int(3.0*minesize/4.0),
                 deltaT=submipsize,
                 UseRolling=rolling,
                 UsePreprocess=usepreprocess,
                 UseGreedy=usegreedy,
                 UseImprove=useimprove,
                 UseCallback=usecallback,
                 display=verbose+1)
if optimize:
  model.params.outputflag=0
  if verbose > 1:
    model.params.outputflag=1
  model.setParam(GRB.Param.Method, 2)
  model.setParam('MIPGap',0.005)
  model.optimize(OpenPitCallback)
print_stats(model)
