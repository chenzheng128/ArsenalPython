# !/usr/bin/python
# --*-- coding:utf-8 --*--


"""
origined from 海龙拓扑测试
revised by zhchen
Usage:
sudo mn -c ; sudo python cuc/hailong_remote.original.py
"""
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, MininetLogger
from mininet.node import RemoteController, OVSSwitch
from mininet.node import OVSController, Controller
from mininet.cli import CLI
import threading
import os
import threading
import time
import json
from signal import SIGINT, SIGKILL
from mininet.link import TCLink

flags1 = False
flags2 = False
global popens

TX_QUEUE_LEN = 100  # 网卡队列长度设置

# 实验拓扑的相关网卡 s1/s2 host-switch, s3/s4 middle-switch

# 主机端口
HOST_PORT = " h1-eth0 h2-eth0 h3-eth0 h4-eth0"
# 交换机连主机端口
SW_HOST_PORTS = "s1-eth1 s1-eth2 s1-eth3 s2-eth1 s2-eth2 s2-eth3"

# 所有主机端口 = 交换机连主机端口 + 主机端口
# ALL_HOST_PORTS = SW_HOST_PORTS + HOST_PORT
# 所有端口 = 交换机连主机端口 + 交换机级联端口
ALL_PORTS = SW_HOST_PORTS + " s3-eth1 s3-eth2 s4-eth1 s4-eth2"

LOG = MininetLogger()


class QbbTopo(Topo):
    """
    Qbb experiment test topology
    @ZHL@CUC@2015.12.26"
    拓扑图: https://www.processon.com/view/link/5752d7f1e4b0695484404d39
    """

    def build(self):
        """
        建立哑铃拓扑, 网卡顺序为对称
        """

        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')

        h1 = self.addHost('h1', inNamespace=True)
        h2 = self.addHost('h2', inNamespace=True)
        h3 = self.addHost('h3', inNamespace=True)
        h4 = self.addHost('h4', inNamespace=True)

        # mininet> link # 查看网卡连接

        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(s1, s3)

        self.addLink(h3, s2) # 优化网卡顺序, 与s1 主机接口对应
        self.addLink(h4, s2)
        self.addLink(s2, s4)

        """
        # s3 <-> s4 查看 含延时链路状态 )
        tc qdisc show dev s3-eth2
        tc class show dev s3-eth2
        """
        self.addLink(s3, s4, delay='10ms', use_htb=True) # 最后连接 s3 s4 优化网卡顺序


