set ns [new Simulator] 

# There are several sources each generating many TCP sessions sharing a bottleneck 
# link and a single destination. Their number is given by the paramter NodeNb

#     S(1) ----- E(1) ----
#     .                   |
#     .     ---- E(i) ---Core---- Ed -------- D
#     .                   |
#     S(NodeNb)- E(NodeNb)-



set cir0       30000; # policing parameter
set cir1       30000; # policing parameter
set pktSize    1000
set NodeNb       20; # Number of source nodes
set NumberFlows 160 ; # Number of flows per source node 
set sduration   25; # Duration of simulation


#Define different colors for data flows (for NAM)
$ns color 1 Blue
$ns color 2 Red
$ns color 3 Green
$ns color 4 Brown
$ns color 5 Yellow
$ns color 6 Black
                   


set Out [open Out.ns w];   # file containing transfer 
                           # times of different connections
set Conn [open Conn.tr w]; # file containing the number of connections 

set tf   [open out.tr w];  # Open the Trace file
$ns trace-all $tf    

#Open the NAM trace file
set file2 [open out.nam w]
# $ns namtrace-all $file2 


# We define three files that will be used to trace the queue size,
# the bandwidth and losses at the bottleneck.


# defining the topology
set D    [$ns node]
set Ed   [$ns node]
set Core [$ns node]

set flink [$ns simplex-link $Core $Ed 10Mb 1ms dsRED/core]
$ns queue-limit  $Core $Ed  100
$ns simplex-link $Ed $Core 10Mb 1ms dsRED/edge
$ns duplex-link  $Ed   $D  10Mb   0.01ms DropTail


for {set j 1} {$j<=$NodeNb} { incr j } {
 set S($j) [$ns node]
 set E($j) [$ns node]
 $ns duplex-link  $S($j) $E($j)  6Mb   0.01ms DropTail
 $ns simplex-link $E($j) $Core   6Mb   0.1ms dsRED/edge
 $ns simplex-link $Core  $E($j)  6Mb   0.1ms dsRED/core
 $ns queue-limit $S($j) $E($j) 100
}

#Config Diffserv
set qEdC    [[$ns link $Ed $Core] queue]
$qEdC       meanPktSize 40
$qEdC   set numQueues_   1
$qEdC    setNumPrec      2
for {set j 1} {$j<=$NodeNb} { incr j } {
 $qEdC addPolicyEntry [$D id] [$S($j) id] TSW2CM 10 $cir0 0.02
}
$qEdC addPolicerEntry TSW2CM 10 11
$qEdC addPHBEntry  10 0 0 
$qEdC addPHBEntry  11 0 1 
$qEdC configQ 0 0 10 30 0.1
$qEdC configQ 0 1 10 30 0.1

$qEdC printPolicyTable
$qEdC printPolicerTable

set qCEd    [[$ns link $Core $Ed] queue]
# set qCEd    [$flink queue]
$qCEd     meanPktSize $pktSize
$qCEd set numQueues_   1
$qCEd set NumPrec       2
$qCEd addPHBEntry  10 0 0 
$qCEd addPHBEntry  11 0 1 
$qCEd setMREDMode RIO-D
$qCEd configQ 0 0 15 45  0.5 0.01
$qCEd configQ 0 1 15 45  0.5 0.01


for {set j 1} {$j<=$NodeNb} { incr j } {
 set qEC($j) [[$ns link $E($j) $Core] queue]
 $qEC($j) meanPktSize $pktSize
 $qEC($j) set numQueues_   1
 $qEC($j) setNumPrec      2
 $qEC($j) addPolicyEntry [$S($j) id] [$D id] TSW2CM 10 $cir1 0.02
 $qEC($j) addPolicerEntry TSW2CM 10 11
 $qEC($j) addPHBEntry  10 0 0 
 $qEC($j) addPHBEntry  11 0 1 
# $qEC($j) configQ 0 0 20 40 0.02
 $qEC($j) configQ 0 0 10 20 0.1
 $qEC($j) configQ 0 1 10 20 0.1

$qEC($j) printPolicyTable
$qEC($j) printPolicerTable
 
 set qCE($j) [[$ns link $Core $E($j)] queue]
 $qCE($j) meanPktSize      40
 $qCE($j) set numQueues_   1
 $qCE($j) setNumPrec      2
 $qCE($j) addPHBEntry  10 0 0 
 $qCE($j) addPHBEntry  11 0 1 
# $qCE($j) configQ 0 0 20 40 0.02
 $qCE($j) configQ 0 0 10 20 0.1
 $qCE($j) configQ 0 1 10 20 0.1

}


