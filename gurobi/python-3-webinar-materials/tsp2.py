#!/usr/bin/python

# Copyright 2016, Gurobi Optimization, Inc.

# Solve a traveling salesman problem on a randomly generated set of
# points using lazy constraints.   The base MIP model only includes
# 'degree-2' constraints, requiring each node to have exactly
# two incident edges.  Solutions to this model may contain subtours -
# tours that don't visit every city.  The lazy constraint callback
# adds new constraints to cut them off.

import sys
import math
import random
import itertools
import time
import argparse
import colorama as pycol
from gurobipy import *

lineseparator = '----------------------------------------------------------------------'

def greedy_heu(model):
  '''
  This heuristics starts from node zero, and select a shortest edge to
  move to an unvisited node. Then repeat the process in the new
  terminal
  '''
  start_time = time.time()
  unvisited = list(range(model._n))
  for i,j in model._vars.keys():
    model._vars[i,j].setAttr('Start',0)
    model._vars[i,j]._curX = 0
  current = 0
  totval  = 0
  #select next node within unvisited
  while current in unvisited:
    nextval = 1e100
    nextvar = None
    bextj   = model._n
    for i,j in model._vars.keys().select(current,'*'):
      if j in unvisited:
        curval = model._vars[current,j].getAttr('Obj') 
        if curval < nextval:
          nextval = curval 
          nextvar = model._vars[current,j]
          nextj   = j
    # This may happen if we are not working on a complete set of edges
    if nextvar is None:
      break
    totval += nextval
    assert(j < model._n)
    nextvar.setAttr('Start',1)
    nextvar._curX = 1
    unvisited.remove(current)
    current = nextj
  assert(len(unvisited) >= 1)
  #add last edge to the solution
  if (current,0) in model._vars.keys():
    unvisited.remove(current)
    totval += model._vars[current,0].getAttr('Obj')
    model._vars[current,0].setAttr('Start',1)
    model._vars[current,0]._curX = 1
  #record whether we found a solution or not
  model._tourval = None
  if unvisited:
    print(pycol.Fore.RED + 'Failed to build greedy solution, unvisited %s %.2f seconds' % (str(unvisited),time.time()-start_time))
    print(pycol.Style.RESET_ALL)
  else:
    model._tourval = totval
    print(pycol.Fore.RED)
    print(lineseparator)
    print('Found feasible solution, value %g %.2f seconds' % (totval,time.time()-start_time))
    print(lineseparator)
    print(pycol.Style.RESET_ALL)
  return None

def local_heu(model, maxlen, maxt=10, display=0, sequential=1):
  '''
  This heuristic start from a solution (stored in
  model._vars[i,j]._curX) and fix all variables incident to all nodes
  but for `maxt` of them, and optimize the remaining problem. The
  selection of nodes can be sequential within the current best
  solution (sequential=1) or following node indices (sequential = 0)
  This process is iterated twice the length of the tour
  '''
  #ensure we have a solution
  if (model._tourval is None):
    print('No starting solution stored')
    return None
  #ensure model is big enough
  if (model._n < maxlen):
    print('Sub-problem too small')
    return None
  #stats
  start_time = time.time()
  optimal = 0
  timelimit = 0
  #change parameters
  origt = model.Params.timelimit
  origP = model.Params.outputflag
  origG = model.Params.mipgap
  model.params.timelimit = maxt
  model.params.outputflag = display
  model.params.mipgap = 0.005
  #build sequence
  tour = subtour(tuplelist((i,j) for i,j in model._vars.keys() if model._vars[i,j]._curX > 0.5))
  #print('Initial Tour:' + str(tour))
  assert(len(tour) == model._n)
  #loop in sequence twice
  for i in range(model._n):
    fixed = []
    #fix part of the problem to the current solution
    for j in range(model._n - maxlen):
      k = i + j
      while (k >= model._n):
        k -= model._n
      if sequential:
        k = tour[k]
        assert(k >= 0 and k < model._n)
      #print('Fix node %d i,j %d,%d' % (k,i,j))  
      assert(k >= 0 and k < model._n and k not in fixed)
      fixed.append(k)
      for a,b in model._vars.keys().select(k,'*'):
        model._vars[a,b].setAttr('LB', model._vars[a,b]._curX)
        model._vars[a,b].setAttr('UB', model._vars[a,b]._curX)
    #optimize
    model.optimize(subtourelim)
    if model.Status == GRB.OPTIMAL:
      optimal += 1
    if model.Status == GRB.TIME_LIMIT:
      timelimit += 1
    if model.getAttr('SolCount') == 0:
      print('Failed in local optimization')
      for i,j in model._vars.keys():
        model._vars[i,j].setAttr('LB', 0)
        model._vars[i,j].setAttr('UB', 1)
      model.update()
      break
    if model.getAttr('ObjVal') + 1e-6 < model._tourval:
      for i,j in model._vars.keys():
        if model._vars[i,j].getAttr('X') > 0.5:
          model._vars[i,j]._curX = 1
        else:
          model._vars[i,j]._curX = 0
      model._tourval = model.getAttr('ObjVal')
      print('Improve solution %g %.2f seconds' % (model._tourval,time.time()-start_time))
      tour = subtour(tuplelist((i,j) for i,j in model._vars.keys() if model._vars[i,j]._curX > 0.5))
      #print('Improved Tour:' + str(tour))
    for i,j in model._vars.keys():
      model._vars[i,j].setAttr('LB', 0)
      model._vars[i,j].setAttr('UB', 1)
      model._vars[i,j].setAttr('Start', model._vars[i,j]._curX)
    if (time.time() - model._start_time > model._runlimit):
      break
  #restore model parameter values
  model.params.timelimit = origt
  model.params.outputflag = origP
  model.Params.mipgap = origG
  #display and end
  print(pycol.Fore.RED)
  print(lineseparator)
  print('Final solution %g subproblems %d optimal %d timelimit %d %.2f seconds' % 
         (model._tourval, model._n, optimal, timelimit, time.time()-start_time))
  print(lineseparator)
  print(pycol.Style.RESET_ALL)
  model.update()
  return None

