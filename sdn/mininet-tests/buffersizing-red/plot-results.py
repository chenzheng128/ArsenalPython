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

args = parser.parse_args()
data = defaultdict(list)
nedata = defaultdict(list)
RTT = 85.0 # ms
BW = 62.5 # Mbps
nruns = 10 # Number of runs for your experiment
nflows = 800
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

plt.plot(first(plot_quido), second(plot_quido), lw=2, label="RTT*C/$\sqrt{n}$")

plt.plot(first(plot_quido2), second(plot_quido2), lw=2, label="RTT*C/$\sqrt{n}$/4")

# BDP 为直线, 固定值; 如果 RTT 和 BW 不变的话
plt.plot(first(plot_bdp), second(plot_bdp), lw=2, label=" bdp", color="gray")

# Should you want the BDP plot
#plt.plot(first(plot_bdp), second(plot_bdp), lw=2, label="RTT*C")

# Plot results from Neda's experiment
# parse_nedata2('nedata2.txt')
# median_yneda = []
# keys = list(sorted(nedata.keys()))
# for k in keys:
#     median_yneda.append(avg(nedata[k]))
# plt.plot(keys, median_yneda, lw=2, label="Hardware",
#          color="black", ls='--', marker='d', markersize=10)


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

plt.plot(keys, avg_mn, lw=2, label="Mininet-HiFi", color="red", marker='s', markersize=10)

#plt.xscale('log')
plt.yscale('log')

plt.xlim((0, nflows))
plt.legend()
plt.ylabel("Queue size")
plt.xlabel("Total \#flows (n)")
plt.grid(True)
xticks = range(0, 801, 100)
plt.xticks(xticks, map(str, xticks))

yticks = [1, 10, 100, 1000]
yticklabels = ['1kB', '10kB', '100kB', '1MB']
plt.yticks(yticks, yticklabels)

if args.out:
    print "Saving to %s" % args.out
    plt.savefig(args.out)
else:
    plt.show()
