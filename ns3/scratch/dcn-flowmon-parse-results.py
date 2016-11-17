#!/usr/bin/env python
#coding: utf-8
from __future__ import division
import sys
import os

try:
    from xml.etree import cElementTree as ElementTree
except ImportError:
    from xml.etree import ElementTree

def parse_time_ns(tm):
    if tm.endswith('ns'):
        return long(tm[:-4])
    raise ValueError(tm)



class FiveTuple(object):
    __slots__ = ['sourceAddress', 'destinationAddress', 'protocol', 'sourcePort', 'destinationPort']
    def __init__(self, el):
        self.sourceAddress = el.get('sourceAddress')
        self.destinationAddress = el.get('destinationAddress')
        self.sourcePort = int(el.get('sourcePort'))
        self.destinationPort = int(el.get('destinationPort'))
        self.protocol = int(el.get('protocol'))

class Histogram(object):
    __slots__ = 'bins', 'nbins', 'number_of_flows'
    def __init__(self, el=None):
        self.bins = []
        if el is not None:
            #self.nbins = int(el.get('nBins'))
            for bin in el.findall('bin'):
                self.bins.append( (float(bin.get("start")), float(bin.get("width")), int(bin.get("count"))) )

class Flow(object):
    __slots__ = ['flowId', 'delayMean', 'packetLossRatio', 'rxBitrate', 'txBitrate',
                 'fiveTuple', 'packetSizeMean', 'probe_stats_unsorted',
                 'hopCount', 'flowInterruptionsHistogram', 'rx_duration',
                 'rxPackets', 'txPackets', # add rx/tx Packets
                 'rxBits', 'txBits', 'lostPackets' # add rx/tx Bytes
                 ]
    def __init__(self, flow_el):
        self.flowId = int(flow_el.get('flowId'))
        self.rxPackets = long(flow_el.get('rxPackets'))
        self.txPackets = long(flow_el.get('txPackets'))

        self.rxBits = long(flow_el.get('rxBytes')) * 8
        self.txBits = long(flow_el.get('txBytes')) * 8
        tx_duration = float(long(flow_el.get('timeLastTxPacket')[:-4]) - long(flow_el.get('timeFirstTxPacket')[:-4]))*1e-9
        rx_duration = float(long(flow_el.get('timeLastRxPacket')[:-4]) - long(flow_el.get('timeFirstRxPacket')[:-4]))*1e-9
        self.rx_duration = rx_duration
        self.probe_stats_unsorted = []
        if self.rxPackets:
            self.hopCount = float(flow_el.get('timesForwarded')) / self.rxPackets + 1
        else:
            self.hopCount = -1000
        if self.rxPackets:
            self.delayMean = float(flow_el.get('delaySum')[:-4]) / self.rxPackets * 1e-9
            self.packetSizeMean = float(flow_el.get('rxBytes')) / self.rxPackets
        else:
            self.delayMean = None
            self.packetSizeMean = None
        if rx_duration > 0:
            self.rxBitrate = long(flow_el.get('rxBytes'))*8 / rx_duration
        else:
            self.rxBitrate = None
        if tx_duration > 0:
            self.txBitrate = long(flow_el.get('txBytes'))*8 / tx_duration
        else:
            self.txBitrate = None
        self.lostPackets = float(flow_el.get('lostPackets'))
        #print "rxBytes: %s; self.txPackets: %s; self.rxPackets: %s; lostPackets: %s" % (flow_el.get('rxBytes'), self.txPackets, self.rxPackets, lost)
        if self.rxPackets == 0:
            self.packetLossRatio = None
        else:
            self.packetLossRatio = (self.lostPackets / (self.rxPackets + self.lostPackets))

        interrupt_hist_elem = flow_el.find("flowInterruptionsHistogram")
        if interrupt_hist_elem is None:
            self.flowInterruptionsHistogram = None
        else:
            self.flowInterruptionsHistogram = Histogram(interrupt_hist_elem)


class ProbeFlowStats(object):
    __slots__ = ['probeId', 'packets', 'bytes', 'delayFromFirstProbe']

