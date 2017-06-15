# Author: Jae Chung
# Date:   7/17/99
#
#
#        s1                 s3
#         \                 /
# 5Mb,3ms \    2Mb,10ms   / 5Mb,3ms
#           r1 --------- r2
# 5Mb,3ms /               \ 5Mb,3ms
#         /                 \
#        s2                 s4 
#

set ns [new Simulator]

#Define different colors for data flows
$ns color 1 Red
$ns color 2 Blue


#Open the nam trace file
set nf [open out.nam w]
set tf [open out.tr w]
$ns namtrace-all $nf
$ns trace-all $tf

#Define a 'finish' procedure
proc finish {} {
        global ns nf tf
        $ns flush-trace
        #Close the trace file
        close $nf
        close $tf
        #Execute nam on the trace file
        exec nam out.nam &
        exit 0
}

set node_(s1) [$ns node]
set node_(s2) [$ns node]
set node_(r1) [$ns node]
set node_(r2) [$ns node]
set node_(s3) [$ns node]
set node_(s4) [$ns node]

$ns duplex-link $node_(s1) $node_(r1) 5Mb 3ms DropTail 
$ns duplex-link $node_(s2) $node_(r1) 5Mb 3ms DropTail 
$ns duplex-link $node_(r1) $node_(r2) 2Mb 10ms RED 
$ns duplex-link $node_(s3) $node_(r2) 5Mb 3ms DropTail 
$ns duplex-link $node_(s4) $node_(r2) 5Mb 3ms DropTail 

#Setup RED queue parameter
$ns queue-limit $node_(r1) $node_(r2) 20
Queue/RED set thresh_ 5
Queue/RED set maxthresh_ 10
Queue/RED set q_weight_ 0.002
Queue/RED set ave_ 0

$ns duplex-link-op $node_(r1) $node_(r2) queuePos 0.5

$ns duplex-link-op $node_(s1) $node_(r1) orient right-down
$ns duplex-link-op $node_(s2) $node_(r1) orient right-up
$ns duplex-link-op $node_(r1) $node_(r2) orient right
$ns duplex-link-op $node_(s3) $node_(r2) orient left-down
$ns duplex-link-op $node_(s4) $node_(r2) orient left-up


#Setup a MM UDP connection
set udp_s [new Agent/UDP/UDPmm]
set udp_r [new Agent/UDP/UDPmm]
$ns attach-agent $node_(s1) $udp_s
$ns attach-agent $node_(s3) $udp_r
$ns connect $udp_s $udp_r
$udp_s set packetSize_ 1000
$udp_r set packetSize_ 1000
$udp_s set fid_ 1
$udp_r set fid_ 1

#Setup a MM Application
set mmapp_s [new Application/MmApp]
set mmapp_r [new Application/MmApp]
$mmapp_s attach-agent $udp_s
$mmapp_r attach-agent $udp_r
$mmapp_s set pktsize_ 1000
$mmapp_s set random_ false

#Setup a TCP connection
set tcp [$ns create-connection TCP/Reno $node_(s2) TCPSink $node_(s4) 0]
$tcp set window_ 15
$tcp set fid_ 2

#Setup a FTP Application
set ftp [$tcp attach-source FTP]

#Simulation Scenario
$ns at 0.0 "$ftp start"
$ns at 1.0 "$mmapp_s start"
$ns at 7.0 "finish"

$ns run





