# !/usr/bin/python
# --*-- coding:utf-8 --*--


"""
origined from 海龙拓扑测试
revised by zhchen

Usage:
sudo mn -c ; sudo python cuc/hailong_local_qos.py



"""
import os
from time import sleep
import qdisc_helper
import sshd
from mininet.link import TCLink, TCIntf, Link
from mininet.log import setLogLevel, MininetLogger, error, info, debug, warn
from mininet.net import Mininet, CLI
from mininet.node import Controller
from mininet.node import OVSSwitch
from mininet.topo import Topo
from mininet.util import pmonitor
from qdisc_helper import os_popen

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


class ECNLink(TCLink):
    def __init__(self, node1, node2, port1=None, port2=None,
                 intf_name1=None, intf_name2=None,
                 addr1=None, addr2=None, **params):
        Link.__init__(self, node1, node2, port1=port1, port2=port2,
                      intfName1=intf_name1, intfName2=intf_name2,
                      cls1=ECNIntf,
                      cls2=ECNIntf,
                      addr1=addr1, addr2=addr2,
                      params1=params,
                      params2=params)


class ECNIntf(TCIntf):
    def change_queue_len(self, tx_queue_len=TX_QUEUE_LEN):
        # LOG.debug("  调整 %s 网络 队列长度 txqueuelen " )
        os_popen("sudo ip link set txqueuelen %s dev %s" % (tx_queue_len, self.name))
        # print " 检查设置: ifconfig | grep txqueuelen"

    def default_config(self, bw=50, queue_len=100):
        self.change_queue_len()  # 设置默认队列大小
        qdisc_helper.port_default_config(self.name, bw=bw, tx_queue_len=queue_len)

    def change_latency(self, delay):
        qdisc_helper.handle_change_netem(self.name, delay=delay)
        pass

        # pass
        # def config(self, **params):
        #    pass
        # super(TCIntf, self).config(params)


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

        # 如果不在这里指定延时链路, 而通过 qdisc_helper.py 进行延时链路维护
        # ./qdisc_helper.py netem 100 10ms ["s1-eth3 s2-eth3"]
        # ./qdisc_helper.py netem 100 10ms "s3-eth2 s4-eth2"
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


