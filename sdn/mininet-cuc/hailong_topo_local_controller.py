# !/usr/bin/python
# --*-- coding:utf-8 --*--


"""
origined from 海龙拓扑测试
revised by zhchen
Usage:
sudo mn -c ; sudo python cuc/hailong_topo.py
"""
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
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


class QbbTopo(Topo):
    """
    Qbb experiment test topology
    @ZHL@CUC@2015.12.26"
    拓扑图: https://www.processon.com/view/link/5752d7f1e4b0695484404d39
    """

    def build(self):
        leftSwitch = self.addSwitch('s1')
        rightSwitch = self.addSwitch('s2')
        middleSwitch1 = self.addSwitch('s3')
        middleSwitch2 = self.addSwitch('s4')

        leftHost = self.addHost('h1', inNamespace=True)
        rightHost = self.addHost('h2', inNamespace=True)
        serverHost1 = self.addHost('h3', inNamespace=True)
        serverHost2 = self.addHost('h4', inNamespace=True)

        self.addLink(leftHost, leftSwitch)
        self.addLink(rightHost, leftSwitch)
        self.addLink(leftSwitch, middleSwitch1)
        """
        # s3 <-> s4 查看 含延时链路状态
        tc qdisc show dev s3-eth2
        tc class show dev s3-eth2
        """
        self.addLink(middleSwitch1, middleSwitch2, delay='10ms', use_htb=True)
        self.addLink(middleSwitch2, rightSwitch)
        self.addLink(serverHost1, rightSwitch)
        self.addLink(serverHost2, rightSwitch)


def qbbTest():
    "Create and test our QBB network standard"
    qbbTopo = QbbTopo()
    global net
    #MMininet 类 API 参考: http://mininet.org/api/classmininet_1_1net_1_1Mininet.html#a1ed0f0c8ba06a398e02f3952cc4c8393
    #命令行参数对应 --mac => autoSetMacs
    net = Mininet(topo=qbbTopo, controller=None, link=TCLink, autoSetMacs=True, xterms=True)

    c0 = Controller( 'c0', port=6633 )
    #net.addController('c0', controller=RemoteController, ip='192.168.57.2', port=6653)
    net.addController(c0)
    net.start()


    print "调整 s1-eth1 qlen: sudo ip link set txqueuelen 500 dev s1-eth1"
    os.popen("sudo ip link set txqueuelen 500 dev s1-eth1")

    print "创建 s2 s3 4m 5m QoS 队列"

    # os.popen("""sudo ovs-vsctl \
    #     -- set port s2-eth1 qos=@4mqos \
    #     -- set port s2-eth2 qos=@4mqos \
    #     -- set port s2-eth3 qos=@4mqos \
    #     -- --id=@4mqos create qos type=linux-htb queues=0=@q0,1=@q1,2=@q2 \
    #     -- --id=@q0 create queue other-config:min-rate=4000000 other-config:max-rate=4000000 \
    #     -- --id=@q1 create queue other-config:min-rate=4000000 other-config:max-rate=4000000 \
    #     -- --id=@q2 create queue other-config:min-rate=4000000 other-config:max-rate=4000000 \
    #     -- set port s1-eth1 qos=@5mqos2 \
    #     -- set port s1-eth2 qos=@5mqos2 \
    #     -- set port s1-eth3 qos=@5mqos2 \
    #     -- --id=@5mqos2 create qos type=linux-htb queues=0=@q3,1=@q4,2=@q5 \
    #     -- --id=@q3 create queue other-config:min-rate=5000000 other-config:max-rate=5000000 \
    #     -- --id=@q4 create queue other-config:min-rate=5000000 other-config:max-rate=5000000 \
    #     -- --id=@q5 create queue other-config:min-rate=5000000 other-config:max-rate=5000000 """)

    print "普通接口 s3-eth1 状态为:  tc qdisc show dev s3-eth1"
    print os.popen('tc qdisc show dev s3-eth1').readlines()
    print "延时链路 s3-eth2 <->s4-eth1 接口状态为:  tc qdisc show dev s3-eth2 / s4-eth1"
    print os.popen('tc qdisc show dev s3-eth2').readlines()
    print os.popen('tc qdisc show dev s4-eth1').readlines()
    print "队列接口 s2-eth1, tc qdisc show 采用的应是 htb, 而不是 pfifo_fast(普通) 或 netem(延时) "
    print os.popen('tc qdisc show dev s2-eth1').readlines()
    print "队列接口 s2-eth1,  tc class show "
    print os.popen('tc class show dev s2-eth1').readlines()


    # check = threading.Timer(5, checkTimer)
    # check.start()

    # killPing = threadTwo(2,5)
    # killPing.start()

    # thread = threadOne(1,7)
    # thread.start()

    CLI(net) #激活命令行交互
    net.stop()


