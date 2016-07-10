#!/usr/bin/python
# --*-- coding:utf-8 --*--

"""
端口修改的快捷脚本 ./port_policy_util.py
使用方法
  ./qdisc_helper.py help
  ./qdisc_helper.py netem 100 30.0ms "s1-eth3 s2-eth3"
"""

import os
import sys


def handle_change(port):
    # handle_change_prio(port, tx_queue_len)
    handle_change_netem(port, 100, "20.0")
    pass


def handle_del(port):
    os.popen("tc qdisc del dev %s parent 1:2 handle 2:" % port)


def handle_show(port):
    # 查看 handle
    print("".join(os.popen("tc -s qdisc show dev %s" % port).readlines()))


def handle_change_netem(port, queue_len=100, delay="10.0ms"):
    # 修改为 prio handle
    handle_del(port)
    os.popen("tc qdisc add dev %s parent 1:2 handle 2: netem limit %s delay %s" % (port, queue_len, delay))
    handle_show(port)


def handle_change_prio(port, queue_len=100):
    handle_del(port)
    os.popen("tc qdisc add dev %s parent 1:2 handle 2: pfifo limit %s" % (port, queue_len))
    handle_show(port)


def handle_change_red(port, queue_len=10000):
    # 队列2 采用RED队列, 支持 早期随机mark为ecn的方式
    handle_del(port)
    os.popen("tc qdisc add dev %s parent 1:2 handle 2: red limit %s min 50000 max 150000 avpkt 1000 ecn" % (
        port, queue_len))
    handle_show(port)


def class_change_hosts_port(rate):
    """
    修改主机接口带宽
    :param rate:
    :return:
    """
    for port in "s1-eth1 s1-eth2 s2-eth1 s2-eth2".split():
        class_change(port, rate)
    class_show("s1-eth1")


def class_change_switch_port(rate):
    """
    修改级联接口带宽
    :param rate:
    :return:
    """
    for port in "s1-eth3 s2-eth3 s3-eth2 s4-eth2".split():
        class_change(port, rate)
    class_show("s1-eth3")


def class_change(port, rate):
    os.popen("tc class change dev %s parent 1:fffe classid 1:1 htb rate %s" % (port, rate))
    os.popen("tc class change dev %s parent 1:fffe classid 1:2 htb rate %s" % (port, rate))
    os.popen("tc class change dev %s parent 1:fffe classid 1:3 htb rate %s" % (port, rate))


def class_show(port):
    print("".join(os.popen("tc class show dev %s" % port).readlines()))


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        print "Usage: %s help" % sys.argv[0]
        print "       %s <all|handle|class|filter|netem> [\"port1 port2 port3\"] ..." % sys.argv[0]
        print "       %s netem <TX_QUEUE_LEN> <delay> [\"port1 port2 port3\"] #netem 队列延时并不稳定" % sys.argv[0]
        print "       %s class host <rate>" % sys.argv[0]
        print "       %s class switch <rate>" % sys.argv[0]
        print "       example: %s netem 100 10.0ms [\"s1-eth3 s2-eth3\"] #设定默认链路队列/延时" % sys.argv[0]
        print "       example: %s netem 100 10.0ms \"s3-eth2 s4-eth2\" #设定特定链路队列/延时" % sys.argv[0]
        print "       example: %s class host 500mbit # 设定主机高速接口带宽" % sys.argv[0]
        print "       example: %s class switch 5mbit # 设定交换低速接口带宽" % sys.argv[0]
        exit(1)

    target_ports = "s1-eth3 s2-eth3"  # default ports

    if sys.argv[1] == "handle":
        for devname in sys.argv[2].split():
            handle_change(devname)
    elif sys.argv[1] == "netem":
        if len(sys.argv) >= 5:
            target_ports = sys.argv[4]
        for devname in target_ports.split():
            handle_change_netem(devname, queue_len=sys.argv[2], delay=sys.argv[3])
    elif sys.argv[1] == "red":
        for devname in target_ports.split():
            handle_change_red(devname, sys.argv[2])
    elif sys.argv[1] == "class":
        if sys.argv[2] == "host":
            class_change_hosts_port(sys.argv[3])
        else:
            class_change_switch_port(sys.argv[3])
    else:
        print "TODO: somthing will be done here .."