# Callback - use lazy constraints to eliminate sub-tours
def subtourelim(model, where):
  if where == GRB.Callback.MIPSOL:
    # make a list of edges selected in the solution
    vals = model.cbGetSolution(model._vars)
    selected = tuplelist((i,j) for i,j in model._vars.keys() if vals[i,j] > 0.5)
    # find the shortest cycle in the selected edge list
    tour = subtour(selected)
    if len(tour) < model._n:
      # add subtour elimination constraint for every pair of cities in tour
      model.cbLazy(quicksum(model._vars[i,j]
                            for i,j in itertools.combinations(tour, 2))
                   <= len(tour)-1)

# Given a tuplelist of edges, find the shortest subtour
def subtour(edges):
  unvisited = list(range(n))
  cycle = range(n+1) # initial length has 1 more city
  while unvisited: # true if list is non-empty
    thiscycle = []
    neighbors = unvisited
    while neighbors:
      current = neighbors[0]
      thiscycle.append(current)
      unvisited.remove(current)
      neighbors = [j for i,j in edges.select(current,'*') if j in unvisited]
    if len(cycle) > len(thiscycle):
      cycle = thiscycle
  return cycle

# init
pycol.init()

# Parse argument
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('cities', help='Number of cities in TSP', type=int)
parser.add_argument('-G','--greedy', help='Enable initial greedy heuristic', default=0, action='count')
parser.add_argument('-I','--improve', help='Improve initial greedy heuristic with sub-mips', default=0, action='count')
parser.add_argument('-D','--drawsolution', help='Draw final mip solution', action='count', default=0)
parser.add_argument('-v','--verbose', help='verbose output', action='count', default=0)
parser.add_argument('-S','--submipsize', type=int,help='Number of cities to consider in sub-mip', default=10)
parser.add_argument('-O','--optimize', type=int,help='Perform full problem optimization', default=1)
parser.add_argument('-T','--timelimit', type=float,help='Time limit for optimization',default=1e100)
args = parser.parse_args()

start_time   = time.time()
n            = args.cities
usegreedy    = args.greedy
useimprove   = args.improve
submipsize   = args.submipsize
drawsolution = args.drawsolution
runlimit     = args.timelimit
verbose      = args.verbose
optimize     = args.optimize

# Create n random points
random.seed(1)
points = [(random.randint(0,100),random.randint(0,100)) for i in range(n)]

# Dictionary of Euclidean distance between each pair of points
dist = {(i,j) :
    math.sqrt(sum((points[i][k]-points[j][k])**2 for k in range(2)))
    for i in range(n) for j in range(i)}

m = Model()
if verbose == 0:
  m.params.outputflag = 0

# Create variables
vars = m.addVars(dist.keys(), obj=dist, vtype=GRB.BINARY, name='e')
for i,j in vars.keys():
    vars[j,i] = vars[i,j] # edge in opposite direction

# Add degree-2 constraint
m.addConstrs(vars.sum(i,'*') == 2 for i in range(n))

# Save additional data within model
m._runlimit   = runlimit
m._start_time = start_time
m._vars       = vars
m._dist       = dist
m._n          = n
m.Params.lazyConstraints = 1

# Run heuristics
if usegreedy:
  m.update() # needed because we access variable attributes in heuristics
  greedy_heu(m)
  lhdisplay = 0
  if verbose > 1:
    lhdisplay=1
  if useimprove:
    local_heu(m, submipsize, display=lhdisplay,sequential=1)

#adjust remaining time
runlimit -= time.time() - start_time
runlimit = max(runlimit,1)
m.params.timelimit  = runlimit

# Optimize model
if optimize:
  m.optimize(subtourelim)

# final reporting
if m.getAttr('SolCount') > 0:
  vals = m.getAttr('x', vars)
  selected = tuplelist((i,j) for i,j in vals.keys() if vals[i,j] > 0.5)

  tour = subtour(selected)
  assert len(tour) == n

  print('')
  print('Solution cost: %g gap %.2f%%' % (m.objVal,100*(m.objVal - m.objBound)/max(1,abs(m.objBound))))
  print('')

  if drawsolution:
    import matplotlib.pyplot as plt
    tour = tour + [tour[0]]
    plt.figure(figsize=(4,3),dpi=150)
    for i in range(len(tour)-1):
      cur=tour[i]
      nex=tour[i+1]
      plt.plot([points[cur][0],points[nex][0]],[points[cur][1],points[nex][1]],'k-',lw=1)
    for i in range(len(tour)):
      plt.plot(points[tour[i]][0],points[tour[i]][1],'ro',markersize=5)
    plt.grid()
    plt.autoscale()
    plt.show()
else:
  print('No solution found')
print('Total running time: %.2f' % (time.time() - start_time))
