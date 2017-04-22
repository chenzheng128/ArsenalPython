#!/usr/bin/python
#coding:utf-8

"CS244 Assignment 1: Parking Lot"

import sys
sys.path = ['../'] + sys.path

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import lg, output
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import irange, custom, quietRun, dumpNetConnections
from mininet.cli import CLI

from time import sleep, time
from multiprocessing import Process
from subprocess import Popen
import termcolor as T
import argparse

import os
from util.monitor import monitor_cpu, monitor_qlen, monitor_devs_ng

import threading
from util_qdisc import os_popen, port_default_config, class_switch

# 记录每个会话启动时间的全局变量
TRANS_SECONDS = [] # 传输时间 -t 使用
TRANS_NUMS = []  # 传输数据量 -d 使用
WASTE_TIMES = [] # 空闲时间


def cprint(s, color, cr=True):
    """Print in color
       s: string to print
       color: color to use"""
    if cr:
        print T.colored(s, color)
    else:
        print T.colored(s, color),

parser = argparse.ArgumentParser(description="Parking lot tests")
parser.add_argument('--bw', '-b',
                    type=float,
                    help="Bandwidth of network links",
                    required=True)

parser.add_argument('--dir', '-d',
                    help="Directory to store outputs",
                    default="results")

parser.add_argument('-n',
                    type=int,
                    help=("Number of senders in the parking lot topo."
                          "Must be >= 1"),
                    required=True)

parser.add_argument('--cli', '-c',
                    action='store_true',
                    help='Run CLI for topology debugging purposes')

parser.add_argument('--time', '-t',
                    dest="time",
                    type=int,
                    help="Duration of the experiment.",
                    default = -1)
                    # default=60)

parser.add_argument('--num_mb', '-m',
                    dest="num_mb",
                    type=int,
                    help="number of mega bytes to transmit",
                    default=100)

parser.add_argument('--switch_bw', '-s',
                    action='store_true',
                    help='switch bw during transmission',
                    default=False)

# Expt parameters
args = parser.parse_args()

if not os.path.exists(args.dir):
    os.makedirs(args.dir)

lg.setLogLevel('info')


# Topology to be instantiated in Mininet
class DaSDNTopo(Topo):
    "Parking Lot Topology"

    def __init__(self, n=1, cpu=.1, bw=10, delay=None,
                 max_queue_size=None, **params):
        """Parking lot topology with one receiver
           and n clients.
           n: number of clients
           cpu: system fraction for each host
           bw: link bandwidth in Mb/s
           delay: link delay (e.g. 10ms)"""

        # BL: This is intentionally a bit pedantic, for
        # illustrative purposes!!

        # Initialize topo
        Topo.__init__(self, **params)

        # Host and link configuration
        hconfig = {'cpu': cpu}
        lconfig = {'bw': bw, 'delay': delay,
                   'max_queue_size': max_queue_size }

        # Create 2 switches, N clients, and 1 receiver
        switches = [self.addSwitch('s%s' % s,)
                     for s in irange(1, 2)]

        clients = [self.addHost('h%s' % c, **hconfig)
                   for c in irange(1, n)]

        receiver = self.addHost('h99')

        # Switch ports 1:uplink 2:hostlink 3:downlink
        uplink, hostlink, downlink = 1, 2, 3


        # # Wire up switches
        # for s1, s2 in zip(switches[:-1], switches[1:]):
        #     self.addLink(s1, s2,
        #                   port1=downlink, port2=0, **lconfig)
        #
        # # Wire up receiver
        # self.addLink(receiver, switches[0],
        #               port1=0, port2=uplink, **lconfig)

        # self.addLink(receiver, switches[1],
        #               port1=0, port2=0, **lconfig)

        # Wire up clients:
        for c in irange(0, n-1):
            self.addLink(clients[c], switches[1],
                port1=0, port2=c+1, **lconfig)

        self.addLink(receiver, switches[1],
                      port1=0, port2=99, **lconfig)




def waitListening(client, server, port):
    "Wait until server is listening on port"
    if not 'telnet' in client.cmd('which telnet'):
        raise Exception('Could not find telnet')
    cmd = ('sh -c "echo A | telnet -e A %s %s"' %
           (server.IP(), port))
    while 'Connected' not in client.cmd(cmd):
        output('waiting for', server,
               'to listen on port', port, '\n')
        sleep(.5)


def progress(t):
    "Report progress of time"
    while t > 0:
        cprint('  %3d seconds left  \r' % (t), 'cyan', cr=False)
        t -= 1
        sys.stdout.flush()
        sleep(1)
    print


def start_tcpprobe():
    os.system("rmmod tcp_probe &>/dev/null; modprobe tcp_probe;")
    Popen("cat /proc/net/tcpprobe > %s/tcp_probe.txt" % args.dir, shell=True)

def stop_tcpprobe():
    os.system("killall -9 cat; rmmod tcp_probe &>/dev/null;")

def monitor_thread_switch_bw():
    """
    线程 monitor_thread_switch_bw() 在 [10, 20] 将调整带宽从 50m 到 100m , 然后恢复
    :return:
    """
    print 'thread %s is running...' % threading.current_thread().name
    sleep(10)
    cprint ('thread %s bw ctl start...' % threading.current_thread().name, 'red')
    # do bw ctl start, duration [10, 20]
    print ("switch bw from 50 to 100")
    class_switch("s2-eth99","50mbit" ,"100mbit", 10)
    # do bw ctl release
    cprint ('thread %s ended.' % threading.current_thread().name, 'red')

