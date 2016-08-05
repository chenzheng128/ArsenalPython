#!/usr/bin/python
# --*-- coding:utf-8 --*--

"""
ecn ovs_vsctl 的快捷脚本

封装命令脚本
http://openvswitch.org/support/dist-docs/ovs-vsctl.8.txt

http://openvswitch.org/support/dist-docs/ovs-ofctl.8.txt
 mod_nw_ecn:ecn
                     Sets  the  ECN bits in the IPv4 ToS or IPv6 traffic class
                     field to ecn, which must be a  value  between  0  and  3,
                     inclusive.  This action does not modify the six most sig‐
                     nificant bits of the field (the DSCP bits).

https://en.wikipedia.org/wiki/Explicit_Congestion_Notification
ecn codepoints
0 00 – Non ECN-Capable Transport, Non-ECT
2 10 – ECN Capable Transport, ECT(0)
1 01 – ECN Capable Transport, ECT(1)
3 11 – Congestion Encountered, CE.

** new cmd
# add and del
/opt/coding/ovs/utilities/ovs-ofctl -O Openflow13 once 0 del
# add only
/opt/coding/ovs/utilities/ovs-ofctl -O Openflow13 once 0 nodel

** original cmd
*** start drop
/opt/coding/ovs/utilities/ovs-ofctl -O Openflow13 add-flow s1 "tcp,nw_dst=10.0.0.3, actions=drop"
/opt/coding/ovs/utilities/ovs-ofctl -O Openflow13 del-flows s1 "tcp,nw_dst=10.0.0.3"
*** start ecn
ovs-ofctl -O Openflow13 add-flow s1 "tcp,nw_dst=10.0.0.3, actions=mod_nw_ecn:3, resubmit(,1)"
ovs-ofctl -O Openflow13 del-flows s1 "tcp,nw_dst=10.0.0.3"
"""
import math
import os
import sys
import time
import re
from mininet.log import MininetLogger, debug, info, warn, error
from ecn_qdisc_helper import os_popen
import ecn_qdisc_helper

LOG = MininetLogger()
OFCTL_BIN = "/usr/local/bin/ovs-ofctl"
OFCTL_BIN_MY = "/opt/coding/ovs/utilities/ovs-ofctl"
OFCTL_OPT = "-O Openflow13"
OFCTL_CMD = "%s %s" % (OFCTL_BIN, OFCTL_OPT)
OFCTL_CMD_MY = "%s %s" % (OFCTL_BIN_MY, OFCTL_OPT)


def switch_ecn_mod():
    """
    执行切换操作后, 通过 wireshark filter: ip.dsfield.ecn == 3 可以看到发生改变的ip包
    一次切换 tcp 包为 11-13个, 时间在 15ms-20ms 左右
    :return:
    """
    mod_ecn_ce()
    mod_ecn_ect()


def switch_ecn_quick(interval_ms=0):
    """
    :param interval_ms : 用于 filter 的interval, 时间越长, 修改包的数量越多
    用我们自己修改的 OFCTL_CMD_MY, 更加快速
    :return:
    """
    os_popen("%s once %s del" % (OFCTL_CMD_MY, interval_ms * 1000))


def switch_ecn_add():
    """
    比较友好的 ecn 方法
    :return:
    """
    os_popen('%s add-flow s1 "%s,nw_dst=10.0.0.3, actions=mod_nw_ecn:3, resubmit(,1)"' % (OFCTL_CMD, "tcp"))
    # 不去除mod_ecn策略的话, 带宽始终上不来, 维持在 0.5Mbps 左右
    os_popen('%s del-flows s1 "%s,nw_dst=10.0.0.3"' % (OFCTL_CMD, "tcp"))


def switch_drop():
    """
    最生猛的 切换 drop 策略大法, 流量绝对走不起来
    :return:
    """
    os_popen('%s add-flow s1 "%s,nw_dst=10.0.0.3, actions=drop"' % (OFCTL_CMD, "tcp"))
    os_popen('%s del-flows s1 "%s,nw_dst=10.0.0.3"' % (OFCTL_CMD, "tcp"))


def mod_ecn_ce():
    return mod_ecn(3)


def mod_ecn_ect():
    return mod_ecn(2)


def mod_ecn(value):
    os_popen("%s mod-flows s1 \"tcp,nw_dst=10.0.0.3, actions=mod_nw_ecn:%s, resubmit(,1)\"" % (OFCTL_CMD, value))
    os_popen("%s mod-flows s1 \"ip,nw_dst=10.0.0.3, actions=mod_nw_ecn:%s, resubmit(,1)\"" % (OFCTL_CMD, value))


def dump_flows():
    info("*** dump-flows \n")
    debug("".join(os.popen('%s dump-flows s1 %s'
                           % (OFCTL_CMD, "")).readlines()))


