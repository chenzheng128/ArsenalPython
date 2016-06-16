#!/usr/bin/python
# --*-- coding:utf-8 --*--

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls

from ryu.ofproto import ofproto_v1_3

class L2Switch(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION] #设置版本号1.3, 无此句默认是1.0

    def __init__(self, *args, **kwargs):
        super(L2Switch, self).__init__(*args, **kwargs)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        dp = msg.datapath  #交换机, 包含源地址, 端口等
        ofp = dp.ofproto
        ofp_parser = dp.ofproto_parser

        actions = [ofp_parser.OFPActionOutput(ofp.OFPP_FLOOD)]
        out = ofp_parser.OFPPacketOut(
            #datapath=dp, buffer_id=msg.buffer_id, in_port=msg.in_port,          # OF1.0 msg.in_port
            datapath=dp, buffer_id=msg.buffer_id, in_port=msg.match['in_port'],  # OF1.3 msg.match
            actions=actions)
        dp.send_msg(out)