set ns [new Simulator] 

# There are several sources of TCP sharing a bottleneck link
# and a single destination. Their number is given by the paramter NodeNb

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

# We define three files that will be used to trace the queue size,
# the bandwidth and losses at the bottleneck.
set qsize [open queuesize.tr w]
set qbw   [open queuebw.tr   w]
set qlost [open queuelost.tr w]   

# defining the topology
set N [$ns node]
set D [$ns node]
$ns duplex-link $N $D 2Mb 1ms DropTail
$ns queue-limit $N $D 3000 

# Number of sources
set NodeNb 6 
# Number of flows per source node 
set NumberFlows 530

#Nodes and links
for {set j 1} {$j<=$NodeNb} { incr j } {
set S($j) [$ns node]
$ns duplex-link $S($j) $N 100Mb 1ms DropTail
$ns queue-limit $S($j) $N 1000
}

#TCP Sources and destinations
for {set i 1} {$i<=$NodeNb} { incr i } {
for {set j 1} {$j<=$NumberFlows} { incr j } {
set tcpsrc($i,$j) [new Agent/TCP/Newreno]
$tcpsrc($i,$j) set window_ 2000
set tcp_snk($i,$j) [new Agent/TCPSink]
 }
}


#Connections
for {set i 1} {$i<=$NodeNb} { incr i } {
for {set j 1} {$j<=$NumberFlows} { incr j } {
$ns attach-agent $S($i) $tcpsrc($i,$j)
$ns attach-agent $D $tcp_snk($i,$j)
$ns connect $tcpsrc($i,$j) $tcp_snk($i,$j)
 }
}

#FTP sources
for {set i 1} {$i<=$NodeNb} { incr i } {
for {set j 1} {$j<=$NumberFlows} { incr j } {
set ftp($i,$j) [$tcpsrc($i,$j) attach-source FTP]
 }
}

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

	  # set the beginning time of next transfer from source i
	  set t [expr $t + [$RV value]]
	  set Conct($i,$j) $t

	  # set the size of next transfer from source i
	  set Size($i,$j) [expr [$RVSize value]]
	  $ns at $Conct($i,$j) "$ftp($i,$j) send $Size($i,$j)"

	  # update the number of flows
 	 $ns at $Conct($i,$j) "countFlows $i 1"
      }
}

# Next is a recursive procedure that checks for each session whether 
# it has ended. The procedure calls itself each 0.1 sec (this is
# set in the variable "time").
# If a connection has ended then we print in the file $Out
#    * the connection identifiers i and j,
#    * the start and end time of the connection,
#    * the throughput of the session,
#    * the size of the transfer in bytes
# and we further define another beginning of transfer after a random time.

proc Test {} {
global Conct tcpsrc Size NodeNb NumberFlows ns RV ftp Out tcp_snk RVSize 
set time 0.1
for {set i 1} {$i<=$NodeNb} { incr i } {
for {set j 1} {$j<=$NumberFlows} { incr j } {

# We now check if the transfer is over
if {[$tcpsrc($i,$j) set ack_]==[$tcpsrc($i,$j) set maxseq_]} {
    if {[$tcpsrc($i,$j) set ack_]>=0} {
# If the transfer is over, we print relevant information in $Out 
puts $Out "$i,$j\t$Conct($i,$j)\t[expr [$ns now]]\t\
   [expr ($Size($i,$j))/(1000*([expr [$ns now]] - $Conct($i,$j)))]\t$Size($i,$j)"
countFlows $i 0
$tcpsrc($i,$j)  reset
$tcp_snk($i,$j) reset
}}}}
$ns at [expr [$ns now]+$time] "Test"
}

for {set j 1} {$j<=$NodeNb} { incr j } {
set Cnts($j) 0
}

#
# The following recursive procedure updates the number of connections 
# as a function of time. Each 0.2 it prints them into $Conn. This
# is done by calling the procedure with the "sign" parameter equal
# 3 (in which case the "ind" parameter does not play a role). The
# procedure is also called by the Test procedure whenever a connection
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
 }    
}

#Define a 'finish' procedure
proc finish {} {
        global ns tf qsize qbw qlost
        $ns flush-trace
	close $qsize
	close $qbw
	close $qlost   
# Execute xgraph to display the queue size, queue bandwidth and loss rate
exec xgraph queuesize.tr -geometry 800x400 -t "Queue size" -x "secs" -y "# packets" &
exec xgraph queuebw.tr -geometry 800x400 -t "bandwidth" -x "secs" -y "Kbps" -fg white &
exec xgraph queuelost.tr -geometry 800x400 -t "# Packets lost" -x "secs" -y "packets" -fg red &
        exit 0
}         


####################
# QUEUE MONiTORiNG #
####################

set qfile [$ns monitor-queue $N $D  [open queue.tr w] 0.05]
[$ns link $N $D] queue-sample-timeout; 

# The following procedure records queue size, bandwidth and loss rate  
proc record {} {
global ns qfile qsize qbw qlost N D 
set time 0.05
set now [$ns now]

# print in the file $qsize the current queue size
# print in the file $qbw the current used bandwidth
# print in the file $qlost the loss rate

$qfile instvar parrivals_ pdepartures_ bdrops_ bdepartures_ pdrops_ 
puts $qsize "$now [expr $parrivals_-$pdepartures_-$pdrops_]"
puts $qbw   "$now [expr $bdepartures_*8/1024/$time]"
set bdepartures_ 0                                
puts $qlost "$now [expr $pdrops_/$time]"
$ns at [expr $now+$time] "record"
}   

$ns at 0.0 "record"
$ns at 0.01 "Test"
$ns at 0.5 "countFlows 1 3"
$ns at 20 "finish"

$ns run


