# coding:utf-8

"""
ecn result 常用工具类
"""
import os
import re
from time import sleep
import numpy
from mininet.log import MininetLogger, debug, info, warn, error


def average_result(results):
    """
    通过regrexp计算多次运行结果的平均值
    :param results:
    """
    # regex online测试连接:
    # https://regex101.com/r/dI4kI6/1
    pattern_throughput = re.compile(r"<*>:\s+\d+\s+\d+\s+\d+\s+[\.\d]+\s+([\.\d]+)")  # 匹配两位数字
    # https://regex101.com/r/gN6vD2/2
    pattern_ping = re.compile(r"<*>: rtt min/avg/max/mdev = ([\.\d]+)/([\.\d]+)/([\.\d]+)/([\.\d]+)")  # 匹配两位数字
    throughputs = []
    ping_mins = []
    ping_avgs = []
    ping_maxs = []
    ping_mdevs = []

    # for key in results.keys():
    # single_result = results[key]
    for single_result in results:
        # print "传入结果为: ", single_result
        # lists = [throughputs, ping_mins, ping_avgs, ping_maxs, ping_mdevs]
        # patterns = []
        # for p,

        match = pattern_throughput.search(single_result)
        if match:
            throughputs.append(float(match.group(1)))

        match = pattern_ping.search(single_result)
        if match:
            ping_mins.append(float(match.group(1)))
            ping_avgs.append(float(match.group(2)))
            ping_maxs.append(float(match.group(3)))
            ping_mdevs.append(float(match.group(4)))

    print "*** 平均结果 \n average_result:        avg     [details] "

    print "{0:10s} {1:15.2f} Mbps {2:30s}".format("throughputs", numpy.mean(throughputs), throughputs)
    print "{0:10s} {1:15.2f} ms   {2:30s}".format("ping_avgs", numpy.mean(ping_avgs), ping_avgs)
    print "{0:10s} {1:15.2f} ms   {2:30s}".format("ping_medvs", numpy.mean(ping_mdevs), ping_mdevs)



example_result = """
如果有一些分析错误的结果可以粘贴到这里, 以 !!! 作为分割符, 便于查看运行结果
*** 测试结果   result ***
sdn_ecn openflow-ecn_ip-80000 min:80000 qlen:200 bw:10Mbps lat:50ms no red: <h1>: PING h3 (10.0.0.3) 56(84) bytes of data.
<s1>: start ecn_ip policy ...
<s1>: ecn_ovs_helper duration=130(s) qmin=80000 filter_interval=1ms sleep_interval=2.5ms ...
<h2>: MIGRATED TCP STREAM TEST from 0.0.0.0 (0.0.0.0) port 0 AF_INET to h3 () port 0 AF_INET : demo
<h2>: Recv   Send    Send
<h2>: Socket Socket  Message  Elapsed
<h2>: Size   Size    Size     Time     Throughput
<h2>: bytes  bytes   bytes    secs.    10^6bits/sec
<h2>:
<h2>: 87380  87380  87380    122.67      6.74
<s1>: ecn_ovs_helper 到达结束时间 130 s, bybye.
<h1>:
<h1>: --- h3 ping statistics ---
<h1>: 1200 packets transmitted, 1200 received, 0% packet loss, time 121340ms
<h1>: rtt min/avg/max/mdev = 100.096/154.587/415.598/56.042 ms, pipe 4
!!!

sdn_ecn openflow-ecn_ip-80001 min:80001 qlen:200 bw:10Mbps lat:50ms no red: <h1>: PING h3 (10.0.0.3) 56(84) bytes of data.
<s1>: start ecn_ip policy ...
<s1>: ecn_ovs_helper duration=130(s) qmin=80001 filter_interval=1ms sleep_interval=2.5ms ...
<h2>: MIGRATED TCP STREAM TEST from 0.0.0.0 (0.0.0.0) port 0 AF_INET to h3 () port 0 AF_INET : demo
<h2>: Recv   Send    Send
<h2>: Socket Socket  Message  Elapsed
<h2>: Size   Size    Size     Time     Throughput
<h2>: bytes  bytes   bytes    secs.    10^6bits/sec
<h2>:
<h2>: 87380  87380  87380    122.57      6.81
<s1>: ecn_ovs_helper 到达结束时间 130 s, bybye.
<h1>:
<h1>: --- h3 ping statistics ---
<h1>: 1200 packets transmitted, 1200 received, 0% packet loss, time 121463ms
<h1>: rtt min/avg/max/mdev = 100.081/146.297/270.129/36.347 ms, pipe 3
!!!

sdn_ecn openflow-ecn_ip-80002 min:80002 qlen:200 bw:10Mbps lat:50ms no red: <h1>: PING h3 (10.0.0.3) 56(84) bytes of data.
<s1>: start ecn_ip policy ...
<s1>: ecn_ovs_helper duration=130(s) qmin=80002 filter_interval=1ms sleep_interval=2.5ms ...
<h2>: MIGRATED TCP STREAM TEST from 0.0.0.0 (0.0.0.0) port 0 AF_INET to h3 () port 0 AF_INET : demo
<s1>: ecn_ovs_helper 到达结束时间 130 s, bybye.
<h2>: Recv   Send    Send
<h2>: Socket Socket  Message  Elapsed
<h2>: Size   Size    Size     Time     Throughput
<h2>: bytes  bytes   bytes    secs.    10^6bits/sec
<h2>:
<h2>: 87380  87380  87380    122.07      5.99
<h1>:
<h1>: --- h3 ping statistics ---
<h1>: 1200 packets transmitted, 1200 received, 0% packet loss, time 121342ms
<h1>: rtt min/avg/max/mdev = 100.085/141.070/276.333/37.933 ms, pipe 3

"""

"""
sdn_ecn openflow-ecn_ip-80000 min:80000 qlen:200 bw:10Mbps lat:50ms no red:
<h1>: PING h3 (10.0.0.3) 56(84) bytes of data.
<s1>: start ecn_ip policy ...
<s1>: ecn_ovs_helper duration=15(s) qmin=80000 filter_interval=1ms sleep_interval=2.5ms ...
<h1>:
<h1>: --- h3 ping statistics ---
<h1>: 50 packets transmitted, 50 received, 0% packet loss, time 5018ms
<h1>: rtt min/avg/max/mdev = 100.154/240.588/414.194/110.921 ms, pipe 4
<h2>: MIGRATED TCP STREAM TEST from 0.0.0.0 (0.0.0.0) port 0 AF_INET to h3 () port 0 AF_INET : demo
<h2>: Recv   Send    Send
<h2>: Socket Socket  Message  Elapsed
<h2>: Size   Size    Size     Time     Throughput
<h2>: bytes  bytes   bytes    secs.    10^6bits/sec
<h2>:
<h2>: 87380  87380  87380    6.62        8.59
<s1>: ecn_ovs_helper 到达结束时间 15 s, bybye.
!!!

"""


if __name__ == "__main__":
    print "test ecn_utl.py"
    average_result(example_result.split("!!!"))