# set flow monitor
set monfile [open mon.tr w]
set fmon [$ns makeflowmon Fid]
$ns attach-fmon $flink $fmon
$fmon attach $monfile

#TCP Sources, destinations, connections
for {set i 1} {$i<=$NodeNb} { incr i } {
for {set j 1} {$j<=$NumberFlows} { incr j } {
set tcpsrc($i,$j) [new Agent/TCP/Newreno]
set tcp_snk($i,$j) [new Agent/TCPSink]
set k [expr $i*1000 +$j];
$tcpsrc($i,$j) set fid_ $k
$tcpsrc($i,$j) set window_ 2000
$ns attach-agent $S($i) $tcpsrc($i,$j)
$ns attach-agent $D $tcp_snk($i,$j)
$ns connect $tcpsrc($i,$j) $tcp_snk($i,$j)
set ftp($i,$j) [$tcpsrc($i,$j) attach-source FTP]
} }
# Generators for random size of files. 
set rng1 [new RNG]
$rng1 seed 22

# Random inter-arrival times of TCP transfer at each source i
set RV [new RandomVariable/Exponential]
$RV set avg_ 0.2
$RV use-rng $rng1 

# Random size of files to transmit 
set RVSize [new RandomVariable/Pareto]
$RVSize set avg_ 10000 
$RVSize set shape_ 1.25
$RVSize use-rng $rng1

# dummy command
set t [$RVSize value]

# We now define the beginning times of transfers and the transfer sizes
# Arrivals of sessions follow a Poisson process.
#
for {set i 1} {$i<=$NodeNb} { incr i } {
     set t [$ns now]

     for {set j 1} {$j<=$NumberFlows} { incr j } {
	 # set the beginning time of next transfer from source and attributes
	 $tcpsrc($i,$j) set sess $j
	 $tcpsrc($i,$j) set node $i
	 set t [expr $t + [$RV value]]
	 $tcpsrc($i,$j) set starts $t
         $tcpsrc($i,$j) set size [expr [$RVSize value]]
  $ns at [$tcpsrc($i,$j) set starts] "$ftp($i,$j) send [$tcpsrc($i,$j) set size]"
  $ns at [$tcpsrc($i,$j) set starts ] "countFlows $i 1"

}}

for {set j 1} {$j<=$NodeNb} { incr j } {
set Cnts($j) 0
}   

# The following procedure is called whenever a connection ends
Agent/TCP instproc done {} {
global tcpsrc NodeNb NumberFlows ns RV ftp Out tcp_snk RVSize 
# print in $Out: node, session, start time,  end time, duration,      
# trans-pkts, transm-bytes, retrans-bytes, throughput   
  set duration [expr [$ns now] - [$self set starts] ] 
  set i [$self set node] 
  set j [$self set sess] 
  set time [$ns now] 
  puts $Out "$i \t $j \t $time \t\
      $time \t $duration \t [$self set ndatapack_] \t\
      [$self set ndatabytes_] \t [$self set  nrexmitbytes_] \t\
      [expr [$self set ndatabytes_]/$duration ]"    

	  # update the number of flows
      countFlows [$self set node] 0

}

# The following recursive procedure updates the number of connections 
# as a function of time. Each 0.2 it prints them into $Conn. This
# is done by calling the procedure with the "sign" parameter equal
# 3 (in which case the "ind" parameter does not play a role). The
# procedure is also called by the "done" procedure whenever a connection
# from source i ends by assigning the "sign" parameter 0, or when
# it begins, by assigning it 1 (i is passed through the "ind" variable).
#
proc countFlows { ind sign } {
global Cnts Conn NodeNb
set ns [Simulator instance]
      if { $sign==0 } { set Cnts($ind) [expr $Cnts($ind) - 1] 
} elseif { $sign==1 } { set Cnts($ind) [expr $Cnts($ind) + 1] 
} else { 
  puts -nonewline $Conn "[$ns now] \t"
  set sum 0
  for {set j 1} {$j<=$NodeNb} { incr j } {
    puts -nonewline $Conn "$Cnts($j) \t"
    set sum [expr $sum + $Cnts($j)]
  }
  puts $Conn "$sum"
  puts $Conn ""
  $ns at [expr [$ns now] + 0.2] "countFlows 1 3"
puts "in count"
} }

#Define a 'finish' procedure
proc finish {} {
        global ns tf file2
        $ns flush-trace
        close $file2 
        exit 0
}         

$ns at 0.5 "countFlows 1 3"
$ns at [expr $sduration - 0.01] "$fmon dump"
$ns at [expr $sduration - 0.001] "$qCEd printStats"
$ns at $sduration "finish"


$ns run


