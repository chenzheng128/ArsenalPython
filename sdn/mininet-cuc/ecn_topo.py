# !/usr/bin/python
# --*-- coding:utf-8 --*--


"""
ecn 实验拓扑类
Origined from: 海龙拓扑测试
Revised by:  zhchen@cuc.edu.cn

Usage:
cd $MININET_HOME/cuc
sudo mn -c ; sudo python ecn_topo.py


"""
import os
from time import sleep
import sshd
import ecn_test_case
import ecn_util
import ecn_qdisc_helper
from mininet.cli import CLI
from mininet.log import setLogLevel, MininetLogger
from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.topo import Topo

TX_QUEUE_LEN = 100  # 网卡队列长度设置

# 实验拓扑的相关网卡 s1/s2 host-switch, s3/s4 middle-switch

# 主机端口
HOST_PORT = " h1-eth0 h2-eth0 h3-eth0 h4-eth0"
# 交换机连主机端口
SW_HOST_PORTS = "s1-eth1 s1-eth2 s1-eth3 s2-eth1 s2-eth2 s2-eth3 s3-eth2 s4-eth2"

# 所有主机端口 = 交换机连主机端口 + 主机端口
# ALL_HOST_PORTS = SW_HOST_PORTS + HOST_PORT
# 所有端口 = 交换机连主机端口 + 交换机级联端口
ALL_PORTS = SW_HOST_PORTS + " s3-eth1 s3-eth2 s4-eth1 s4-eth2"

LOG = MininetLogger()


class ECNTopo(Topo, object):
    """
    Qbb experiment test topology
    @ZHL@CUC@2015.12.26"
    拓扑图: https://www.processon.com/view/link/5752d7f1e4b0695484404d39

    拓扑初始化类

    """

    def __init__(self):
        self.slow_link = None
        self.s1 = None
        self.s2 = None
        self.s3 = None
        self.s4 = None
        self.h1 = None
        self.h2 = None
        self.h3 = None
        self.h4 = None

        super(ECNTopo, self).__init__()

    def build(self):
        """
        建立哑铃拓扑, 网卡顺序为对称
        """

        self.s1 = self.addSwitch('s1')
        self.s2 = self.addSwitch('s2')
        self.s3 = self.addSwitch('s3')
        self.s4 = self.addSwitch('s4')

        self.h1 = self.addHost('h1', inNamespace=True)
        self.h2 = self.addHost('h2', inNamespace=True)
        self.h3 = self.addHost('h3', inNamespace=True)
        self.h4 = self.addHost('h4', inNamespace=True)

        # mininet> link # 查看网卡连接

        self.addLink(self.h1, self.s1)
        self.addLink(self.h2, self.s1)
        self.addLink(self.s1, self.s3)

        self.addLink(self.h3, self.s2)  # 优化网卡顺序, 与s1 主机接口对应
        self.addLink(self.h4, self.s2)
        self.addLink(self.s2, self.s4)

        # """
        # # s3 <-> s4 查看 含延时链路状态 )
        # tc qdisc show dev s3-eth2
        # tc class show dev s4-eth2
        # # 将延时设置为 0ms, netem延时链路调整到 s1-eth3 s2-eth3 上
        # """
        self.addLink(self.s3, self.s4, delay='0ms', use_htb=True)  # 最后连接 s3 s4 优化网卡顺序

        # 如果不在这里指定延时链路, 而通过 ecn_qdisc_helper.py 进行延时链路维护
        # ./ecn_qdisc_helper.py netem 100 10ms ["s1-eth3 s2-eth3"]
        # ./ecn_qdisc_helper.py netem 100 10ms "s3-eth2 s4-eth2"
        # self.addLink(s3, s4)

    @staticmethod
    def get_link_intfs(network, dst, src):  # copy from mininet.configLinkStatus
        """
        获取两个节点之间的链接, 并进行设置
        :param network:
        :param dst:
        :param src:
        :return:
        """
        src = network.nameToNode[src]
        dst = network.nameToNode[dst]
        connections = src.connectionsTo(dst)
        if len(connections) == 0:
            LOG.error('src and dst not connected: %s %s\n' % (src, dst))
        else:
            return connections

            # for srcIntf, dstIntf in connections:
            #    func(srcIntf.name), "<->", dstIntf.name


