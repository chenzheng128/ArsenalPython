# Polly Huang 8-7-98

# Initial setup
source ~/ns-allinone-2.1b4a/ns-2/tcl/http/http-mod.tcl
source dumbbell.tcl
global num_node n

set ns [new Simulator]
$ns set-address 7 24     ;# set-address <bits for node address> <bits for port>

# set up colors for nam 
for {set i 1} {$i <= 30} {incr i} {
    set color [expr $i % 6]
    if {$color == 0} {
	$ns color $i blue
    } elseif {$color == 1} {
	$ns color $i red
    } elseif {$color == 2} {
	$ns color $i green
    } elseif {$color == 3} {
	$ns color $i yellow
    } elseif {$color == 4} {
	$ns color $i brown
    } elseif {$color == 5} {
	$ns color $i black
    }
}

# Create nam trace and generic packet trace
$ns namtrace-all [open out.nam w]
# trace-all is the generic trace we've been using
$ns trace-all [open out.tr w]

create_topology

########################### Modify From Here #####################
## Number of Pages per Session
set numPage 10
set httpSession1 [new HttpSession $ns $numPage [$ns picksrc]]
set httpSession2 [new HttpSession $ns $numPage [$ns picksrc]]

## Inter-Page Interval
## Number of Objects per Page
## Inter-Object Interval
## Number of Packets per Object
## have to set page specific attributes before createPage
## have to set object specific attributes after createPage
$httpSession1 setDistribution interPage_ Exponential 1 ;#in sec
$httpSession1 setDistribution pageSize_ Constant 1 ;# number of objects/page
$httpSession1 createPage
$httpSession1 setDistribution interObject_ Exponential 0.01 ;# in sec
$httpSession1 setDistribution objectSize_ ParetoII 10 1.2 ;# number of packets

# uses default 
$httpSession2 createPage

$ns at 0.1 "$httpSession1 start" ;# in sec as well
$ns at 0.2 "$httpSession2 start"

$ns at 30.0 "finish"

proc finish {} {
	global ns
	$ns flush-trace
	puts "running nam..."
    # exec to run unix command
	exec nam out.nam &
	exit 0
}

# Start the simualtion
$ns run


