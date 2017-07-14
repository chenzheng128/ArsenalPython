
#N=2 时的拓扑
#                0
#    1Gb/0.05ms   \    1Gb/0.05ms
#                  2 ------------- 3
#    1Gb/0.05ms   /
#                1
#




set N 2
set B 200
set K 35
set RTT 0.0002 ;#0.2ms
set flow_tcp dctcp

set simulationTime 2.0

set sourceAlg DC-TCP-Sack
set switchAlg RED
set lineRate 1Gb
set inputLineRate 1Gb
set DCTCP_g_ 0.0625
set ackRatio 1
set packetSize 1460 ;#bytes

set cwndInterval 0.001

set ns [new Simulator]

puts "注意：如果下面出现 can't read dctcp_g_: no such variable 错误，说明 ns 没有正常的加入 dctcp 补丁. 请重新 patch 后重新编译 ns"
puts "检查DCTCP默认参数: dctcp_ [Agent/TCP set dctcp_]"
puts "检查DCTCP默认参数: dctcp_g_ [Agent/TCP set dctcp_g_]"
puts "检查DCTCP默认参数: dctcp_alpha_ [Agent/TCP set dctcp_alpha_]"


set enableNAM 0
set enableALL 0

# set up tracing
if { $enableALL != 0 } {
set tracefd  [open tcp-all.tr w]
$ns trace-all $tracefd
}
if { $enableNAM != 0} {
set namtrace [open out.nam w]
$ns namtrace-all $namtrace
}


Agent/TCP set ecn_ 1
Agent/TCP set old_ecn_ 1
Agent/TCP set packetSize_ $packetSize
Agent/TCP/FullTcp set segsize_ $packetSize
Agent/TCP set window_ 200
Agent/TCP set slow_start_restart_ false
Agent/TCP set tcpTick_ 0.01
Agent/TCP set minrto_ 0.2 ; # minRTO = 200ms
Agent/TCP set windowOption_ 0

if {[string compare $sourceAlg "DC-TCP-Sack"] == 0} {
    Agent/TCP set dctcp_ true
    Agent/TCP set dctcp_g_ $DCTCP_g_;
}

Agent/TCP set abc $DCTCP_g_;

Agent/TCP/FullTcp set segsperack_ $ackRatio;
Agent/TCP/FullTcp set spa_thresh_ 3000;
Agent/TCP/FullTcp set interval_ 0.04 ; #delayed ACK interval = 40ms

Queue set limit_ 1000

Queue/RED set bytes_ false
Queue/RED set queue_in_bytes_ true
Queue/RED set mean_pktsize_ $packetSize
Queue/RED set setbit_ true
Queue/RED set gentle_ false
Queue/RED set q_weight_ 1.0
Queue/RED set mark_p_ 1.0
Queue/RED set thresh_ [expr $K]
Queue/RED set maxthresh_ [expr $K]

DelayLink set avoidReordering_ true

#cwndfile
for {set i 0} {$i < $N} {incr i} {

	set cwndfile($i) [open cwnd-$flow_tcp$i.tr w]

}

$ns color 0 Red
$ns color 1 Orange
$ns color 2 Yellow
$ns color 3 Green
$ns color 4 Blue
$ns color 5 Violet
$ns color 6 Brown
$ns color 7 Black

for {set i 0} {$i < $N} {incr i} {
    set n($i) [$ns node]
}

set nqueue [$ns node]
set nclient [$ns node]


$nqueue color red
$nqueue shape box
$nclient color blue

for {set i 0} {$i < $N} {incr i} {
    $ns duplex-link $n($i) $nqueue $inputLineRate [expr $RTT/4] DropTail
    $ns duplex-link-op $n($i) $nqueue queuePos 0.25
}


$ns simplex-link $nqueue $nclient $lineRate [expr $RTT/4] $switchAlg
$ns simplex-link $nclient $nqueue $lineRate [expr $RTT/4] DropTail
$ns queue-limit $nqueue $nclient $B

$ns duplex-link-op $nqueue $nclient color "green"
$ns duplex-link-op $nqueue $nclient queuePos 0.25


for {set i 0} {$i < $N} {incr i} {
    if {[string compare $sourceAlg "Newreno"] == 0 || [string compare $sourceAlg "DC-TCP-Newreno"] == 0} {
	set tcp($i) [new Agent/TCP/Newreno]
	set sink($i) [new Agent/TCPSink]
    }
    if {[string compare $sourceAlg "Sack"] == 0 || [string compare $sourceAlg "DC-TCP-Sack"] == 0} {
        set tcp($i) [new Agent/TCP/FullTcp/Sack]
	set sink($i) [new Agent/TCP/FullTcp/Sack]
	$sink($i) listen
    }

    $ns attach-agent $n($i) $tcp($i)
    $ns attach-agent $nclient $sink($i)

    $tcp($i) set fid_ [expr $i]
    $sink($i) set fid_ [expr $i]

    $ns connect $tcp($i) $sink($i)
}


for {set i 0} {$i < $N} {incr i} {
    set ftp($i) [new Application/FTP]
    $ftp($i) attach-agent $tcp($i)
}



for {set i 0} {$i < $N} {incr i} {

    #$ns at [expr 0.0 + $simulationTime * $i / ($N + 0.0001)] "$ftp($i) start"
    $ns at 0.0 "$ftp($i) start"

    $ns at [expr $simulationTime] "$ftp($i) stop"
}

#record the cwnd
proc recordCwnd {} {

        global  cwndInterval N tcp cwndfile
        #Get an instance of the simulator
        set ns [Simulator instance]
        #Set the time after which the procedure should be called again

        #Get the current time
        set now [$ns now]

        #Get the cwnd of tcp
       for {set i 0} {$i < $N} {incr i} {
        set cwnd($i) [$tcp($i) set cwnd_]
        }
       for {set i 0} {$i < $N} {incr i} {
        puts $cwndfile($i) "$now $cwnd($i)"
        }
        #Re-schedule the procedure
        $ns at [expr $now+$cwndInterval] "recordCwnd"
}

proc finish {} {
        global ns enableNAM namfile enableALL tracefd
        $ns flush-trace

       if {$enableALL != 0} {
		close $tracefd
		}
       if {$enableNAM != 0} {
	    close $namtrace
	    exec nam out.nam &
		}

		exec xgraph  cwnd-dctcp0.tr  &
		exec xgraph  cwnd-dctcp1.tr  &

	exit 0
}


set qfile [open queue.tr w]
set qmon [$ns monitor-queue $nqueue $nclient $qfile 0.0001]
[$ns link $nqueue $nclient] queue-sample-timeout

$ns at 0 "recordCwnd"

$ns at [expr 0.1+$simulationTime] "finish"

$ns run
