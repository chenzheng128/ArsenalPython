# The preamble
set ns [new Simulator]			;# initialise the simulation

#Define different colors for data flows (for NAM)
$ns color 1 Blue
$ns color 2 Red

# Predefine tracing
set f [open out.tr w]
$ns trace-all $f
set nf [open out.nam w]
$ns namtrace-all $nf

#\clearpage
# so, we lied.  now, we define the topology
#
#       n0
#         \bs
#      5Mb \bs
#      2ms  \bs
#            \bs
#             n2 --------- n3
#            /     1.5Mb
#      5Mb  /       10ms
#      2ms /
#         /
#       n1
#
set n0 [$ns node]
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]

$ns duplex-link $n0 $n2 5Mb 2ms DropTail
$ns duplex-link $n1 $n2 5Mb 2ms DropTail
$ns duplex-link $n2 $n3 1.5Mb 10ms DropTail

# Some agents.
set udp0 [new Agent/UDP]		;# A UDP agent;
$ns attach-agent $n0 $udp0		;# on node $n0;
set cbr0 [new Application/Traffic/CBR]		;# A CBR traffic generator agent;
$cbr0 attach-agent $udp0		;# attached to the UDP agent;
$udp0 set class_ 0			;# actually, the default, but\ldots;
$udp0 set fid_ 2  			;# set udp color 2 Red

set null0 [new Agent/Null]		;# Its sink;
$ns attach-agent $n3 $null0		;# on node $n3;

$ns connect $udp0 $null0
$ns at 1.0 "$cbr0 start"

puts [$cbr0 set packetSize_]
puts [$cbr0 set interval_]

# A FTP over TCP/Tahoe from $n1 to $n3, flowid 2
set tcp [new Agent/TCP]
$tcp set class_ 1
$ns attach-agent $n1 $tcp

set sink [new Agent/TCPSink]
$ns attach-agent $n3 $sink

set ftp [new Application/FTP]	;# TCP does not generate its own traffic;
$ftp attach-agent $tcp
$ns at 1.2 "$ftp start"
$ftp set fid_ 1 				;# set tcp color 1 Blue

$ns connect $tcp $sink
$ns at 1.35 "$ns detach-agent $n0 $tcp ; $ns detach-agent $n3 $sink"

# \clearpage
# The simulation runs for \(3s\).
# The simulation comes to an end when the scheduler invokes the finish{} procedure below.
# This procedure closes all trace files, and invokes nam visualization on one of the trace files.

$ns at 3.0 "finish"
proc finish {} {
        global ns f nf
        $ns flush-trace
        close $f
        close $nf

        puts "running nam..."
        exec nam out.nam &
        exit 0
}

# Finally, start the simulation.
$ns run