def checkTimer():  # no timer in use now
    '''result=os.popen('tc -s class ls dev s2-eth2 parent 1:fffe classid 1:3').read()
    arr=result.split(' ')
    sendbyte = arr[17]
    sendpack = arr[19]
    backlog = arr[33]
    sendpackint = int(sendpack)
    backlogint = int(backlog[:-1])
    print "queue statistics"
    print 's2-eth2'
    print(sendbyte)
    print(sendpack)
    print(backlogint)'''
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
    parsedResult = json.loads(result)

    leftPackets2 = parsedResult['queue_sts_reply'][0]['queue_sts'][2]['leftPackets']
    leftInt2 = int(leftPackets2)

    print "s2-eth3 queue3 leftpackets:" + leftPackets2
    if (leftInt2 > 800) and (flags2 == False):
        flags2 = True
        command2 = "curl -s http://192.168.57.2:8080/wm/core/switch/queuerate/00:00:00:00:00:00:00:01/s1-eth3/2/1000000/json"
        result2 = os.popen(command2).read()
        # os.popen('tc class change dev s1-eth2 parent 1:fffe classid 1:3 htb rate 1000000bit ceil 1000000bit')
        print "change s1-eth3 to 1M"
    elif (leftInt2 < 300) and (flags2 == True):
        flags2 = False
        command2 = "curl -s http://192.168.57.2:8080/wm/core/switch/queuerate/00:00:00:00:00:00:00:01/s1-eth3/2/5000000/json"
        result2 = os.popen(command2).read()
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
    parsedResult = json.loads(result)

    leftPackets2 = parsedResult['queue_sts_reply'][0]['queue_sts'][2]['leftPackets']
    leftInt2 = int(leftPackets2)

    print "s1-eth3 queue3 leftpackets:" + leftPackets2
    if (leftInt2 > 800) and (flags1 == False):
        flags1 = True
        h2 = net.get('h2')
        h2.popen("tc class change dev h2-eth0 parent 1:fffe classid 1:1 htb rate 1000000bit ceil 1000000bit")

        print "change h2 to slow speed"
    elif (leftInt2 < 30) and (flags1 == True):
        flags1 = False
        h2 = net.get('h2')
        h2.popen("tc class change dev h2-eth0 parent 1:fffe classid 1:1 htb rate 10000kbit ceil 10000kbit")
        print "change h2 to fast speed"

        # test queue 2
    command = "curl -s http://192.168.57.2:8080/wm/core/switch/queue/00:00:00:00:00:00:00:02/1/json"
    result = os.popen(command).read()
    parsedResult = json.loads(result)
    leftPackets2 = parsedResult['queue_sts_reply'][0]['queue_sts'][1]['leftPackets']
    print "s2-eth2 queue2 leftpackets:" + leftPackets2

    command = "curl -s http://192.168.57.2:8080/wm/core/switch/queue/00:00:00:00:00:00:00:01/1/json"
    result = os.popen(command).read()
    parsedResult = json.loads(result)
    leftPackets2 = parsedResult['queue_sts_reply'][0]['queue_sts'][2]['leftPackets']
    print "s1-eth3 queue2 leftpackets:" + leftPackets2
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
    check = threading.Timer(0.5, checkTimer)
    check.start()


class threadOne(threading.Thread):
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
        # h1.popen("sudo ovs-vsctl -- set port h1-eth0 qos=@newqos -- --id=@newqos create qos type=linux-htb queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create queue other-config:min-rate=20000000 other-config:max-rate=20000000 -- --id=@q1 create queue other-config:min-rate=20000000 other-config:max-rate=20000000 -- --id=@q2 create queue other-config:min-rate=20000000 other-config:max-rate=20000000")
        # h2.popen("sudo ovs-vsctl -- set port h2-eth0 qos=@newqos -- --id=@newqos create qos type=linux-htb queues=0=@q0,1=@q1,2=@q2 -- --id=@q0 create queue other-config:min-rate=20000000 other-config:max-rate=20000000 -- --id=@q1 create queue other-config:min-rate=20000000 other-config:max-rate=20000000 -- --id=@q2 create queue other-config:min-rate=20000000 other-config:max-rate=20000000")

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


class threadTwo(threading.Thread):
    def __init__(self, num, interval):
        threading.Thread.__init__(self)
        self.thread_num = num
        self.interval = interval
        self.thread_stop = False

    def run(self):
        time.sleep(self.interval)
        h1 = net.get('h1')
        h2 = net.get('h2')
        while 1:
            result = os.popen('tc -s class ls dev s2-eth2 parent 1:fffe classid 1:3').read()
            arr = result.split(' ')
            sendbyte = arr[17]
            sendpack = arr[19]
            sendpackint = int(sendpack)
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


def pingTimerTwo():
    print "ping two"


def pingTimerThree():
    print "ping three"


if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    qbbTest()
    # check = threading.Timer(8, checkTimer)
    # check.start()
    # killPing = threadTwo(2,5)
    # killPing.start()
    # thread = threadOne(1,10)
    # thread.start()
