# Author: Jae Chung
# Date:   7/20/99
#
# This file is modified from 
# "ns-2/tcl/ex/lantest.tcl"

set opt(tr)	"out.tr"
set opt(namtr)	"out.nam"
set opt(seed)	0
set opt(stop)	5
set opt(node)	8

set opt(qsize)	100
set opt(bw)	10Mb
set opt(delay)	1ms
set opt(ll)	LL
set opt(ifq)	Queue/DropTail
set opt(mac)	Mac/Csma/Ca
set opt(chan)	Channel
set opt(tcp)	TCP/Reno
set opt(sink)	TCPSink

set opt(app)	FTP


proc finish {} {
	global ns opt trfd ntrfd

	$ns flush-trace
	close $trfd
        close $ntrfd
	exec nam $opt(namtr) &
	exit 0
}

proc create-trace {} {
	global ns opt

	set trfd [open $opt(tr) w]
	$ns trace-all $trfd
	return $trfd
}

proc create-namtrace {} {
        global ns opt

        set ntrfd [open $opt(namtr) w]
        $ns namtrace-all $ntrfd
}

proc create-topology {} {
	global ns opt
	global lan node source node0

	set num $opt(node)
	for {set i 0} {$i < $num} {incr i} {
		set node($i) [$ns node]
		lappend nodelist $node($i)
	}

	set lan [$ns newLan $nodelist $opt(bw) $opt(delay) \
			-llType $opt(ll) -ifqType $opt(ifq) \
			-macType $opt(mac) -chanType $opt(chan)]

	set node0 [$ns node]
	$ns duplex-link $node0 $node(0) 2Mb 2ms DropTail

	$ns duplex-link-op $node0 $node(0) orient right

}

## MAIN ##

set ns [new Simulator]
set trfd [create-trace]
set ntrfd [create-namtrace]

create-topology

set tcp0 [$ns create-connection TCP/Reno $node0 TCPSink $node(7) 0]
$tcp0 set window_ 15

set ftp0 [$tcp0 attach-app FTP]

$ns at 0.0 "$ftp0 start"
$ns at $opt(stop) "finish"

$ns run
