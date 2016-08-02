# coding:utf-8


"""
ecn 测试 test_case 包含结果信息
"""
import os
from time import sleep
from mininet.log import info, debug, warn, error
from mininet.util import pmonitor
import ecn_util
import ecn_ovs_helper
import ecn_qdisc_helper

"""

调用参数: ecn_test_case.test_diff_ecn_red(net, duration=60)
ecn_test_case.test_diff_ecn_red_level2(net, duration=(1, 2, 3))  #

test01 无ecn测试
test02 有ecn测试

"""


def test01_04_ecn_red_diff_duration(network, bw=10, latency=50, qlen=200, duration=(5, 10, 15)):
    """
    将 test_diff_ecn_red 封装入更上一级的测试中去, 支持不同时长 duration 的多轮测试
    测试结果 ecn_result/2016-06-28_ecn_red.txt
    :param network:
    :param bw:
    :param latency:
    :param qlen:
    :param duration:
    :return:
    """
    results = {}
    for param in duration:  # 时延测试
        results[param] = test01_04_ecn_red(network, bw=bw, latency=latency, qlen=qlen, duration=param)
    for key in sorted(results.keys()):
        print "** 测试时长 %s seconds" % key
        ecn_util.dump_result(results[key])



def test11_base(network, testname, bw=10, latency=50, qlen=200, duration=10):
    """
    # 设置 使用 外部 ecn
    :param testname:    # 测试名称
    :param network:
    :param bw:          # 10Mbps 带宽
    :param latency:     # 50ms 延时
    :param qlen:        # 队列长度
    :param duration:    # 运行时间
    :return:
    """
    # print_mininet_objs(net)
    result_all = {}
    red_ecn = False

    def run_this_bench():
        return ecn_util.mesure_ping_and_netperf(network, round_count=1, round_duration=duration, ping_interval=0.1)

    # 无ecn测试 TEST01
    default_minmax = ""
    queue_setup_fullname = "%s ECN:%s qlen:%s bw:%sMbps lat:%sms no red:%s" % (
        testname, red_ecn, qlen, bw, latency, "")
    info("*** setup queue %s\n" % queue_setup_fullname)
    test01_06_setup_queue_and_latency(network, ecn=red_ecn, bw=bw, queue_len=qlen, latency=latency,
                                      redminmax=default_minmax)

    for min in [75000]:
        testfullname = "%s min:%s qlen:%s bw:%sMbps lat:%sms no red:%s" % (
            testname+str(min), min, qlen, bw, latency, "")
        info("*** setup ecn_ovs_helper (min= %s) for mod_ecn \n" % min)
        ecn_ovs_helper.init_switch()
        # ecn_ovs_helper.stop()
        # ecn_ovs_helper.start(min)
        # ecn_qdisc_helper.os_popen("/opt/mininet/cuc/ecn_ovs_helper.py new_red & " % min)
        info("*** running %s ...\n" % testfullname)
        result_all[min] = run_this_bench()

    ecn_util.dump_result(result_all)
    return result_all


def test01_04_ecn_red(network, bw=10, latency=50, qlen=200, duration=10):
    """

    测试结果记录在 ecn_result/2016-06-28_ecn_red.txt

    # 设置 使用 red ecn 以及不使用, 并使用 mesure_delay_and_output() 测试
    :param network:
    :param bw:          # 10Mbps 带宽
    :param latency:     # 50ms 延时
    :param qlen:        # 队列长度
    :param duration:    # 运行时间
    :return:
    """
    # print_mininet_objs(net)
    result_all = {}

    # result_all dict 追加入01 结果
    result_all.update(test01_base(network, "TEST01", bw=bw, latency=latency, qlen=qlen, duration=duration))

    # result_all dict 追加入03 04 05 结果
    for testname, redminmax in zip(["TEST02", "TEST03", "TEST04"],
                                   ["min 50000  max  150000 avpkt 1500",
                                    "min 65000  max  150000 avpkt 1500",
                                    "min 75000  max  150000 avpkt 1500"
                                    ]):
        # result_all = result1.copy()
        # if testname == "TEST02": continue
        result_all.update(
            test02_04_base_ecn_red(network, testname, redminmax, bw=bw, latency=latency, qlen=qlen, duration=duration))

    info("\n\n\n*** all result here ***\n\n\b")
    ecn_util.dump_result(result_all)
    return result_all


