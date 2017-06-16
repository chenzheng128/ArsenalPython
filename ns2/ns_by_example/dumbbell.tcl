# Created by Polly Huang
# Simple 4-node star topology
#        8    7       2    3
#           \ |       | / 
#        9 -- 1 ----- 0 -- 4
#           / |       | \
#        10   11      6    5   

proc create_topology {} {
global ns n num_node
set num_node 12

for {set i 0} {$i < $num_node} {incr i} {
	set n($i) [$ns node]
}

$ns set src_ [list 2 3 4 5 6]
$ns set dst_ [list 7 8 9 10 11]

# EDGES (from-node to-node length a b):
$ns duplex-link $n(0) $n(1) 1.5Mb 40ms DropTail
$ns duplex-link $n(0) $n(2) 10Mb 20ms DropTail
$ns duplex-link $n(0) $n(3) 10Mb 20ms DropTail
$ns duplex-link $n(0) $n(4) 10Mb 20ms DropTail
$ns duplex-link $n(0) $n(5) 10Mb 20ms DropTail
$ns duplex-link $n(0) $n(6) 10Mb 20ms DropTail
$ns duplex-link $n(1) $n(7) 10Mb 20ms DropTail
$ns duplex-link $n(1) $n(8) 10Mb 20ms DropTail
$ns duplex-link $n(1) $n(9) 10Mb 20ms DropTail
$ns duplex-link $n(1) $n(10) 10Mb 20ms DropTail
$ns duplex-link $n(1) $n(11) 10Mb 20ms DropTail

$ns duplex-link-op $n(0) $n(1) orient left
$ns duplex-link-op $n(0) $n(2) orient up
$ns duplex-link-op $n(0) $n(3) orient right-up
$ns duplex-link-op $n(0) $n(4) orient right
$ns duplex-link-op $n(0) $n(5) orient right-down
$ns duplex-link-op $n(0) $n(6) orient down
$ns duplex-link-op $n(1) $n(7) orient up
$ns duplex-link-op $n(1) $n(8) orient left-up
$ns duplex-link-op $n(1) $n(9) orient left 
$ns duplex-link-op $n(1) $n(10) orient left-down
$ns duplex-link-op $n(1) $n(11) orient down
}
# end of create_topology
