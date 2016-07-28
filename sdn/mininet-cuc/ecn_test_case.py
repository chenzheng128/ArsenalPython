# coding:utf-8


"""
ecn 测试 test_case 包含结果信息
"""
import os
from time import sleep
from mininet.log import info, debug, warn, error
from mininet.util import pmonitor
from ecn_util import mesure_ping_and_netperf, setup_queue_and_filter, dump_result

"""

调用参数: ecn_test_case.test_diff_ecn_red(net, duration=60)
ecn_test_case.test_diff_ecn_red_level2(net, duration=(1, 2, 3))  #

"""


def test_diff_ecn_red_2016_06_28(network, bw=10, latency=50, qlen=200, duration=(5, 10, 15)):
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
        results[param] = test_diff_ecn_red(network, bw=bw, latency=latency, qlen=qlen, duration=param)
    for key in sorted(results.keys()):
        print "** 测试时长 %s seconds" % key
        dump_result(results[key])

"""

调用参数: ecn_test_case.test_diff_ecn_red(net, duration=60)

**** 测试结果 	 result ***
ECN:False qlen:200 bw:10Mbps lat:50ms	<h1>: PING h3 (10.0.0.3) 56(84) bytes of data.
<h1>:
<h1>: --- h3 ping statistics ---
<h1>: 600 packets transmitted, 580 received, 3% packet loss, time 61027ms
<h1>: rtt min/avg/max/mdev = 100.216/375.909/587.119/99.584 ms, pipe 6
<h2>: MIGRATED TCP STREAM TEST from 0.0.0.0 (0.0.0.0) port 0 AF_INET to h3 () port 0 AF_INET : demo
<h2>: Recv   Send    Send
<h2>: Socket Socket  Message  Elapsed
<h2>: Size   Size    Size     Time     Throughput
<h2>: bytes  bytes   bytes    secs.    10^6bits/sec
<h2>:
<h2>: 87380  87380  87380    62.96       9.42

*** 测试结果 	 result ***
ECN:True qlen:200 bw:10Mbps lat:50ms redminmax:min 30000 max 35000 avpkt 1500
<h1>: PING h3 (10.0.0.3) 56(84) bytes of data.
<h1>:
<h1>: --- h3 ping statistics ---
<h1>: 600 packets transmitted, 597 received, 0% packet loss, time 60600ms
<h1>: rtt min/avg/max/mdev = 100.189/110.219/129.141/7.406 ms, pipe 2
<h2>: MIGRATED TCP STREAM TEST from 0.0.0.0 (0.0.0.0) port 0 AF_INET to h3 () port 0 AF_INET : demo
<h2>: Recv   Send    Send
<h2>: Socket Socket  Message  Elapsed
<h2>: Size   Size    Size     Time     Throughput
<h2>: bytes  bytes   bytes    secs.    10^6bits/sec
<h2>:
<h2>: 87380  87380  87380    60.42       9.29

ECN:True qlen:200 bw:10Mbps lat:50ms redminmax:min 45000 max 50000 avpkt 1500
<h1>: PING h3 (10.0.0.3) 56(84) bytes of data.
<h1>:
<h1>: --- h3 ping statistics ---
<h1>: 600 packets transmitted, 600 received, 0% packet loss, time 60494ms
<h1>: rtt min/avg/max/mdev = 100.165/118.009/142.847/10.934 ms, pipe 2
<h2>: MIGRATED TCP STREAM TEST from 0.0.0.0 (0.0.0.0) port 0 AF_INET to h3 () port 0 AF_INET : demo
<h2>: Recv   Send    Send
<h2>: Socket Socket  Message  Elapsed
<h2>: Size   Size    Size     Time     Throughput
<h2>: bytes  bytes   bytes    secs.    10^6bits/sec
<h2>:
<h2>: 87380  87380  87380    60.74       9.24

ECN:True qlen:200 bw:10Mbps lat:50ms redminmax:min 60000 max 65000 avpkt 1500
<h1>: PING h3 (10.0.0.3) 56(84) bytes of data.
<h1>:
<h1>: --- h3 ping statistics ---
<h1>: 600 packets transmitted, 598 received, 0% packet loss, time 60407ms
<h1>: rtt min/avg/max/mdev = 100.176/127.282/152.700/13.584 ms, pipe 2
<h2>: MIGRATED TCP STREAM TEST from 0.0.0.0 (0.0.0.0) port 0 AF_INET to h3 () port 0 AF_INET : demo
<h2>: Recv   Send    Send
<h2>: Socket Socket  Message  Elapsed
<h2>: Size   Size    Size     Time     Throughput
<h2>: bytes  bytes   bytes    secs.    10^6bits/sec
<h2>:
<h2>: 87380  87380  87380    60.53       9.37

测试结果    |无red ecn| 有redmimmax条件1| 条件2  | 条件3
-----------|-----|--------|-----
bw:        |9.42M|9.29M| 9.24M  | 9.37M
ping avg:  |375ms|110ms| 118ms  | 127ms
ping mdev: | 99ms|7.4ms| 10.9ms | 13.6ms

分析: 打开ECN前后Throughput 从 9.4 下降到 8.2 (burst 20), 但是 ping 的 /max/mdev 变化很大, mdev从 99 ms 下降到 7 ms
而且在条件2测试时, red minmax 设置不当时, 可能会出现ping延时和throughput同时变差的情况.
"""


def test_diff_ecn_red(network, bw=10, latency=50, qlen=200, duration=10):
    """
    # 设置 使用 red ecn 以及不使用, 并使用 mesure_delay_and_output() 测试
    :param network:
    :param bw:          # 10Mbps 带宽
    :param latency:     # 50ms 延时
    :param qlen:        # 队列长度
    :param duration:    # 运行时间
    :return:
    """
    # print_mininet_objs(net)
    result1 = {}

    def run_this_bench():
        return mesure_ping_and_netperf(network, round_count=1, round_duration=duration, ping_interval=0.1)

    # 有无ecn测试
    for ecn in [True, False]:
        default_minmax = "min 30000 max 35000 avpkt 1500"
        setup_queue_and_filter(network, ecn=ecn, bw=bw, latency=latency, queue_len=qlen, redminmax=default_minmax)
        result1["ECN:%s qlen:%s bw:%sMbps lat:%sms redminmax:%s" % (
            ecn, qlen, bw, latency, default_minmax)] = run_this_bench()
        if ecn:
            print

    # ecn 参数变化测试
    for redminmax in ["min 45000 max 50000 avpkt 1500", "min 60000 max 65000 avpkt 1500"]:
        setup_queue_and_filter(network, ecn=True, bw=bw, latency=latency, queue_len=qlen, redminmax=redminmax)
        result1[
            "ECN:%s qlen:%s bw:%sMbps lat:%sms redminmax:%s" % (True, qlen, bw, latency, redminmax)] = run_this_bench()

    dump_result(result1)
    return result1


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