def test01_base(network, testname, bw=10, latency=50, qlen=200, duration=10):
    """
    # 设置 使用 red ecn 以及不使用, 并使用 mesure_delay_and_output() 测试
    :param testname:    # 测试名称
    :param network:
    :param bw:          # 10Mbps 带宽
    :param latency:     # 50ms 延时
    :param qlen:        # 队列长度
    :param duration:    # 运行时间
    :return:
    """
    # print_mininet_objs(net)
    result = {}
    red_ecn = False

    def run_this_bench():
        return ecn_util.mesure_ping_and_netperf(network, round_count=1, round_duration=duration, ping_interval=0.1)

    # 无ecn测试 TEST01
    default_minmax = ""
    testfullname = "%s ECN:%s qlen:%s bw:%sMbps lat:%sms no red:%s" % (
        testname, red_ecn, qlen, bw, latency, "")
    info("*** setup %s\n" % testfullname)
    test01_06_setup_queue_and_latency(network, ecn=red_ecn, bw=bw, queue_len=qlen, latency=latency,
                                      redminmax=default_minmax)
    info("*** running %s ...\n" % testfullname)
    result[testfullname] = run_this_bench()

    ecn_util.dump_result(result)
    return result


def test02_04_base_ecn_red(network, testname, redminmax, bw=10, latency=50, qlen=200, duration=10):
    """
    独立复制出的 03 04 实验, 用于enc抓包测试
    :param redminmax:      # red参数设置
    :param testname:       # 测试名称
    :param network:
    :param bw:
    :param latency:
    :param qlen:
    :param duration:
    :return:
    """

    result = {}

    def run_this_bench():
        return ecn_util.mesure_ping_and_netperf(network, round_count=1, round_duration=duration, ping_interval=0.1)

    # ecn 参数变化测试 02 03 04
    testfullname = "%s ECN:%s qlen:%s bw:%sMbps lat:%sms redminmax:%s" % (
        testname, True, qlen, bw, latency, redminmax)
    info("*** setup %s \n" % testfullname)
    test01_06_setup_queue_and_latency(network, ecn=True, bw=bw, queue_len=qlen, latency=latency,
                                      redminmax=redminmax)
    info("*** running %s ...\n" % testfullname)
    result[testfullname] = run_this_bench()

    ecn_util.dump_result(result)
    return result


def test01_06_setup_queue_and_latency(network, ecn=True, bw=10, queue_len=200, latency=50,
                                      redminmax="min 30000 max 35000 avpkt 1500"):
    # 从 base 中扩展出的实验拓扑设置; 采用 bw=10, qlen=200, latency=50 固定参数进行测试,

    ecn_util.base_setup_queue_and_latency(network, bw=bw, queue_len=queue_len, latency=latency, ecn=ecn,
                                          redminmax=redminmax)


def test_ping_with_background_traffice(network, round_count=1, round_duration=5, ping_interval=1.0, background=True):
    """
    h1 执行 ping 测试延时
    h2 执行 netperf 测试带宽利用率
    :param background:
    :param network: mininet class
    :param round_count:    循环次数
    :param round_duration: 循环时间每轮
    :param ping_interval:  ping包采样间隔
    :return:
    """
    result = ""
    h1 = network.get("h1")
    popens = {}
    if background:  # backgroud traffice, 每轮增加10秒时延
        h1.cmd("netperf -H h3 -l %s &" % (round_count * (round_duration + 5)))
    sleep(3)  # wait 2 second to reach tcp max output
    for r in range(round_count):
        print ("*** ROUND %s" % r)
        for h in [h1]:
            ping_cmd = "ping -c%s -i%s h3 " % (int(round_duration / ping_interval), ping_interval)
            info("<%s>: popen cmd: %s \n" % (h.name, ping_cmd))
            popens[h] = h.popen(ping_cmd)

        # Monitor them and print output
        for host, line in pmonitor(popens):
            if host:
                if line.find("icmp_seq") != -1:
                    debug("<%s>: %s\n" % (host.name, line.strip()))  # suppressed ping output to debug level
                else:
                    info("<%s>: %s\n" % (host.name, line.strip()))
                    result += "<%s>: %s\n" % (host.name, line.strip())

    debug("\n".join(os.popen('tc -s -d qdisc show dev s1-eth3').readlines()))
    return result
