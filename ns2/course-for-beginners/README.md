# NS Simulator Course for Beginners  

原始代码为 2002 年，考虑按 ns-2.35 修改

 Lecture Notes, Sept 2002
                         Univ. de Los Andes,
                           Merida, Venezuela
                   Eitan Altman, Tania Jimenez

  NS InterSIM

                      Toolbox for performance evaluation of
                                 INTERNET PROTOCOLS:

* Performance Evaluation of TCP
    - ex1.tcl Performance Evaluation of TCP and CBR connections sharing a bottleneck link.
    - rdrop.tcl Performance Evaluation of TCP and CBR connections with random drops.
    - ex3.tcl Several TCP connections. Delays and initial trnamission times created at radom.
    - shortTcp.tcl Short TCP files with several source nodes, sharing a single bottleneck link.
      + # 生成队列大小, 带宽, 丢包 3 个文件, 并用于绘图展示
    - shortTcp2.tcl A more sophisticated tcl programming. Extra monitoring features.
* Unicast and multicast routing
    - ex2.tcl Unicast routing.
    - ctr.tcl Multicast routing, CTR.
    - dvmrp.tcl Multicast routing, DVMRP.
    - pimdm.tcl Multicast routing, PIMDM.
    - bst.tcl Multicast routing, bi-directional shared tree.
* RED queue
    - red.tcl TCP connections with a RED bottleneck buffer. Parameters are configured automatically.
    - drptail.tcl The same network as in red.tcl but with a dropt tail buffer. The queue monitoring is done differently.
    - shortRED.tcl This is a script for working with short TCP files with
    - several source nodes, sharing a single bottleneck link with a RED buffer.
* Diffserv
    - diffs.tcl Short TCP files with several source nodes, sharing a single bottleneck link. It allows to how with proper choice of CIR, marking decreases losses of vulnerable packets (syns etc).
* Local Area Networks
    - 802p3.tcl
    - csma.tcl
* Classical Queueing Models
    - mm1.tcl An M/M/1 queue
    - mm1k.tcl An M/M/1 queue with finite capacity
* Mobile networks
    - wrls-dsdv.tcl TCP over a 3 nodes Ad-hoc network with DSDV routing protocol.
    - wrls-dsr.tcl TCP over a 3 nodes Ad-hoc network with DST routing protocol.
    - wrls-aodv.tcl TCP over a 3 nodes Ad-hoc network with AODV routing protocol.
    - wrls-tora1.tcl TCP over a 3 nodes Ad-hoc network with TORA routing protocol.
    - wrls-tora2.tcl TCP over a 4 nodes Ad-hoc network with TORA routing protocol.
    - chain.tcl TCP over a chain of nodes: the impact of increasing the delayed-ack factor
* Others
    - rv1.tcl Testing Random Variables

AWK FILES:
    - avr.awk Computing the average
    - stdv.awk Computing thestandard deviation.

PERL FILES:
    - throughput.pl Computing the throughput
    - column.pl Extracting a column from a file
