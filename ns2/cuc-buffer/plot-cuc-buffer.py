#coding: utf-8
#!/usr/bin/env python

# 绘制多组图形

import sys
import math
# sys.path.append('..')
# sys.path.append('../util')
# sys.path.append('../..')
# sys.path.append('../../util')
# from util.helper import *
import glob
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np
import argparse

from matplotlib import rc, rcParams

# import plot_defaults start
AXES_LABELSIZE = 24
TICK_LABELSIZE = 24
TEXT_LABELSIZE = 24
HLINE_LABELSIZE = 24
HLINE_LINEWIDTH = 2
rc('axes', **{'labelsize' : 'xx-large',
              'titlesize' : 'xx-large',
              'grid' : True})
rc('legend', **{'fontsize': 'x-large'})
rcParams['axes.labelsize'] = AXES_LABELSIZE
rcParams['xtick.labelsize'] = TICK_LABELSIZE
rcParams['ytick.labelsize'] = TICK_LABELSIZE
rcParams['xtick.major.pad'] = 4
rcParams['ytick.major.pad'] = 6
# import plot_defaults end

# Adjust just for this graph
rcParams['figure.subplot.bottom'] = 0.20
rcParams['figure.subplot.left'] = 0.20
# Disable tex
# rcParams['text.usetex'] = True
rcParams['text.usetex'] = False


parser = argparse.ArgumentParser()
parser.add_argument('-o', '--out',
                    help="Save plot to output file, e.g.: --out plot.png",
                    dest="out",
                    default=None)

parser.add_argument('--dir',
                    dest="dir",
                    help="Directory from which outputs of the sweep are read.",
                    required=True)
                    
parser.add_argument('-e', '--embed', action='store_true', help='使用内嵌数据生成图形')
parser.add_argument('-m', '--merge', action='store_true', help='使用循环模式合并绘图')

args = parser.parse_args()
data = defaultdict(list) # 存储一组绘图数据
datas = {} # 存储多组绘图数据
RTT = 85.0 # ms
BW = 62.5 # Mbps
nruns = 0 # Number of runs for your experiment
nflows = 800
# 调整坐标轴
nflows = 200
nfiles = 0

def first(lst):
    return map(lambda e: e[0], lst)

def second(lst):
    return map(lambda e: e[1], lst)

# - 平均计算方法: 如运行多轮 -r1 -r2 -r3 , 则将数据放入 list 中进行平均
def avg(lst):
    return sum(lst)/len(lst)

def median(lst):
    l = len(lst)
    lst.sort()
    return lst[l/2]

def parse_data(filename):
    """
    将数据追加至 data 中
    """
    lines = open(filename).read().split("\n")
    for l in lines:
        if l.strip() == "":
            continue
        x, pkt, byte = map(float, l.split(' '))
        # data[int(x)].append(byte/1024.0)
        data[int(x)].append(pkt)
        if  len(data[int(x)])>2: # 打印汇总数据的 list
            print "debug: parse_data data[x] x=%s avg_pkt=%d list=%s" % (x, avg(data[int(x)]), data[int(x)])
    return

nresult = 0
folders = []
# 依据参数, 搜索 data 开头目录, 已绘制多组数据, 或是一组 default 数据
for folder in glob.glob("%s/data*" % args.dir):
    data = defaultdict(list) # 存储一组绘图数据
    nfiles = 0
    for f in glob.glob("%s/*/result.txt" % folder):
        print "Parsing %s" % f
        parse_data(f)
        nfiles += 1
    print "debug: 分析一组 data 结束 ..."
    datas[folder] = data
    nresult +=1

if nfiles == 0:
    print "Result files not found.   Did you pass the directory correctly?"
    sys.exit(0)

plot_quido = []
plot_quido2 = []
plot_bdp = []
plot_data = []
for n in sorted(data.keys()):
    bdp = (RTT * 1000 * BW / 8.0 / 1024.0)
    quido =  bdp / math.sqrt(n)
    quido2 =  bdp / math.sqrt(n) * 2
    plot_quido.append((n, quido))
    plot_quido2.append((n, quido2))
    plot_bdp.append((n, bdp))

# 定义绘图大小
PHI=1.618
fig = plt.figure(figsize=(9, 9/PHI))

keys = list(sorted(data.keys()))

for i in xrange(nruns):
    try:
        values = [mndata[k][i] for k in keys]
    except:
        break
    if i == 0:
        label = "Mininet-HiFi"
    else:
        label = ''
    plt.plot(keys, values,
             lw=1, label=label, color="red")


if args.embed:
    """
    这部分代码在改为 循环模式后暂时不用
    """
    keys=[50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150,]
    
    plt.plot(first(plot_quido), second(plot_quido), lw=2, label="RTT*C/$\sqrt{n}$")
    
    plt.plot(first(plot_quido2), second(plot_quido2), lw=2, label="2*RTT*C/$\sqrt{n}$")
    
    plt.plot(keys, [105, 97, 99, 104, 110, 74, 61, 35, 41, 24, 25], ls='None', label="980-80-500-43.5-360", marker='+', markersize=10)
    
    plt.plot(keys, [134, 149, 130, 174, 158, 102, 117, 84, 64, 50, 56], ls='None', label="995-80-500-43.5-360", marker='x', markersize=10)
    
    plt.plot(keys, [118, 114, 128, 111, 107, 82, 73, 50, 40, 38, 35], ls='None', label="999-80-500-43.5-360", marker='*', markersize=10)
    
else:
    # 绘制 BDP 为直线, 固定值; 如果 RTT 和 BW 不变的话
    # plt.plot(first(plot_bdp), second(plot_bdp), lw=2, label="BDP", color="gray")
    
    plt.plot(first(plot_quido), second(plot_quido), lw=2, label="RTT*C/$\sqrt{n}$")
    
    plt.plot(first(plot_quido2), second(plot_quido2), lw=2, label="2*RTT*C/$\sqrt{n}$")
    

    for x in sorted(datas.keys()):
        # - 平均计算方法: 如运行多轮 -r1 -r2 -r3 , 则将数据放入 list 中进行平均
        data = datas[x]
        avg_mn = []
        for k in keys:
            avg_mn.append(avg(data[k]))
                
        # print key, datas[key]
        
        # 绘制当前数据
        simple_label = ("%s" % x).split("/")[-1] # 取出最后一个目录作为lable
        plt.plot(keys, avg_mn, lw=2, label=simple_label, marker='s', markersize=10)
        
        for i in keys:
            print "%s," % i, 
        print "== data comes from  %s/result.txt" % args.dir

        for i in xrange(len(keys)):
            print "%d," % (avg_mn[i]), 
        print "== paste above data to %s/result.txt" % args.dir
        


plt.legend()
plt.ylabel("Queue size (pkts)")
plt.xlabel("Total #flows (n)")
plt.grid(True)

if args.out:
    print "Saving to %s" % args.out
    plt.savefig(args.out)
else:
    # TODO linux 下不起作用
    plt.show()
