#!/usr/bin/env python
#coding: utf-8

# 检查 flows 中的速率是否接近于 rate0 中的速率
import sys, glob
import matplotlib.pyplot as plt
import numpy as np
import argparse
from collections import defaultdict

flow_rate = defaultdict(list) # 给数据制定一个默认类型
link_rate = defaultdict(float) # 给数据制定一个默认类型

# - 平均计算方法: 如运行多轮 -r1 -r2 -r3 , 则将数据放入 list 中进行平均
def avg(lst):
    return sum(lst)/len(lst)

def median(lst):
    l = len(lst)
    lst.sort()
    return lst[l/2]
    
def parse_flow_data(filename):
    """
    读取 now, ack 格式至 flow_rate: now [ack1, ack2, ack3 ...]
    """
    lines = open(filename).read().split("\n")
    for l in lines:
        if l.strip() == "":
            continue
        #print l
        x, cwnd, ack = map(float, l.split(' '))
        flow_rate[float(x)].append(ack)
        if  len(flow_rate[int(x)])==5: # 调试 打印汇总数据的 list
            pass
            # print "debug: parse_data flow_rate[x] x=%s ack=%s list=%s" % (x, ack, flow_rate[float(x)])
    return
    
def parse_link_data(filename):
    """
    读取 now, rate 格式至 link_rate: now, rate
    """
    lines = open(filename).read().split("\n")
    for l in lines:
        if l.strip() == "":
            continue
        #print l
        x, rate = map(float, l.split(' '))
        link_rate[float(x)] = rate
    return

parser = argparse.ArgumentParser(description='参数检查')

parser.add_argument('-o', '--out',
                    help="Save plot to output file, e.g.: --out plot.png",
                    dest="out",
                    default=None)

parser.add_argument('--dir',
                    dest="dir",
                    help="Directory from which outputs of the sweep are read.",
                    required=True)
                    
parser.add_argument('-c', '--compare', action='store_true', help='将数据进行打印输出')

args = parser.parse_args()
#parse_data()

for f in glob.glob("%s/rate0" % args.dir):
    if not args.out:
        print "Parsing %s" % f
    parse_link_data(f)

nfiles = 0
for f in glob.glob("%s/result*" % args.dir):
    if not args.out:
        print "Parsing %s" % f
    parse_flow_data(f)
    nfiles += 1

if not args.out:
    print "parse %d files" % nfiles

keys = list(sorted(flow_rate.keys()))


# 依据 ack 计算 rate 
writefile = None
if args.out:
    writefile = open("%s/%s" % (args.dir, args.out), 'w')
last_ack = np.array([0] * nfiles)
for k in keys:
    pass
    this_ack = np.array(flow_rate[k])
    cur_bytes = (this_ack - last_ack)
    # 打印调试 rate 计算是否正确
    # print "debug: %.1f %s %s %.1f" % (k, flow_rate[k], cur_bytes, sum(cur_bytes))
    # 打印 now flow汇总值, link带宽值
    if not args.out:
        print "%.1f %.1f %.1f" % (k, sum(cur_bytes) * 1498 * 8 , link_rate[k])
    else:
        writefile.write("%.1f %.1f\n" % (k, sum(cur_bytes) * 1498 * 8 ))
    last_ack = this_ack
    
if args.out:
    writefile.close()
    

