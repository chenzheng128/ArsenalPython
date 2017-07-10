
#
# Source: http://netlab.caltech.edu/projects/ns2tcplinux/ns2linux-2.29-linux-2.6.16/scripts/test-linux.tcl
# documentation: http://netlab.caltech.edu/projects/ns2tcplinux/ns2linux-2.29-linux-2.6.16/
# 
# 或者
#
# 从 http://netlab.cs.ucla.edu/tcpsuite/ns-linux-2.31.patch 补丁中还原出的代码
#

set TCP_Variant "Agent/TCP/Fack1"
set TCP_ACK_Variant "Agent/TCPSink/Sack1/DelAck"
set FlowNumber 1
set MainBW "1000Mb"
set SideBW "4000Mb"
#should be 4 times of SideBW
set MainBuffer 2000
#should be 1/4 of BDP
set BDP 30000
set EndTime 200
set MSS 1448 

#constants
set SideDelay "0ms"
set MainDelay "50ms"

set conf [open "config" "r"]
# main capacity  (e.g. 100Mb)
set TCP_Variant [gets $conf]
set TCP_Name [gets $conf]
set FlowNumber [gets $conf]
set MainBW [gets $conf]
set MainDelay [gets $conf]
set MainBuffer [gets $conf]
set SideBW [gets $conf]
set EndTime [gets $conf]
close $conf

set record_config [open "Configuration_Record" w]
puts $record_config "$TCP_Variant (TCP variants)"
puts $record_config "$TCP_Name (TCP Type)"
puts $record_config "$TCP_ACK_Variant (ack variants)"
puts $record_config "$FlowNumber (flow number)"
puts $record_config "$MainBW (main bw)"
puts $record_config "$SideBW (side bw)"
puts $record_config "$MainDelay (main delay)"
puts $record_config "$SideDelay (side delay)"
puts $record_config "$BDP (side buffer)"
puts $record_config "$MainBuffer (main buffer)"
puts $record_config "$MSS (packet size)"
puts $record_config "$EndTime (finish time)"
close $record_config

#Create a simulator object
set ns [new Simulator]

proc monitor {interval} {
    global FlowNumber tcp ns
    set nowtime [$ns now]

    for {set i 0} {$i < $FlowNumber} {incr i 1} {
        set win [open result$i a]
	puts $win "$nowtime [$tcp($i) set cwnd_] [$tcp($i) set ack_]"
	close $win
    }
    $ns after $interval "monitor $interval"
}


#Define a 'finish' procedure
proc finish {} {
#    global ns tf
#    $ns flush-trace
#    close $tf
    exit 0
}

#Create four nodes
set bs [$ns node]
set br [$ns node]

#Create links between the nodes
$ns duplex-link $bs $br $MainBW $MainDelay DropTail
#Set Queue Size of link (bs-br) to 
$ns queue-limit $bs $br $MainBuffer

#set tf [open "traceall" "w"]
#$ns trace-all $tf


#Setup TCP connections
for {set i 0} {$i < $FlowNumber} {incr i 1} {
	#setup topology
        set win [open result$i w]
	close $win
	set sendNode($i) [$ns node]
	set rcvNode($i) [$ns node]
	$ns duplex-link $sendNode($i) $bs $SideBW $SideDelay DropTail
	$ns duplex-link $br $rcvNode($i) $SideBW $SideDelay DropTail
	$ns queue-limit $sendNode($i) $bs $BDP
	$ns queue-limit $br $rcvNode($i) $BDP

	#setup sender side	
	set tcp($i) [new $TCP_Variant]
	$tcp($i) set packetSize_ $MSS
	$tcp($i) set window_ $BDP
        $tcp($i) set timestamps_ true
	$tcp($i) set partial_ack_ true

#        $tcp($i) set windowOption_ $TCP_Name

	$ns attach-agent $sendNode($i) $tcp($i)
	
	#setup receiver side
	set sink($i) [new $TCP_ACK_Variant]
	$sink($i) set generateDSacks_ false
	$sink($i) set ts_echo_rfc1323_ true
	$sink($i) set interval_ 200ms
	$ns attach-agent $rcvNode($i) $sink($i)

	#logical connection
	$ns connect $tcp($i) $sink($i)

	#Setup a FTP over TCP connection
	set ftp($i) [new Application/FTP]
	$ftp($i) attach-agent $tcp($i)
	$ftp($i) set type_ FTP

	$ns at 0 "$tcp($i) select_ca $TCP_Name"

	$ns at 0 "$ftp($i) start"
	$ns at $EndTime+1 "$ftp($i) stop"
}

#call the monitor at the end
$ns at 0 "monitor 0.5"

#Call the finish procedure after 1 seconds of simulation time
$ns at $EndTime+2 "finish"

puts "start"
#Run the simulation
$ns run