def qbb_test():
    """
    :return:
    Create and test our QBB network standard"
    """

    # LOG.setLogLevel("debug") #打开 debug 日志

    qbb_topo = QbbTopo()
    global net
    # MMininet 类 API 参考: http://mininet.org/api/classmininet_1_1net_1_1Mininet.html#a1ed0f0c8ba06a398e02f3952cc4c8393
    # 命令行参数对应 --mac => autoSetMacs
    net = Mininet(topo=qbb_topo, controller=None, link=TCLink, autoSetMacs=True, xterms=True)

    c0 = Controller('c0', port=6633)
    # net.addController('c0', controller=RemoteController, ip='192.168.57.2', port=6653)
    net.addController(c0)
    net.start()

    # 调整队列大小
    print "调整下列端口的 txqueuelen 网络队列大小为 %s ..." % TX_QUEUE_LEN
    for port in ALL_PORTS.split():
        print "  %s" % port,
        LOG.debug("  调整 %s 网络 队列长度 txqueuelen: sudo ip link set txqueuelen %s dev %s ..." % (port, TX_QUEUE_LEN, port))
        os.popen("sudo ip link set txqueuelen %s dev %s" % (TX_QUEUE_LEN, port))
    print " 检查设置: ifconfig | grep txqueuelen"

    print "使用 ovs-vsctl 创建 s2 s3  哑铃拓扑的流量策略, 主机接口带宽大 big_link, \n" \
          "   交换机接口流量带宽小 small_lin. QoS 策略 ( tc htb qdisc ), "

    os.popen("""sudo ovs-vsctl \
        -- set port s1-eth3 qos=@small_link \
        -- set port s2-eth3 qos=@small_link \
        -- --id=@small_link create qos type=linux-htb queues=0=@q0,1=@q1,2=@q2 \
        -- --id=@q0 create queue other-config:min-rate=5000000 other-config:max-rate=5000000 \
        -- --id=@q1 create queue other-config:min-rate=5000000 other-config:max-rate=5000000 \
        -- --id=@q2 create queue other-config:min-rate=5000000 other-config:max-rate=5000000 \
        -- set port s1-eth1 qos=@big_link \
        -- set port s1-eth2 qos=@big_link \
        -- set port s2-eth1 qos=@big_link \
        -- set port s2-eth2 qos=@big_link \
        -- --id=@big_link create qos type=linux-htb queues=0=@q3,1=@q4,2=@q5 \
        -- --id=@q3 create queue other-config:min-rate=20000000 other-config:max-rate=20000000 \
        -- --id=@q4 create queue other-config:min-rate=20000000 other-config:max-rate=20000000 \
        -- --id=@q5 create queue other-config:min-rate=20000000 other-config:max-rate=20000000 """)

    # for port in SW_HOST_PORTS.split():  # 配置 HOST_PORT 和上面的 ovsctl 一样策略 (如果用 ALL_PORT 来执行可以不用上面 ovs-vsctl 了,
    #     之前用 ovs-vsctl 是为了保持和ovs的兼容性)
    #     os.popen("tc qdisc add dev %s root handle 1: htb default 1" % port)
    #     TODO 这里host的 burst 值还和 ovs 的不一样, 回头细调
    #     os.popen("tc class add dev %s parent 1: classid 1:fffe htb rate 10000mbit burst 1250b cburst 1250b" % port)
    #     os.popen("tc class add dev %s parent 1:fffe classid 1:1 htb rate 5mbit burst 1563b cburst 1563b" % port)
    #     os.popen("tc class add dev %s parent 1:fffe classid 1:2 htb rate 5mbit burst 1563b" % port)
    #     os.popen("tc class add dev %s parent 1:fffe classid 1:3 htb rate 5mbit burst 1563b" % port)
    #     pass  # 通过 ovs-vsctl 已配置

    # 设置 tc filter:  端口 5001 -> 队列 1:1, 5002 -> 1:2 , 5003 -> 1:3
    LOG.info("在交换机接主机端口上设置 handle 和 filter 端口 5001 -> 队列 1:1, 5002 -> 1:2 , 5003 -> 1:3 \n" \
             "  h1 -> 队列2, icmp -> 队列2... \n")
    for port in SW_HOST_PORTS.split():
        # 放置 class handle
        os.popen("tc qdisc add dev %s parent 1:1 handle 1: pfifo limit %s" % (port, TX_QUEUE_LEN))
        # 队列2 采用RED队列, 支持 早期随机mark为ecn的方式
        os.popen("tc qdisc add dev $NDEV parent 1:2 handle 2: red limit 200000 min 50000 max 150000 avpkt 1000 ecn")
        os.popen("tc qdisc add dev %s parent 1:3 handle 3: pfifo limit %s" % (port, TX_QUEUE_LEN))

        # 放置 class filter
        u32_filter_prefix = "tc filter add dev %s protocol ip parent 1:0 prio 1 u32" % port
        os.popen('%s match ip dport 5001 0xffff flowid 1:1' % u32_filter_prefix)
        os.popen('%s match ip dport 5002 0xffff flowid 1:2' % u32_filter_prefix)
        os.popen('%s match ip dport 5003 0xffff flowid 1:3' % u32_filter_prefix)
        os.popen('%s match ip dport 5003 0xffff flowid 1:3' % u32_filter_prefix)
        os.popen('%s match match ip src 10.0.0.1/32 flowid 1:2' % u32_filter_prefix)  # 把h1所有包 match 到队列2
        os.popen('%s match ip protocol 1 0xff flowid 1:2' % u32_filter_prefix)  # 把icmp所有包 match 到队列2
        print "  设置端口 %s 完成 ..." % port
    print " 检查设置: tc filter show dev $NDEV parent 1:fffe"

    LOG.info("查看 tc qdisc")
    LOG.info("  普通 pfifo_fast 接口 s3-eth1 状态为:  tc qdisc show dev s3-eth1\n")
    LOG.debug("\n".join(os.popen('tc qdisc show dev s3-eth1').readlines()))
    print "  查看 netem 延时链路 s3-eth2 <->s4-eth1 接口状态为:  tc qdisc show dev s3-eth2 / s4-eth1"
    LOG.debug("\n".join(os.popen('tc qdisc show dev s3-eth2').readlines()))
    LOG.debug("\n".join(os.popen('tc qdisc show dev s4-eth1').readlines()))
    print "  查看 htb qdisc 队列接口 s1-eth3, tc qdisc show dev $NDEV (采用的应是 htb, 而不是 pfifo_fast(普通) 或 netem(延时) )"
    LOG.debug("\n".join(os.popen('tc qdisc show dev s1-eth3').readlines()))
    print "  查看 htb class 队列接口 s1-eth3,  tc class show dev $NDEV"
    LOG.debug("\n".join(os.popen('tc class show dev s1-eth3').readlines()))
    print "  查看 htb filter 队列接口 s1-eth3,  tc filter show dev $NDEV parent 1:0"
    LOG.debug("\n".join(os.popen('tc filter show dev s1-eth3 parent 1:0').readlines()))

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

    # check = threading.Timer(5, checkTimer)
    # check.start()

    # killPing = threadTwo(2,5)
    # killPing.start()

    # thread = threadOne(1,7)
    # thread.start()
    # s1 = net.get('s1')
    # s1.sendCmd('ls')
    # s1.sendCmd('watch -n 0.1 tc -s -d class show dev s1-eth3')
    # s1 = net.getNodeByName('s1')
    # s1.sendCmd('ls')
    CLI(net)  # 激活命令行交互
    # cli.do_sh("ls")
    net.stop()