def run_dasdn_expt(net, n):
    "Run experiment"
    print 'thread %s is running...' % threading.current_thread().name


    # 创建5个节点的可变时间 (n)
    if args.time !=-1:
        TRANS_SECONDS = [args.time*0.5, args.time, args.time*0.5, args.time*1.5, args.time]
        if (len(TRANS_SECONDS) < args.n): # 检查节点时间长度
            output("节点可变时间的数据不足，长度 %d < n(%d) , exit ... " %(len(TRANS_SECONDS), args.n))
            exit()
    else:
        TRANS_NUMS = [args.num_mb*0.5, args.num_mb, args.num_mb*1.5, args.num_mb*2, args.num_mb*0.5]

    WASTE_TIMES = [0, 0, 5, 0, 0] # 是否存在空闲时间

    print 'len: WASTE_TIMES %d' % len(WASTE_TIMES)
    print 'len: TRANS_SECONDS %d' % len(TRANS_SECONDS)


    # Start the bandwidth and cwnd monitors in the background
    monitors = []

    monitor = Process(target=monitor_devs_ng,
                      args=('%s/bwm.txt' % args.dir, 1.0))
    monitor.start()
    monitors.append(monitor)

    monitor = Process(target=monitor_cpu, args=('%s/cpu.txt' % args.dir,))
    monitor.start()
    monitors.append(monitor)

    # monitor = Process(target=monitor_qlen, args=('s1-eth1', 0.01, '%s/qlen_s1-eth1.txt' % (args.dir)))
    # monitor.start()
    # monitors.append(monitor)

    start_tcpprobe()

    # Get receiver and clients
    recvr = net.getNodeByName('h99')
    clients = [net.getNodeByName('h%s' % i)
                for i in irange(1, n)]
    cprint("Receiver: %s" % recvr, 'magenta')
    cprint("Clients: " + ', '.join([str(c) for c in clients]),
           'magenta')

    # Start the receiver
    port = 5001
    recvr.cmd('iperf -s -p', port,
              '> %s/iperf_server.txt' % args.dir, '&')

    waitListening(clients[0], recvr, port)


    for i in range(n):
        # for c in clients:
        c = clients[i]
        waste_time = WASTE_TIMES[i]

        sleep(1+waste_time)

        cmd = ['iperf',
               '-c', recvr.IP(),
               '-p', port,
               '-i', 1,  # reporting interval
               '-Z reno',  # use TCP Reno
               #'-yc', # report output as comma-separated values
               ]

        outfile = {}

        outfile[c] = '%s/iperf_%s.txt' % (args.dir, c.name)
        # Ugh, this is a bit ugly....
        redirect = ['>', outfile[c]]

        if args.time != -1 :
            seconds = TRANS_SECONDS[i]
            cmd += ['-t', seconds ]  # change -t seconds to -d num_bytes seconds * 75000000
            output(cmd , "\n")
            c.sendCmd(cmd + redirect, printPid=False) # background cmd
            output(' client %s connect with %d seconds, waste %d seconds ..\n' % (c, seconds, waste_time))
            #sleep(seconds)
            #output(' client %s start ... \n' % c )
            progress(seconds) # 读秒等待
        else:
            num_mb = TRANS_NUMS[i]
            cmd += ['-d', "%sM" % (num_mb) ]  # change -t seconds to -d num_bytes seconds * 75000000
            output(cmd , "\n")
            c.cmd(cmd + redirect, printPid=False)  # foreground cmd

    # Start command line for debug
    if args.cli:
        CLI(net)

    # Count down time
    # progress(seconds * n)

    # Wait for clients to complete
    # If you don't do this, iperfs may keep running!
    output('Waiting for clients to complete...\n')
    for c in clients:
        c.waitOutput(verbose=True)

    recvr.cmd('kill %iperf')

    # Shut down monitors
    for monitor in monitors:
	monitor.terminate()
    stop_tcpprobe()

def check_prereqs():
    "Check for necessary programs"
    prereqs = ['telnet', 'bwm-ng', 'iperf', 'ping']
    for p in prereqs:
        if not quietRun('which ' + p):
            raise Exception((
                'Could not find %s - make sure that it is '
                'installed and in your $PATH') % p)


def main():
    "Create and run experiment"
    start = time()

    topo = DaSDNTopo(n=args.n)

    host = custom(CPULimitedHost, cpu=.15)  # 15% of system bandwidth
    link = custom(TCLink, bw=args.bw, delay='1ms',
                  max_queue_size=200)

    net = Mininet(topo=topo, host=host, link=link)

    net.start()

    cprint("*** Dumping network connections:", "green")
    dumpNetConnections(net)

    cprint("*** Setting default port config", "green")
    # 设置默认的端口带宽策略
    port_default_config("s2-eth99", bw=50, tx_queue_len=10)

    cprint("*** Testing connectivity", "blue")

    net.pingAll()

    # if args.cli:
        # Run CLI instead of experiment
    #    CLI(net)
    #else:


    if True:
        cprint("*** Running experiment", "magenta")

        print 'thread %s is running...' % threading.current_thread().name
        # Start Bandwith control thread to Simulation SDN Ctl
        if args.switch_bw:
            t1 = threading.Thread(target=monitor_thread_switch_bw, name='ThreadBwCtl')
            t1.start()

        t2 = threading.Thread(target=run_dasdn_expt, args=(net, args.n), name='ThreadRunExpt')
        t2.start()

        if args.switch_bw: # t1.join需要放在  t2.join  cli 之前
            t1.join()
        t2.join()




    net.stop()
    end = time()
    os.system("killall -9 bwm-ng")
    cprint("Experiment took %.3f seconds" % (end - start), "yellow")

if __name__ == '__main__':
    check_prereqs()
    main()
