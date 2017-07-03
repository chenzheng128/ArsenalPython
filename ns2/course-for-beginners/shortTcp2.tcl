set ns [new Simulator] 

# There are several sources each generating many TCP sessions sharing a bottleneck
# link and a single destination. Their number is given by the paramter NodeNb

#  	S(1)	    ----
#       .  		|
#	.    	    ---- ---- N -------- D(1)...D(NodeNb)
#       .  		|
#  	S(NodeNb)   ----

# Next file will contain the transfer time of different connections
set Out [open Out.ns w]
# Next file will contain the number of connections
set Conn [open Conn.tr w]
#Open the Trace file
set tf [open out.tr w]
$ns trace-all $tf

# defining the topology
set N [$ns node]
set D [$ns node]
$ns duplex-link $N $D 2Mb 1ms DropTail
$ns queue-limit $N $D 3000

set NodeNb 6
# Number of flows per source node
set NumberFlows 530

#Nodes and links
for {set j 1} {$j<=$NodeNb} { incr j } {
set S($j) [$ns node]
$ns duplex-link $S($j) $N 100Mb 1ms DropTail
$ns queue-limit $S($j) $N 1000
}

#TCP Sources, destinations, connections
for {set i 1} {$i<=$NodeNb} { incr i } {
for {set j 1} {$j<=$NumberFlows} { incr j } {
set tcpsrc($i,$j) [new Agent/TCP/Newreno]
set tcp_snk($i,$j) [new Agent/TCPSink]
$tcpsrc($i,$j) set window_ 2000
$ns attach-agent $S($i) $tcpsrc($i,$j)
$ns attach-agent $D $tcp_snk($i,$j)
$ns connect $tcpsrc($i,$j) $tcp_snk($i,$j)
set ftp($i,$j) [$tcpsrc($i,$j) attach-source FTP]
} }

# Generators for random size of files.
set rng1 [new RNG]
$rng1 seed 0
set rng2 [new RNG]
$rng2 seed 0

# Random inter-arrival times of TCP transfer at each source i
set RV [new RandomVariable/Exponential]
$RV set avg_ 0.045
$RV use-rng $rng1

# Random size of files to transmit
set RVSize [new RandomVariable/Pareto]
$RVSize set avg_ 10000
$RVSize set shape_ 1.5
$RVSize use-rng $rng2

# We now define the beginning times of transfers and the transfer sizes
# Arrivals of sessions follow a Poisson process.
#
for {set i 1} {$i<=$NodeNb} { incr i } {
     set t [$ns now]
     for {set j 1} {$j<=$NumberFlows} { incr j } {
	 # set the beginning time of next transfer from source and attributes
	 set t [expr $t + [$RV value]]
	 $tcpsrc($i,$j) set starts $t
	 $tcpsrc($i,$j) set sess $j
	 $tcpsrc($i,$j) set node $i
         $tcpsrc($i,$j) set size [expr [$RVSize value]]

  $ns at [$tcpsrc($i,$j) set starts] "$ftp($i,$j) send [$tcpsrc($i,$j) set size]"

	  # update the number of flows
 	 $ns at [$tcpsrc($i,$j) set starts] "countFlows $i 1"
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
  puts $Out "[$self set node] \t [$self set sess] \t [$self set starts] \t\
      [$ns now] \t $duration \t [$self set ndatapack_] \t\
      [$self set ndatabytes_] \t [$self set  nrexmitbytes_] \t\
      [expr [$self set ndatabytes_]/$duration ]"
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
  $ns at [expr [$ns now] + 0.2] "countFlows 1 3"
} }

#Define a 'finish' procedure
proc finish {} {
        global ns tf
        $ns flush-trace
	close $tf
        exit 0
}

$ns at 0.5 "countFlows 1 3"
$ns at 20 "finish"

$ns run