def ecn_qos_init():
    """
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
    net = Mininet(topo=topo, controller=None, link=ECNLink, autoSetMacs=True, xterms=False,
                  autoStaticArp=True)

    c0 = Controller('c0', port=6633)
    # net.addController('c0', controller=RemoteController, ip='192.168.57.2', port=6653)
    net.addController(c0)

    enable_ssh = False  # 如果系统
    if enable_ssh:
        setup_ssh()
    else:
        net.start()

    setup_server(net)

    print_mininet_objs(net)  # 打印 mininet 拓扑对象
    test_diff_bw(net)        # 设置不同带宽条件qos, 并使用 iperf测试
    test_diff_latency(net)   # 设置不同延时条件qos, 并使用 ping 测试

    # CLI(net)  # 激活命令行交互

    net.stop()

def test_diff_latency(network):
    """
    # 设置不同延时条件qos, 并使用 ping 测试
    :param network:
    :return:
    """
    # print_mininet_objs(net)
    result = {}
    for latency in ["10ms", "50ms", "100ms"]:
        setup_queue_and_filter(net, latency=latency, queue_len=200)
        # run_multi_bench()
        # result[latency] = network.ping([net.get("h1"), net.get("h3")] )
        result[latency] = run_bench(net, background=False)
    print result

def test_diff_bw(network):
    """
    # 设置不同带宽条件qos, 并使用 iperf测试
    :param network:
    :return:
    """
    # print_mininet_objs(net)
    result = {}
    for bw in [10, 50, 100]:
        setup_queue_and_filter(net, bw=bw, queue_len=200)
        # run_multi_bench()
        result[bw] = network.iperf(hosts=[network.get("h1"), net.get("h2")])
    print result


def setup_queue_and_filter(network, bw=50, queue_len=TX_QUEUE_LEN, latency="50ms"):
    LOG.info("* setup_queue_and_filter() ... \n")
    for sw in network.switches:
        assert isinstance(sw, OVSSwitch)
        for p in sw.ports: # 修改所有的 ECNIntf
            if isinstance(p, ECNIntf):
                LOG.debug(type(p), p.name, p.bwParamMax, p.params, "\n")
                # p.change_delay()
                p.default_config(bw=bw, queue_len=queue_len)

                # p.delayCmds()
                # print queue_len

                # break

                # p.tc("%s class add dev %s parent 1: classid 1:fffe htb rate 10000mbit burst 1250b cburst 1250b")
                # qdisc_helper.handle_change_netem()
        for intf1, intf2 in network.topo.get_link_intfs(network, "s3", "s4"):
            debug("change latency %s %s to %s" % (intf1, intf2, latency))
            intf1.change_latency(latency);
            intf2.change_latency(latency);


def print_mininet_objs(network):
    print "* mininet hosts"
    for host in network.hosts:
        print type(host)
    # for host in net.intf: print type(host)
    print "* mininet switchs"
    for sw in network.switches:
        assert isinstance(sw, OVSSwitch)
        for p in sw.ports:
            if isinstance(p, TCIntf):
                print type(p), p.name, p.bwParamMax, p.params
            else:
                print type(p), p.name
    print "* mininet links"
    for li in network.links:
        assert isinstance(li, TCLink)
        # for p in [li.intf1 , li.intf2]:
        print type(li.intf1), li.intf1.name, "<->", li.intf2.name

    print "* gethostbyname"
    print network.getNodeByName("h1").name

    print "* config and get link status"
    for srcIntf, dstIntf in network.topo.get_link_intfs(network, "s3", "s4"):
        print srcIntf.name, "<->", dstIntf.name


def run_multi_bench():
    for var in [100, 200, 500]:
        print ("* VAR %s" % var)

        # 带流量测试
        # run_bench(net, round_count=3, round_duration=20, ping_interval=0.2)
        # 不带流量测试
        run_bench(net, background=False)


def run_bench(network, round_count=1, round_duration=5, ping_interval=1.0, background=True):
    """

    :param background:
    :param network: mininet class
    :param round_count:    循环次数
    :param round_duration: 循环时间每轮
    :param ping_interval:  ping包采样间隔
    :return:
    """
    result = ""
    h1 = network.getNodeByName("h1")
    popens = {}
    if background:  # backgroud traffice, 每轮增加10秒时延
        h1.cmd("netperf -H h3 -l %s &" % (round_count * (round_duration + 10)))
    sleep(3)  # wait 2 second to reach tcp max output
    for r in range(round_count):
        print ("*** ROUND %s" % r)
        for h in [h1]:
            ping_cmd = "ping -c%s -i%s h3 " % (int(round_duration / ping_interval), ping_interval)
            LOG.info("<%s>: popen cmd: %s \n" % (h.name, ping_cmd))
            popens[h] = h.popen(ping_cmd)

        # Monitor them and print output
        for host, line in pmonitor(popens):
            if host:
                if line.find("icmp_seq") != -1:
                    LOG.debug("<%s>: %s\n" % (host.name, line.strip()))  # suppressed ping output to debug level
                else:
                    LOG.info("<%s>: %s\n" % (host.name, line.strip()))
                    result += "<%s>: %s\n" % (host.name, line.strip())

    print("".join(os.popen('tc -s -d qdisc show dev s1-eth3').readlines()))
    return result


def setup_server(network):
    """
    :param network: mininet network
    :return:
    设置 host 上的测速 iperf/netperf 服务
    """
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
    setLogLevel('info')
    setLogLevel("debug")  # 打开 debug 日志
    ecn_qos_init()