def init_switch():
    info("*** 初始化交换机 OpenFlow13 协议支持 \n")
    os_popen("ovs-vsctl set bridge s1 protocols=OpenFlow10,OpenFlow13 # 设置s1 交换机 openflow 13 协议支持")
    debug("".join(os.popen("ovs-vsctl list bridge s1 # | grep protocols #查看s1交换机现有协议").readlines()))

    # 初始化 table=0 中的 ip/tcp ecn mod 流 mod之后提交到table=1转发;
    # info("*** add 2 flow in table=0 for ecn ip/tcp #  这里 add-flow之后, 将来作 mod-flows 操作即可 \n")
    # for protocol in ["ip", "tcp"]:
    #    os_popen('%s add-flow s1 "%s,nw_dst=10.0.0.3, actions=mod_nw_ecn:%s, resubmit(,1)"' % (OFCTL_CMD, protocol, 1))


def stop():
    pass


def start_opeflow_ecn(queue_min, sleep_interval, ecn_policy=True, quick=True, run_duration=10):
    """
    自定义的 red 函数, 通过监控队列, 对ecnjixn
    :param queue_min:      触发策略的最小队列
    :param sleep_interval: 查询间隔
    :param ecn_policy:            使用 ecn 或是 drop 策略
    :param quick 使用自编译的 ovs-ofctl 作高效控制
    :param run_duration 运行秒数
    :return:
    """
    init_switch()

    pattern = re.compile(r"backlog (\d\d+)b (\d\d+)p")  # 匹配两位数字
    search_count = 0
    queue_exceed_count = 1
    start_second = time.time()
    while True:
        # class_status = (ecn_qdisc_helper.class_get("s1-eth3", "1:2"))
        queue_status = ecn_qdisc_helper.handle_get("s1-eth3")
        # debug("%s\n", queue_status)
        # queue_status = ""
        # debug("type:%s, %s" % (type(class_status), class_status))
        # match = re.search(r'hello', 'i am 1hello world!')
        match = pattern.search(queue_status)
        search_count += 1
        filter_ms_base = 1
        if (time.time() - start_second) > run_duration:
            info("到达结束时间 %s s, bybye. \n" % run_duration)
            break
        if match:
            # print ("%sp" % match.group(2))
            qsize = int(match.group(1))
            qlen = int(match.group(2))
            # if (search_count * sleep_interval) % 3 == 0:  # supressing to 1 output / per 1 seconds
            # debug(" %sb %sp " % (qsize, qlen))
            if qsize > queue_min:
                # pass
                queue_exceed_count += 1
                exceed_second = time.time() - start_second

                if ecn_policy:
                    if quick:
                        # filter_ms =  min( int( (qsize - queue_min) / float(queue_min) *  filter_ms_base), 3)
                        filter_ms = 3.5  # 固定 filter 间隔
                        info("%3.3fs NO.%4s queue_min %s filter %sms exceeded  (%sb %sp) \n" % (
                    exceed_second, queue_exceed_count, queue_min, filter_ms, qsize, qlen))
                        switch_ecn_quick(interval_ms=filter_ms)
                    else:
                        switch_ecn_add()
                        # pass
                else:
                    switch_drop()
                # mod_ecn(3)
                # if (qsize - queue_min) / float(queue_min) < 0.1:  # 如果超出的队列不多, 考虑减少发包控制
                #    time.sleep(sleep_interval)  # 每次修改后至少休息一下, 避免重复提交
                # continue
        else:
            # print "not maching"
            pass
        time.sleep(sleep_interval)


def print_usage(argv):
    print "Usage: %s help 初始化, 切换ecn状态# " % argv[0]
    print "       %s new_red  #新 openflow red 策略" % argv[0]
    print "       %s mod [code] #修改ecncode" % argv[0]
    print "       %s switch  #切换ecn策略" % argv[0]
    print "       %s init  #初始化交换机为 openflow13, 加入初始 mod_nw_ecn 流" % argv[0]
    print "       %s dump  #显示流" % argv[0]
    print "       %s start <queue_min> <duration> # 启动 ecn 策略  " % argv[0]

    print "       example: %s mod_ecn [1|2|3]" % argv[0]


if __name__ == "__main__":

    LOG.setLogLevel("info")
    LOG.setLogLevel("debug")

    if len(sys.argv) <= 1:
        print_usage(sys.argv)
        exit(1)

    if sys.argv[1] == "switch":
        switch_ecn_add()
    elif sys.argv[1] == "init":
        init_switch()
        dump_flows()
    elif sys.argv[1] == "dump":
        dump_flows()
    elif sys.argv[1] == "start":
        ecn = True
        duration = 10
        if len(sys.argv) != 4:  # and sys.argv[2] == "drop":
            print_usage(sys.argv)
            exit(1)
            # ecn = False
            # print "start drop policy ... "
        qmin = int(sys.argv[2])
        duration = int(sys.argv[3])

        print "start ecn policy qmin %s duration %s(s)..." % (qmin, duration)
        start_opeflow_ecn(queue_min=qmin, sleep_interval=0.0025, ecn_policy=ecn, run_duration=duration)
    elif sys.argv[1] == "mod":
        code = 1
        if len(sys.argv) >= 3:
            code = int(sys.argv[2])
        mod_ecn(code)
    else:
        print_usage(sys.argv)