def check_timer():  # no timer in use now

    # result=os.popen('tc -s class ls dev s2-eth2 parent 1:fffe classid 1:3').read()
    # arr=result.split(' ')
    # sendbyte = arr[17]
    # sendpack = arr[19]
    # backlog = arr[33]
    # sendpackint = int(sendpack)
    # backlogint = int(backlog[:-1])
    # print "queue statistics"
    # print 's2-eth2'
    # print(sendbyte)
    # print(sendpack)
    # print(backlogint)
    print "queue statistics"
    global flags1
    global flags2
    global popens
    '''
    result=os.popen('tc -s class ls dev s2-eth1 parent 1:fffe classid 1:3').read()
    arr=result.split(' ')
    sendbyte = arr[17]
    sendpack = arr[19]
    backlog = arr[33]
    sendpackint = int(sendpack)
    backlogint = int(backlog[:-1])
    print 's2-eth1:'+sendbyte+'--'+sendpack+'--'+backlog
    '''

    # Test s2-eth2
    '''
    result=os.popen('tc -s class ls dev s2-eth2 parent 1:fffe classid 1:3').read()
    arr=result.split(' ')
    sendbyte = arr[17]
    sendpack = arr[19]
    backlog = arr[33]
    sendpackint = int(sendpack)
    backlogint = int(backlog[:-1])
    print 's2-eth2:'+sendbyte+'--'+sendpack+'--'+backlog
    '''

    # another method rest api
    command = "curl -s http://192.168.57.2:8080/wm/core/switch/queue/00:00:00:00:00:00:00:02/2/json"
    result = os.popen(command).read()
    parsed_result = json.loads(result)

    left_packets2 = parsed_result['queue_sts_reply'][0]['queue_sts'][2]['leftPackets']
    left_int2 = int(left_packets2)

    print "s2-eth3 queue3 leftpackets:" + left_packets2
    if (left_int2 > 800) and (flags2 is False):
        flags2 = True
        command2 = \
            "curl -s http://192.168.57.2:8080/wm/core/switch/queuerate/00:00:00:00:00:00:00:01/s1-eth3/2/1000000/json"
        os.popen(command2).read()
        # os.popen('tc class change dev s1-eth2 parent 1:fffe classid 1:3 htb rate 1000000bit ceil 1000000bit')
        print "change s1-eth3 to 1M"
    elif (left_int2 < 300) and (flags2 is True):
        flags2 = False
        command2 = \
            "curl -s http://192.168.57.2:8080/wm/core/switch/queuerate/00:00:00:00:00:00:00:01/s1-eth3/2/5000000/json"
        os.popen(command2).read()
        # os.popen('tc class change dev s1-eth2 parent 1:fffe classid 1:3 htb rate 5000000bit ceil 5000000bit')
        print "change s1-eth3 to 5M"

    '''
    result=os.popen('tc -s class ls dev s1-eth1 parent 1:fffe classid 1:3').read()
    arr=result.split(' ')
    sendbyte = arr[17]
    sendpack = arr[19]
    backlog = arr[33]
    sendpackint = int(sendpack)
    backlogint = int(backlog[:-1])
    print 's1-eth1:'+sendbyte+'--'+sendpack+'--'+backlog
    '''
    # Test s1-eth2
    '''
    result=os.popen('tc -s class ls dev s1-eth2 parent 1:fffe classid 1:3').read()
    arr=result.split(' ')
    sendbyte = arr[17]
    sendpack = arr[19]
    backlog = arr[33]
    sendpackint = int(sendpack)
    backlogint = int(backlog[:-1])
    print 's1-eth2:'+sendbyte+'--'+sendpack+'--'+backlog
    if (backlogint > 800) and (flags1 == False):
        flags1 = True
        h1 = net.get('h1')
        h1.popen("tc class change dev h1-eth0 parent 1:fffe classid 1:1 htb rate 1000000bit ceil 1000000bit")
        
        print "change h1 to slow speed"
    elif (backlogint < 30) and (flags1 == True):
        flags1 = False
        h1 = net.get('h1')
        h1.popen("tc class change dev h1-eth0 parent 1:fffe classid 1:1 htb rate 10000kbit ceil 10000kbit")
        print "change h1 to fast speed"
    '''

    # another method rest api
    command = "curl -s http://192.168.57.2:8080/wm/core/switch/queue/00:00:00:00:00:00:00:01/2/json"
    result = os.popen(command).read()
    parsed_result = json.loads(result)

    left_packets2 = parsed_result['queue_sts_reply'][0]['queue_sts'][2]['leftPackets']
    left_int2 = int(left_packets2)

    print "s1-eth3 queue3 leftpackets:" + left_packets2
    if (left_int2 > 800) and (flags1 is False):
        flags1 = True
        h2 = net.get('h2')
        h2.popen("tc class change dev h2-eth0 parent 1:fffe classid 1:1 htb rate 1000000bit ceil 1000000bit")

        print "change h2 to slow speed"
    elif (left_int2 < 30) and (flags1 is True):
        flags1 = False
        h2 = net.get('h2')
        h2.popen("tc class change dev h2-eth0 parent 1:fffe classid 1:1 htb rate 10000kbit ceil 10000kbit")
        print "change h2 to fast speed"

        # test queue 2
    command = "curl -s http://192.168.57.2:8080/wm/core/switch/queue/00:00:00:00:00:00:00:02/1/json"
    result = os.popen(command).read()
    parsed_result = json.loads(result)
    left_packets2 = parsed_result['queue_sts_reply'][0]['queue_sts'][1]['leftPackets']
    print "s2-eth2 queue2 leftpackets:" + left_packets2

    command = "curl -s http://192.168.57.2:8080/wm/core/switch/queue/00:00:00:00:00:00:00:01/1/json"
    result = os.popen(command).read()
    parsed_result = json.loads(result)
    left_packets2 = parsed_result['queue_sts_reply'][0]['queue_sts'][2]['leftPackets']
    print "s1-eth3 queue2 leftpackets:" + left_packets2
    # print '%s:' % h1.name, h1.monitor().strip()

    # if backlogint > 900:
    #  popens[h1].send_signal(SIGINT)
    # for p in popens.values():
    #     p.send_signal( SIGINT )
    # h1.sendCmd('pgrep ping | xargs kill -s 9')
    #  if sendpackint >500:
    #  thread.stop()
    # print h1.cmd('ps aux|grep ping')
    global check
    check = threading.Timer(0.5, check_timer)
    check.start()


