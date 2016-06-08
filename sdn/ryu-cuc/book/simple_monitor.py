#!/usr/bin/python
# --*-- coding:utf-8 --*--

import json
from operator import attrgetter

from ryu.app import simple_switch_13
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import hub


class SimpleMonitor(simple_switch_13.SimpleSwitch13):

    def __init__(self, *args, **kwargs):
        super(SimpleMonitor, self).__init__(*args, **kwargs)
        self.datapaths = {}
        # 通过hub处理, 定期轮训代码
        # 通过hub.spawn() 建立執行緒。背后使用 evernlet 的 green 執行
        self.monitor_thread = hub.spawn(self._monitor)

    @set_ev_cls(ofp_event.EventOFPStateChange,
                [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        """
         EventOFPStateChange 就可以用來監測交換器的連線中斷。
         這個事件偵測是 Ryu 框架所提供的功能，會被觸發在 Datapath 的狀態改變時
        :param ev:
        :return:
        """
        datapath = ev.datapath
        # 當 Datapath 的狀態變成 MAIN_DISPATCHER 時，代表交換器已經註冊並正處於被監視的狀態。
        if ev.state == MAIN_DISPATCHER:
            if not datapath.id in self.datapaths:
                self.logger.debug('register datapath: %016x', datapath.id)
                self.datapaths[datapath.id] = datapath
        # 而狀態變成 DEAD_DISPATCHER 時代表已經從註冊狀態解除。
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                self.logger.debug('unregister datapath: %016x', datapath.id)
                del self.datapaths[datapath.id]

    def _monitor(self):
        """
        在執行緒中 _monitor() 方法確保了執行緒可以在每 10 秒的間隔中，
        不斷地向註冊的交換器發送要求以取得統計資訊。
        :return:
        """
        while True:
            for dp in self.datapaths.values():
                # 定期(10秒钟)呼叫 _request_stats()
                self._request_stats(dp)
            hub.sleep(10)

    def _request_stats(self, datapath):
        """
        定期呼叫 _request_stats()
         以驅動 OFPFlowStatsRequest 和 OFPPortStatsRequest 對交換器發出訊息
        :param datapath:
        :return:
        """
        self.logger.debug('send stats request: %016x', datapath.id)
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        """
        OFPFlowStatsRequest 主要用來對交換器的 Flow Entry 取得統計的資料。
         對於交換器發出的要求可以使用 table ID、output port、cookie 值和 match 條件來限縮範圍，
         但是這邊的例子是取得所有的 Flow Entry。
        """
        req = parser.OFPFlowStatsRequest(datapath)
        datapath.send_msg(req)

        """
        OFPPortStatsRequest 是用來取得關於交換器的連接埠相關資訊以及統計訊息。
         使用的時候可以指定連接埠號，這邊使用 OFPP_ANY 目的是要取得所有的連接埠統計資料。
        """
        req = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_ANY)
        datapath.send_msg(req)

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def _flow_stats_reply_handler(self, ev):
        body = ev.msg.body

        self.logger.info('datapath         '
                         'in-port  eth-dst           '
                         'out-port packets  bytes')
        self.logger.info('---------------- '
                         '-------- ----------------- '
                         '-------- -------- --------')

        """
        prioirity=0 ? 的 Table-miss Flow 除外的全部 Flow Entry 將會被選擇，
        通過並符合該 Flow Entry 的封包數和位元數統計資料將會被回傳，
        並以 in_ports 接收埠號和 eth_dst 目的 MAC 位址的方式排序。
        """
        for stat in sorted([flow for flow in body if flow.priority == 1],
                           key=lambda flow: (flow.match['in_port'],
                                             flow.match['eth_dst'])):
            self.logger.info('%016x %8x %17s %8x %8d %8d',
                             ev.msg.datapath.id,
                             stat.match['in_port'], stat.match['eth_dst'],
                             stat.instructions[0].actions[0].port,
                             stat.packet_count, stat.byte_count)

            # 增加 json logger 输出
            #self.logger.info('%s', json.dumps(ev.msg.to_jsondict(), ensure_ascii=True,
            #                      indent=3, sort_keys=True))


    @set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
    def _port_stats_reply_handler(self, ev):
        """
        為了接收來自交換器的回應，建立一個 event handler 來接受從交換器發送的 FlowStatsReply 訊息。
        :param ev:
        :return:
        """

        # 屬性 body 是 OFPFlowStats 的列表，當中儲存了每一個 Flow Entry 的統計資訊
        body = ev.msg.body

        """
        OPFPortStatsReply 類別的屬性 body 會列出在 OFPPortStats 中的資料列表。
        OFPPortStats 連接埠號儲存接收端的封包數量、位元數量、丟棄封包數量、錯誤數量、
        frame錯誤數量、overrrun數量、CRC錯誤數量、collection數量等等的統計資訊。
        依據連接埠號的排序列出接收的封包數量、接收位元數量、接收錯誤數量、
        發送封包數量、發送位元數、發送錯誤數量。
        """

        self.logger.info('datapath         port     '
                         'rx-pkts  rx-bytes rx-error '
                         'tx-pkts  tx-bytes tx-error')
        self.logger.info('---------------- -------- '
                         '-------- -------- -------- '
                         '-------- -------- --------')
        for stat in sorted(body, key=attrgetter('port_no')):
            self.logger.info('%016x %8x %8d %8d %8d %8d %8d %8d',
                             ev.msg.datapath.id, stat.port_no,
                             stat.rx_packets, stat.rx_bytes, stat.rx_errors,
                             stat.tx_packets, stat.tx_bytes, stat.tx_errors)