#Create a simulator object
set ns [new Simulator]

#Create two nodes and a link
set bs [$ns node]
set br [$ns node]
$ns duplex-link $bs $br 100Mb 10ms DropTail

#setup sender side	
set tcp [new Agent/TCP/Linux]
$tcp set timestamps_ true
#$tcp set windowOption_ 8
$ns attach-agent $bs $tcp

#set up receiver side
set sink [new Agent/TCPSink/Sack1]
$sink set ts_echo_rfc1323_ true
$ns attach-agent $br $sink

#logical connection
$ns connect $tcp $sink

#Setup a FTP over TCP connection
set ftp [new Application/FTP]
$ftp attach-agent $tcp
$ftp set type_ FTP

$ns at 0 "$tcp select_ca highspeed"

#Start FTP 
$ns at 0 "$ftp start"
$ns at 10 "$ftp stop"
$ns at 11 "exit 0"
$ns run