def ecn_qos_init(remote_controller=False):
    """
    :param remote_controller 是否使用外部控制器
    :return:
    Create and test our QBB network standard"
    初始化拓扑qos; 包括
      四个存在带宽差异(big_link small_link)导致拥堵点的链路 qos 带宽 s1-eth3 s2-eth3 s3-eth3 s4-eth1
      将 5002, h1, icmp 所有流量转移到队列2中, 便于测试

    """

    topo = ECNTopo()  #
    global net
    # MMininet 类 API 参考: http://mininet.org/api/classmininet_1_1net_1_1Mininet.html#a1ed0f0c8ba06a398e02f3952cc4c8393
    # 命令行参数对应 --mac => autoSetMacs
    # 命令行参数对应 --arp => autoStaticArp
    # 命令行参数对应 -x => xterms
    net = Mininet(topo=topo, controller=None, link=ecn_util.ECNLink, autoSetMacs=True, xterms=False,
                  autoStaticArp=True)

    if remote_controller:
        # ecn_qdisc_helper.os_popen("PYTHONPATH=/opt/ryu/ /opt/ryu/bin/ryu-manager
        # ryu.app.rest_qos cuc.book.qos_simple_switch_13 ryu.app.rest_conf_switch & ")
        net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6653)
    else:
        c0 = Controller('c0', port=6633)  # buildin-controller
        net.addController(c0)

    enable_ssh = False  # 激活ssh如果系统 - 暂时不用
    if enable_ssh:
        setup_ssh()
    else:
        net.start()

    if remote_controller:
        print "*** run this command for remote ryu controller"
        print "cd /opt/ryu; PYTHONPATH=/opt/ryu/ /opt/ryu/bin/ryu-manager " \
              "ryu.app.rest_qos cuc.book.qos_simple_switch_13 ryu.app.rest_conf_switch "

    setup_server(net)
    background = False  # 激活后台流量 - 暂时不用
    if background:  # backgroud traffice,
        net.get("h1").cmd("netperf -H h3 -l %s &" % 3600)

    # ecn_util.print_mininet_objs(net)  # 打印 mininet 拓扑对象
    # ecn_test_case.test_diff_bw(net)        # 设置不同带宽条件qos, 并使用 iperf测试
    # ecn_test_case.test_diff_latency(net)   # 设置不同延时条件qos, 并使用 ping 测试

    # ecn_test_case.test01_06_setup_queue_and_latency(net) # 初始化 TEST01_06 拓扑 qos

    # ecn_test_case.test01_04_ecn_red_duration(net, duration=(1, 180))  # 设置不同时长, 进行TEST01-04测试
    # ecn_test_case.test01_04_ecn_red(net, duration=180)  # 进行TEST01-04测试
    # ecn_test_case.test01_base(net, "TEST01", duration=18000)  # 独立测试TEST 01
    ecn_test_case.test11_base(net, "TEST11-py-", duration=120)  # 独立测试TEST 11

    # ecn_test_case.TEST05_openflow_ecn(net, duration=1800) # 进行  TEST05 测试

    CLI(net)  # 激活命令行交互

    net.stop()


def test_diff_latency(network):
    """
    # 设置不同延时条件qos, 并使用 ping 测试
    :param network:
    :return:
    """
    # print_mininet_objs(net)
    result = {}
    for latency in [10, 50, 100]:
        ecn_util.base_setup_queue_and_latency(net, latency=latency, queue_len=200)
        # run_multi_bench()
        # result[latency] = network.ping([net.get("h1"), net.get("h3")] )
        result[latency] = ecn_test_case.test_ping_with_background_traffice(network, background=False)  # 禁止背后流量, 以查看准确延时
    ecn_util.dump_result(result)


def test_diff_bw(network):
    """
    # 设置不同带宽条件qos, 并使用 iperf测试
    :param network:
    :return:
    """
    # print_mininet_objs(net)
    result = {}
    for bw in [10, 50, 100]:
        ecn_util.base_setup_queue_and_latency(net, bw=bw, queue_len=200)
        # run_multi_bench()
        result[bw] = network.iperf(hosts=[network.get("h1"), net.get("h3")])
    ecn_util.ump_result(result)


def setup_server(network):
    """
    :param network: mininet network
    :return:
    设置 host 上的测速 iperf/netperf 服务
    """
    for h in network.hosts:
        h.cmd("echo 1 > /proc/sys/net/ipv4/tcp_ecn #设置为 ecn 主动发起")
    h3 = network.getNodeByName('h3')
    h3.cmd("iperf -s -p 5002 &")
    for host in net.hosts:
        host.cmd("/usr/bin/netserver")  # 启动 netperf daemon


def setup_ssh():
    # net.start()

    # 支持host ssh访问 # route add -net 10.0.0.0/16 root-eth0 出现路由丢失的情况则需要重新添加
    argvopts = '-D -o UseDNS=no -u0'
    sshd.sshd(net, opts=argvopts, ip="10.0.0.254", routes=["10.0.0.0/24"])
    sleep(3)
    os.popen('ifconfig root-eth0 10.0.0.254 netmask 255.255.255.0')  # 上面的设置路由接口会丢失, 改为ip设置
    os.popen('route add -net 10.0.0.0/24 gw 10.0.0.254')


if __name__ == '__main__':
    # Tell mininet to print useful information
    # setLogLevel('info')
    setLogLevel("debug")  # 打开 debug 日志
    ecn_qos_init(remote_controller=True)  # 使用外部 ryu 控制器, 支持openflow13,  qos_ecn_table=0, fw_table=1