class ThreadOne(threading.Thread):
    def __init__(self, num, interval):
        threading.Thread.__init__(self)
        self.thread_num = num
        self.interval = interval
        self.thread_stop = False

    def run(self):
        global popens
        popens = {}
        time.sleep(self.interval)
        print "ping one"
        h1 = net.get('h1')
        h2 = net.get('h2')
        h3 = net.get('h3')
        h4 = net.get('h4')
        # h1.sendCmd('ping -i0.01 10.0.0.2')
        # h1.popen("sudo ovs-vsctl -- set port h1-eth0 qos=@newqos --
        # --id=@newqos create qos type=linux-htb queues=0=@q0,1=@q1,2=@q2 --
        # --id=@q0 create queue other-config:min-rate=20000000 other-config:max-rate=20000000 --
        # --id=@q1 create queue other-config:min-rate=20000000 other-config:max-rate=20000000 --
        # --id=@q2 create queue other-config:min-rate=20000000 other-config:max-rate=20000000")
        # h2.popen("sudo ovs-vsctl -- set port h2-eth0 qos=@newqos --
        # --id=@newqos create qos type=linux-htb queues=0=@q0,1=@q1,2=@q2 --
        # --id=@q0 create queue other-config:min-rate=20000000 other-config:max-rate=20000000 --
        # --id=@q1 create queue other-config:min-rate=20000000 other-config:max-rate=20000000 --
        # --id=@q2 create queue other-config:min-rate=20000000 other-config:max-rate=20000000")

        h1.popen("sudo /sbin/tc qdisc add dev h1-eth0 root handle 1: htb default 1")
        h1.popen("sudo /sbin/tc class add dev h1-eth0 parent 1: classid 1:0xffff htb rate 300000kbit ceil 300000kbit")
        h1.popen("sudo /sbin/tc class add dev h1-eth0 parent 1:0xffff classid 1:1 htb rate 10000kbit ceil 10000kbit ")
        h1.popen("sudo /sbin/tc class add dev h1-eth0 parent 1:0xffff classid 1:2 htb rate 10000kbit ceil 10000kbit ")
        h1.popen("sudo /sbin/tc qdisc add dev h1-eth0 parent 1:1 handle 10: pfifo 1000")
        h1.popen("sudo /sbin/tc qdisc add dev h1-eth0 parent 1:2 handle 20: pfifo 1000")

        h2.popen("sudo /sbin/tc qdisc add dev h2-eth0 root handle 1: htb default 1")
        h2.popen("sudo /sbin/tc class add dev h2-eth0 parent 1: classid 1:0xffff htb rate 300000kbit ceil 300000kbit")
        h2.popen("sudo /sbin/tc class add dev h2-eth0 parent 1:0xffff classid 1:1 htb rate 10000kbit ceil 10000kbit ")
        h2.popen("sudo /sbin/tc class add dev h2-eth0 parent 1:0xffff classid 1:2 htb rate 10000kbit ceil 10000kbit ")
        h2.popen("sudo /sbin/tc qdisc add dev h2-eth0 parent 1:1 handle 10: pfifo 1000")
        h2.popen("sudo /sbin/tc qdisc add dev h2-eth0 parent 1:2 handle 20: pfifo 1000")

        h3.popen("sudo /sbin/tc qdisc add dev h3-eth0 root handle 1: htb default 1")
        h3.popen("sudo /sbin/tc class add dev h3-eth0 parent 1: classid 1:0xffff htb rate 300000kbit ceil 300000kbit")
        h3.popen("sudo /sbin/tc class add dev h3-eth0 parent 1:0xffff classid 1:1 htb rate 20000kbit ceil 20000kbit ")
        h3.popen("sudo /sbin/tc class add dev h3-eth0 parent 1:0xffff classid 1:2 htb rate 20000kbit ceil 20000kbit ")
        h3.popen("sudo /sbin/tc qdisc add dev h3-eth0 parent 1:1 handle 10: pfifo 1000")
        h3.popen("sudo /sbin/tc qdisc add dev h3-eth0 parent 1:2 handle 20: pfifo 1000")

        h4.popen("sudo /sbin/tc qdisc add dev h4-eth0 root handle 1: htb default 1")
        h4.popen("sudo /sbin/tc class add dev h4-eth0 parent 1: classid 1:0xffff htb rate 300000kbit ceil 300000kbit")
        h4.popen("sudo /sbin/tc class add dev h4-eth0 parent 1:0xffff classid 1:1 htb rate 20000kbit ceil 20000kbit ")
        h4.popen("sudo /sbin/tc class add dev h4-eth0 parent 1:0xffff classid 1:2 htb rate 20000kbit ceil 20000kbit ")
        h4.popen("sudo /sbin/tc qdisc add dev h4-eth0 parent 1:1 handle 10: pfifo 1000")
        h4.popen("sudo /sbin/tc qdisc add dev h4-eth0 parent 1:2 handle 20: pfifo 1000")

        # popens[h3] = h3.popen("iperf -s -p 12345 -i 1 -u")
        # popens[h1] = h1.popen("iperf -c %s -p 12345 -i 1 -t 10000 -u -b 6M"% h3.IP())
        # popens[h2] = h2.popen("iperf -c %s -p 12345 -i 1 -t 10000 -u -b 6M"% h3.IP())
        # popens[h1] = h1.popen("iperf -s -p 12345 -i 1 -M")
        # popens[h2] = h2.popen("iperf -c %s -p 12345 -i 1 -t 10000"% h1.IP())

        # popens[h1].wait()
        # popens[h1] = h1.popen('ping -i0.1',h2.IP())
        # h1.sendCmd('ping -i0.01 10.0.0.2 &')
        # pid = int(h1.cmd('ping -i0.01 10.0.0.2'))
        # for p in popens.values():
        #   print p
        # popens[h1] = h1.popen('ping -i0.1',h2.IP())

    def stop(self):
        self.thread_stop = True


class ThreadTwo(threading.Thread):
    def __init__(self, num, interval):
        threading.Thread.__init__(self)
        self.thread_num = num
        self.interval = interval
        self.thread_stop = False

    def run(self):
        time.sleep(self.interval)
        h1 = net.get('h1')
        net.get('h2')
        while 1:
            result = os.popen('tc -s class ls dev s2-eth2 parent 1:fffe classid 1:3').read()
            arr = result.split(' ')
            sendbyte = arr[17]
            sendpack = arr[19]
            # sendpackint = int(sendpack)
            backlog = arr[33]
            backlogint = int(backlog[:-1])
            print "queue statistics"
            print(sendbyte)
            print(sendpack)
            print(backlogint)
            if backlogint > 600:
                popens[h1].send_signal(SIGINT)
            time.sleep(1)

    def stop(self):
        self.thread_stop = True


def ping_timer_two():
    print "ping two"


def ping_timer_three():
    print "ping three"


if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    qbb_test()
    # check = threading.Timer(8, checkTimer)
    # check.start()
    # killPing = threadTwo(2,5)
    # killPing.start()
    # thread = threadOne(1,10)
    # thread.start()
