#!/usr/bin/python
# --*-- coding:utf-8 --*--

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls

from ryu.ofproto import ofproto_v1_3

from ryu.lib.packet import packet
import array

from ryu.ofproto import ether
from ryu.lib.packet import ethernet, arp, packet, tcp

class L2LibPacketSwitch(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION] #设置版本号1.3, 无此句默认是1.0

    def __init__(self, *args, **kwargs):
        super(L2LibPacketSwitch, self).__init__(*args, **kwargs)


    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):


        # print recv packect
        print "## RECV PACKET"
        pkts = packet.Packet(array.array('B', ev.msg.data))
        for p in pkts.protocols:
            print p

        # print build packet
        self.build_packet()

        # extract msg and flooding
        msg = ev.msg
        dp = msg.datapath  #dp交换机, 包含源地址, 端口等
        ofp = dp.ofproto   #dp交换机对应的 OF 协议 CONSTANTS 常量
        ofp_parser = dp.ofproto_parser  #dp交换机对应的 OF 协议 parsing 处理

        actions = [ofp_parser.OFPActionOutput(ofp.OFPP_FLOOD)] # 构建 FLOOD Action
        out = ofp_parser.OFPPacketOut(
            #datapath=dp, buffer_id=msg.buffer_id, in_port=msg.in_port,          # OF1.0 msg.in_port
            datapath=dp, buffer_id=msg.buffer_id, in_port=msg.match['in_port'],  # OF1.3 msg.match
            actions=actions)
        #print "(handle by l2.py) EventOFPPacketIn:", ev
        dp.send_msg(out)  #将 out 消息发送到 dp 上

    def build_packet(self):
        print "## BUILD PACKET"
        e = ethernet.ethernet(dst='ff:ff:ff:ff:ff:ff',
                      src='08:60:6e:7f:74:e7',
                      ethertype=ether.ETH_TYPE_ARP)
        a = arp.arp(hwtype=1, proto=0x0800, hlen=6, plen=4, opcode=2,
                    src_mac='08:60:6e:7f:74:e7', src_ip='192.0.2.1',
                    dst_mac='00:00:00:00:00:00', dst_ip='192.0.2.2')
        p = packet.Packet()
        p.add_protocol(e)
        p.add_protocol(a)
        p.serialize()
        print repr(p.data)  # the on-wire packet

                    #pkt = tcp.tcp(bits=(tcp.TCP_SYN | tcp.TCP_ACK))
        pkt = tcp.tcp(bits=(tcp.TCP_SYN | tcp.TCP_ACK))
        if pkt.has_flags(tcp.TCP_SYN, tcp.TCP_ACK):
            print "BUILD pkt has tcp SYN/ACK flags" #repr(pkt.)