class Simulation(object):
    def __init__(self, simulation_el):
        self.flows = []
        FlowClassifier_el, = simulation_el.findall("Ipv4FlowClassifier")
        flow_map = {}
        for flow_el in simulation_el.findall("FlowStats/Flow"):
            flow = Flow(flow_el)
            flow_map[flow.flowId] = flow
            self.flows.append(flow)
        for flow_cls in FlowClassifier_el.findall("Flow"):
            flowId = int(flow_cls.get('flowId'))
            flow_map[flowId].fiveTuple = FiveTuple(flow_cls)

        for probe_elem in simulation_el.findall("FlowProbes/FlowProbe"):
            probeId = int(probe_elem.get('index'))
            for stats in probe_elem.findall("FlowStats"):
                flowId = int(stats.get('flowId'))
                s = ProbeFlowStats()
                s.packets = int(stats.get('packets'))
                s.bytes = long(stats.get('bytes'))
                s.probeId = probeId
                if s.packets > 0:
                    s.delayFromFirstProbe =  parse_time_ns(stats.get('delayFromFirstProbeSum')) / float(s.packets)
                else:
                    s.delayFromFirstProbe = 0
                flow_map[flowId].probe_stats_unsorted.append(s)


def main(argv):
    if len(argv) <= 2:
        print "Usage: %s xmlfile simu_duration_seconds" % argv[0]
        print "Examples: python scratch/dcn-flowmon-parse-results.py statistics/Fat-tree.xml 100"
    file_obj = open(argv[1])
    print "Reading XML file ",
    simu_duration_seconds = float(argv[2])

    sys.stdout.flush()
    level = 0
    sim_list = []
    for event, elem in ElementTree.iterparse(file_obj, events=("start", "end")):
        if event == "start":
            level += 1
        if event == "end":
            level -= 1
            if level == 0 and elem.tag == 'FlowMonitor':
                sim = Simulation(elem)
                sim_list.append(sim)
                elem.clear() # won't need this any more
                sys.stdout.write(".")
                sys.stdout.flush()
    print " done."



    flow_count = 0
    total_rx_bits = 0.0
    total_tx_bits = 0.0
    total_mean_delay = 0.0
    total_loss_ratio = 0.0
    total_rx_packets = 0.0
    total_lost_packets = 0.0
    for sim in sim_list:
        print "debug: for sim %s" % sim
        for flow in sim.flows:
            flow_count += 1
            total_rx_packets += flow.rxPackets
            total_lost_packets += flow.lostPackets
            t = flow.fiveTuple
            proto = {6: 'TCP', 17: 'UDP'} [t.protocol]
            print "FlowID: %i (%s %s/%s --> %s/%i)" % \
                (flow.flowId, proto, t.sourceAddress, t.sourcePort, t.destinationAddress, t.destinationPort)
            if flow.txBitrate is None:
                print "\tTX bitrate: None"
            else:
                print "\tTX bitrate: %.2f kbit/s" % (flow.txBitrate*1e-3,)
                total_tx_bits += flow.txBits
            if flow.rxBitrate is None:
                print "\tRX bitrate: None"
            else:
                print "\tRX bitrate: %.2f kbit/s" % (flow.rxBitrate*1e-3,)
                total_rx_bits += flow.rxBits
            if flow.delayMean is None:
                print "\tMean Delay: None"
            else:
                print "\tMean Delay: %.2f ms" % (flow.delayMean*1e3,)
                total_mean_delay += flow.delayMean
            if flow.packetLossRatio is None:
                print "\tPacket Loss Ratio: None"
            else:
                print "\tPacket Loss Ratio: %.2f %%" % (flow.packetLossRatio*100)
                total_loss_ratio += flow.packetLossRatio

            print "\tRx Duration: %.2f seconds" % ( flow.rx_duration)


    print "-- total statictis --"
    print "\t%d number flows" % (flow_count)
    tx_bps = (total_tx_bits / simu_duration_seconds * 1e-6)
    rx_bps = (total_rx_bits / simu_duration_seconds * 1e-6)
    print "\tTX bitrate: %.2f mbit/s" % tx_bps
    print "\tRX bitrate: %.2f mbit/s" % rx_bps
    print "\tUtilization: %.2f %%" % ((tx_bps *2) / (100 * flow_count))
    print "\tMean Delay: %.2f ms" % (total_mean_delay / flow_count *1e3,)
    # print "\tPacket Loss Ratio: %.2f %%" % ( total_loss_ratio / flow_count * 100)
    print "\tPacket Loss Ratio: %.2f %%" % (total_lost_packets / (total_lost_packets+total_rx_packets) * 100)

if __name__ == '__main__':
    main(sys.argv)
