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
from mininet.log import MininetLogger

LOG = MininetLogger()

def port_default_config(port, bw=50, tx_queue_len=100):
    os_popen("tc qdisc del dev %s root" % port)
    os.popen("tc qdisc add dev %s root handle 1: htb default 2" % port)  # 将流量默认到 2 号接口上
    os_popen("tc class add dev %s parent 1: classid 1:fffe htb rate 10000mbit burst 1250b cburst 1250b" % port)
    os_popen("tc class add dev %s parent 1:fffe classid 1:1 htb rate %smbit burst 1563b cburst 1563b" % (port, bw))
    os_popen("tc class add dev %s parent 1:fffe classid 1:2 htb rate %smbit burst 1563b" % (port, bw))
    os_popen("tc class add dev %s parent 1:fffe classid 1:3 htb rate %smbit burst 1563b" % (port, bw))

    # os_popen("tc qdisc del dev %s root" % port)
    os_popen("tc qdisc add dev %s parent 1:1 handle 1: pfifo limit %s" % (port, tx_queue_len))
    os_popen("tc qdisc add dev %s parent 1:2 handle 2: pfifo limit %s" % (port, tx_queue_len))
    os_popen("tc qdisc add dev %s parent 1:3 handle 3: pfifo limit %s" % (port, tx_queue_len))

    # 放置 class filter
    os_popen("tc filter del dev %s parent 1: protocol ip pref 1 u32" % port)
    u32_filter_prefix = "tc filter add dev %s protocol ip parent 1:0 prio 1 u32" % port
    os_popen('%s match ip dport 12856 0xffff flowid 1:1' % u32_filter_prefix)  # netperf 到队列2
    os_popen('%s match ip dport 5001 0xffff flowid 1:2' % u32_filter_prefix)  # iperf 5001/5002 到队列2
    os_popen('%s match ip dport 5002 0xffff flowid 1:2' % u32_filter_prefix)
    os_popen('%s match ip dport 5003 0xffff flowid 1:3' % u32_filter_prefix)
    os_popen('%s match ip dport 5003 0xffff flowid 1:3' % u32_filter_prefix)
    os_popen('%s match ip src 10.0.0.1/32 flowid 1:2' % u32_filter_prefix)  # 把h1所有包 match 到队列2
    os_popen('%s match ip protocol 1 0xff flowid 1:2' % u32_filter_prefix)  # 把icmp所有包 match 到队列2
    LOG.debug("  设置端口 %s 完成 ...\n" % port)
    LOG.debug(" 检查设置: tc filter show dev $NDEV parent 1:fffe\n")


def handle_change(port):
    # handle_change_prio(port, tx_queue_len)
    handle_change_netem(port, 100, "20.0")
    pass


def handle_del(port):
    os_popen("tc qdisc del dev %s parent 1:2 handle 2:" % port)


def handle_show(port):
    # 查看 handle
    print("".join(os_popen("tc -s qdisc show dev %s" % port).readlines()))


def os_popen(cmd):
    LOG.debug(cmd + "\n")
    return os.popen(cmd)


def handle_change_netem(port, queue_len=100, delay="10.0ms"):
    # 修改为 prio handle
    handle_del(port)
    os_popen(cmd="tc qdisc add dev %s parent 1:2 handle 2: netem limit %s delay %s" % (port, queue_len, delay))
    handle_show(port)


def handle_change_prio(port, queue_len=100):
    handle_del(port)
    os_popen("tc qdisc add dev %s parent 1:2 handle 2: pfifo limit %s" % (port, queue_len))
    handle_show(port)


def handle_change_red(port, queue_len=10000):
    # 队列2 采用RED队列, 支持 早期随机mark为ecn的方式
    handle_del(port)
    os_popen("tc qdisc add dev %s parent 1:2 handle 2: red limit %s min 50000 max 150000 avpkt 1000 ecn" % (
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
    os_popen("tc class change dev %s parent 1:fffe classid 1:1 htb rate %s" % (port, rate))
    os_popen("tc class change dev %s parent 1:fffe classid 1:2 htb rate %s" % (port, rate))
    os_popen("tc class change dev %s parent 1:fffe classid 1:3 htb rate %s" % (port, rate))


def class_show(port):
    print("".join(os_popen("tc class show dev %s" % port).readlines()))


def qos_print_help():
    LOG.info("查看 tc qdisc")
    LOG.info("  普通 pfifo_fast 接口 s3-eth1 状态为:  tc qdisc show dev s3-eth1\n")
    LOG.debug("\n".join(os_popen('tc qdisc show dev s3-eth1').readlines()))
    print "  查看 netem 延时链路 s3-eth2 <->s4-eth1 接口状态为:  tc qdisc show dev s3-eth2 / s4-eth1"
    LOG.debug("\n".join(os_popen('tc qdisc show dev s3-eth2').readlines()))
    LOG.debug("\n".join(os_popen('tc qdisc show dev s4-eth1').readlines()))
    print "  查看 htb qdisc 队列接口 s1-eth3, tc qdisc show dev $NDEV (采用的应是 htb, 而不是 pfifo_fast(普通) 或 netem(延时) )"
    LOG.debug("\n".join(os_popen('tc qdisc show dev s1-eth3').readlines()))
    print "  查看 htb class 队列接口 s1-eth3,  tc class show dev $NDEV"
    LOG.debug("\n".join(os_popen('tc class show dev s1-eth3').readlines()))
    print "  查看 htb filter 队列接口 s1-eth3,  tc filter show dev $NDEV parent 1:0"
    LOG.debug("\n".join(os_popen('tc filter show dev s1-eth3 parent 1:0').readlines()))

    print "拥塞测试方法:"
    print " 设置 iperf server 测速: h3(xterm)>  iperf -s -p 5002 -m # 监听在5002端口, 会被 tc filter 匹配到队列2中 "
    print " 连接 iperf client 测速: h1(xterm)> iperf -c h3 -p 5002 -i 3 -t 60 -M 500 -m #以MSS500 发送数据流量"
    print " 应当流量都在队列2 class 1:2 中处理. 如修改端口号为 5003 则在 1:3 队列处理"
    print " 如 iperf -b 带宽超过QoS瓶颈之上, 应该能看到当前队列增加 ( backlog 100p ) 至TX_QUEUELEN后, 丢包(dropped)数开始增加"
    print " 当发送流量过高 时, s1-eth3 发生拥塞"
    print "   检查端口拥塞状态: s1(xterm)> watch -n 0.1 tc -s -d qdisc show dev s1-eth3 "
    print "队列2 qdisc 的修改方法 "
    print "  - 先删除: tc qdisc delete dev $NDEV parent 1:2 handle 2: ; \ "
    print "  - 再新增RED: " \
          "tc qdisc add dev $NDEV parent 1:2 handle 2: red limit 200000 min 50000 max 150000 avpkt 1000 ecn"


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
