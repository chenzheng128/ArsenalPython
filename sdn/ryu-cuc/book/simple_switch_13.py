#!/usr/bin/python
# --*-- coding:utf-8 --*--

"""
参考文档: Ryu Book(中文版): https://osrg.github.io/ryu-book/zh_tw/html/switching_hub.html
"""

# Copyright (C) 2011 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types


class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}

    """
    @ set_ev_cls 用于事件处理
    類別名稱的規則為 ryu.controller.ofp_event.EventOFP + <OpenFlow訊息名稱>
    这里 EventOFP+SwitchFeatures 代表 接受了一个SwitchFeatures消息进行处理

    常见的几个 dispacher 如下 名稱	說明
    ryu.controller.handler.HANDSHAKE_DISPATCHER	交換 HELLO 訊息
    ryu.controller.handler.CONFIG_DISPATCHER	接收 SwitchFeatures訊息
    ryu.controller.handler.MAIN_DISPATCHER	一般狀態
    ryu.controller.handler.DEAD_DISPATCHER	連線中斷
    dispacher的作用是?

    """

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        """
        :param ev: ev.msg 是用來儲存對應事件的 OpenFlow 訊息類別實體
          這個例子中則是 ryu.ofproto.ofproto_v1_3_parser.OFPSwitchFeatures
        :return:
        """

        """
        # msg.datapath 這個訊息是用來儲存 OpenFlow 交換器的 ryu.controller.controller.Datapath 類別所對應的實體。
        # Datapath 類別是用來處理 OpenFlow 交換器重要的訊息，例如執行與交換器的通訊和觸發接收訊息相關的事件。

        """
        datapath = ev.msg.datapath
        # 表示使用的 OpenFlow 版本所對應的 ofproto module。 目前的狀況會是下述的其中之一。ryu.ofproto.ofproto_v1_3
        ofproto = datapath.ofproto
        # 和 ofproto 一樣，表示 ofproto_parser module。 目前的狀況會是下述的其中之一 ryu.ofproto.ofproto_v1_3_parser
        parser = datapath.ofproto_parser

        # install table-miss flow entry
        #
        # We specify NO BUFFER to max_len of the output action due to
        # OVS bug. At this moment, if we specify a lesser number, e.g.,
        # 128, OVS will send Packet-In with invalid buffer_id and
        # truncated packet data. In that case, we cannot output packets
        # correctly.  The bug has been fixed in OVS v2.1.0.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        """

        :param ev:
        :return:
        """
        # If you hit this you might want to increase
        # the "miss_send_length" of your switch
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)
        # type ryu.ofproto.ofproto_v1_3_parser.OFPPacketIn
        msg = ev.msg
        # type ryu.controller.controller.Datapath  # print type(msg)
        datapath = msg.datapath

        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return
        dst = eth.dst
        src = eth.src

        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        # 输出如下日志信息 packet in 1 00:00:00:00:00:02 00:00:00:00:00:01 2
        self.logger.info("packet in dpid=%s %s %s in_port=%s", dpid, src, dst, in_port)

        # learn a mac address to avoid FLOOD next time.
        """
        # mac地址表的维护与更新
        # 為了可以對應連接到多個 OpenFlow 交換器，MAC 位址表和每一個交換器之間的識別，
        就使用 datapath.id 來進行確認
        # dp=1 交换机1 dp=2 交换机2
        # 测试命令
        sudo mn --topo=linear --mac --controller=remote,ip=192.168.57.2 --test_mylib pingal
        """
        self.mac_to_port[dpid][src] = in_port

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            #找不到对于端口时就flood
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst)
            # verify if we have a valid buffer_id, if yes avoid to send both
            # flow_mod & packet_out
            if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                self.add_flow(datapath, 1, match, actions, msg.buffer_id)
                return
            else:
                self.add_flow(datapath, 1, match, actions)
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)
