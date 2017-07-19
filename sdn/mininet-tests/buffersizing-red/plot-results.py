#coding: utf-8
#!/usr/bin/env python
import sys
sys.path.append('..')
sys.path.append('../util')
sys.path.append('../..')
sys.path.append('../../util')
from util.helper import *
import glob
from collections import defaultdict
import plot_defaults
from matplotlib import rc, rcParams

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

args = parser.parse_args()
data = defaultdict(list)
nedata = defaultdict(list)
RTT = 85.0 # ms
BW = 62.5 # Mbps
nruns = 10 # Number of runs for your experiment
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
    lines = open(filename).read().split("\n")
    for l in lines:
        if l.strip() == "":
            continue
        x, pkt, byte = map(float, l.split(' '))
        data[int(x)].append(byte/1024.0)
        if  len(data[int(x)])==3: # 打印汇总数据的 list
            print "debug: parse_data data[x] x=%s byte=%s list=%s" % (x, byte, data[int(x)])
    return

def parse_nedata2(filename):
    lines = open(filename).read().split("\n")
    for l in lines:
        if l.strip() == "":
            continue
        values = map(int, l.split(' '))
        x, y = values[0], values[1]
        nedata[x].append(y / 1024.0)
    return

for f in glob.glob("%s/*/result.txt" % args.dir):
    print "Parsing %s" % f
    parse_data(f)
    nfiles += 1

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
    quido2 =  bdp / math.sqrt(n) / 4
    plot_quido.append((n, quido))
    plot_quido2.append((n, quido2))
    plot_bdp.append((n, bdp))

PHI=1.618
fig = plt.figure(figsize=(8, 8/PHI))

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

# - 平均计算方法: 如运行多轮 -r1 -r2 -r3 , 则将数据放入 list 中进行平均
avg_mn = []
for k in keys:
    avg_mn.append(avg(data[k]))



if args.embed:
    
    # 使用内嵌4项数据生成图表 for flows_per_host in 10 25 50 100; 
    
    #绘制 基准数据 rootdir=../buffersizing/result-buffersizing-Jul18-09-11/ 多测试了1组400流
    # [12.6953125, 6.8359375, 5.859375, 4.8828125, 4.8828125]
    plt.plot(keys, [12.6953125, 6.8359375, 5.859375, 4.8828125], lw=2, label="Mininet-Droptail", marker='s', markersize=10)
    
    # RED 数据源来自于 写入 result.txt 中的 q_max = q_limit/4
    #绘制 参考数据 rootdir=result-p0.02-Jul17-23-13-含25流
    plt.plot(keys, [16.2194010417, 10.9258626302, 5.05208333333, 3.56640625], lw=2, label="Mininet-red-p0.02", marker='s', markersize=10)
    #绘制 参考数据 rootdir=result-p0.2-Jul18-10-13
    plt.plot(keys, [37.3435872396, 11.9458007812, 8.82307942708, 5.11311848958], lw=2, label="Mininet-red-p0.2", marker='s', markersize=10)
    #绘制 参考数据 rootdir=result-p0.08-Jul18-08-24
    plt.plot(keys, [28.8127441406, 17.9835611979, 8.76204427083, 4.80493164062], lw=2, label="Mininet-red-p0.8", marker='s', markersize=10)
else:
    # 绘制 BDP 为直线, 固定值; 如果 RTT 和 BW 不变的话
    plt.plot(first(plot_bdp), second(plot_bdp), lw=2, label="BDP", color="gray")

    # 绘制
    plt.plot(first(plot_quido), second(plot_quido), lw=2, label="RTT*C/$\sqrt{n}$")
    
    # 绘制
    plt.plot(first(plot_quido2), second(plot_quido2), lw=2, label="RTT*C/$\sqrt{n}$/4")
    
    # 绘制当前数据
    plt.plot(keys, avg_mn, lw=2, label="%s" % args.dir, marker='s', markersize=10)

for i in xrange(len(keys)):
    print "%s," % (avg_mn[i]), 
print "== paste above data to %s/result.txt" % args.dir

#plt.xscale('log')
plt.yscale('log')

plt.xlim((0, nflows))

plt.legend()
# 修改默认的 内嵌 legend 位置为右侧
# Place a legend to the right of this smaller subplot.
# plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


plt.ylabel("Queue size")
plt.xlabel("Total \#flows (n)")
plt.grid(True)
# xticks = range(0, 801, 100)
# 调整坐标轴
xticks = range(0, 201, 25)
plt.xticks(xticks, map(str, xticks))

# yticks = [1, 10, 100, 1000]
# yticklabels = ['1kB', '10kB', '100kB', '1MB']
yticks = [1, 1.5, 3, 10, 100]
yticklabels = ['1kB', '', '3kB', '10kB', '100kB']
plt.yticks(yticks, yticklabels)

if args.out:
    print "Saving to %s" % args.out
    plt.savefig(args.out)
else:
    # TODO linux 下不起作用
    plt.show()
