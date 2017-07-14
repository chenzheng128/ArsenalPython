#
#              0                 4
#    200Mb/10ms \  100Mb/20ms   / 200Mb/10ms
#                2 ----------- 3
#    200Mb/20ms /               \ 200Mb/20ms
#              1                 5
#


#Create a simulator object
set ns [new Simulator]

#Define different colors for data flows(for NAM)
#$ns color 1 Blue
#$ns color 2 Red

set outInterval 0.5
set cwndInterval 0.1

set flow1_tcp cubic
set flow2_tcp cubic

set packetSize 1200

# Mb
set bandwidth1 200
set bandwidth2 100
# ms
set delay1 10
set delay2 20
set delay3 20

set StopTime 200

#Open the nam trace file
#set nf [open tcp.nam w]
#$ns namtrace-all $nf

#set tracefd [open tcp_all.tr w]
#$ns trace-all $tracefd

set rm [open readme w]
puts $rm "tcp fairless -- flow1:$flow1_tcp flow2:$flow2_tcp rtt1:$delay1 rtt2:$delay2 rtt3:$delay3"

########set the basic topo########

#record the output of sink
set f0 [open out_1_$flow1_tcp.tr w]
set f1 [open out_2_$flow2_tcp.tr w]

#record the cwnd 
set fw0 [open cwnd_1_$flow1_tcp.tr w]
set fw1 [open cwnd_2_$flow2_tcp.tr w]

#Create six nodes
set n0 [$ns node]
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]

#Create links between the nodes
# Syntax: duplex-link <node0> <node1> <bandwidth> <delay> <queue_type>
$ns duplex-link $n0 $n2 [set bandwidth1]Mb [set delay1]ms DropTail
$ns duplex-link $n1 $n2 [set bandwidth1]Mb [set delay2]ms DropTail
$ns duplex-link $n2 $n3 [set bandwidth2]Mb [set delay3]ms RED
$ns duplex-link $n3 $n4 [set bandwidth1]Mb [set delay1]ms DropTail
$ns duplex-link $n3 $n5 [set bandwidth1]Mb [set delay2]ms DropTail
set QueueLen [expr 0.2*$bandwidth2*1000000*$delay3*6/$packetSize/8/1000]
#set QueueLen 30
puts "QueueLen = $QueueLen"
$ns queue-limit $n2 $n3 $QueueLen
$ns queue-limit $n3 $n2 $QueueLen

# Create layout for nam
#$ns duplex-link-op $n0 $n2 orient right-down
#$ns duplex-link-op $n1 $n2 orient right-up
#$ns duplex-link-op $n2 $n3 orient right
#$ns duplex-link-op $n3 $n4 orient right-up
#$ns duplex-link-op $n3 $n5 orient right-down


#Monitor the queue for the link between node 2 and node 3 (for NAM)
#$ns duplex-link-op $n2 $n3 queuePos 0

#setup flow1 sender side    
set tcp1 [new Agent/TCP/Linux]
$tcp1 set class_ 1
$tcp1 set timestamps_ true
$tcp1 set window_ 20000
$tcp1 set packetSize_ $packetSize
$tcp1 set fid_ 1
$ns at 0 "$tcp1 select_ca $flow1_tcp"
$ns attach-agent $n0 $tcp1

#setup flow1 receiver side
set sink1 [new Agent/TCPSink/Sack1]
$sink1 set ts_echo_rfc1323_ true
$ns attach-agent $n4 $sink1

#setup flow2 sender side    
set tcp2 [new Agent/TCP/Linux]
$tcp2 set class_ 2
$tcp2 set timestamps_ true
$tcp2 set window_ 20000
$tcp2 set packetSize_ $packetSize
$tcp2 set fid_ 2
$ns at 0 "$tcp2 select_ca $flow2_tcp"
$ns attach-agent $n1 $tcp2

#set up flow2 receiver side
set sink2 [new Agent/TCPSink/Sack1]
$sink2 set ts_echo_rfc1323_ true
$ns attach-agent $n5 $sink2

#logical connection
$ns connect $tcp1 $sink1
$ns connect $tcp2 $sink2

#Setup a FTP over TCP connection
set ftp1 [new Application/FTP]
$ftp1 attach-agent $tcp1
$ftp1 set type_ FTP

set ftp2 [new Application/FTP]
$ftp2 attach-agent $tcp2
$ftp2 set type_ FTP


#========error model=========
#Creating Error Module
#set loss_module [new ErrorModel]
#$loss_module set rate_ 0.0005
#$loss_module unit pkt
#$loss_module ranvar [new RandomVariable/Uniform]
#$loss_module drop-target [new Agent/Null]

#Inserting Error Module
#$ns lossmodel $loss_module $n2 $n3


########define function to record########

#record the out of basic node
proc recordOut {} {
        global sink1 sink2 f0 f1 outInterval
        #Get an instance of the simulator
        set ns [Simulator instance]
        
        #How many bytes have been received by the traffic sinks?
        set bw0 [$sink1 set bytes_]
        set bw1 [$sink2 set bytes_]
        
        #Get the current time
        set now [$ns now]
        #Calculate the bandwidth (in MBit/s) and write it to the files
        puts $f0 "$now [expr $bw0/$outInterval*8/1000000]"
        puts $f1 "$now [expr $bw1/$outInterval*8/1000000]"
        
     
        #Reset the bytes_ values on the traffic sinks
        $sink1 set bytes_ 0
        $sink2 set bytes_ 0
        
        #Re-schedule the procedure
        $ns at [expr $now+$outInterval] "recordOut"
}

#record the cwnd of basic node
proc recordCwnd {} {

        global tcp1 tcp2 fw0 fw1 cwndInterval
        #Get an instance of the simulator
        set ns [Simulator instance]
        #Set the time after which the procedure should be called again    
        
        #Get the current time
        set now [$ns now]
        
        #Get the cwnd of tcp
        set cwnd0 [$tcp1 set cwnd_]
        set cwnd1 [$tcp2 set cwnd_]     
        
        puts $fw0 "$now $cwnd0"
        puts $fw1 "$now $cwnd1"
                
        #Re-schedule the procedure
        $ns at [expr $now+$cwndInterval] "recordCwnd"
}


########define function to finish########

proc finish {} {
  global ns nf f0 f1 fw0 fw1 ftw tracefd
  $ns flush-trace
#Close the trace file
  #close $nf
  #close $tracefd
#Close the output files
  close $f0
  close $f1
#Close the cwnd files
  close $fw0
  close $fw1
	
#Execute nam on the trace file
#  exec nam test_cubic.nam &
#Call xgraph to display the results
 exec xgraph  cwnd_1_cubic.tr cwnd_2_cubic.tr
 
#  exec xgraph test_cubic_flow1_cwnd(flow1_tcp).tr test_cubic_flow2_cwnd($flow2_tcp).tr  -geometry 800x400 &
  exit 0
}

########set the start/stop time########

#start the record function
$ns at 0 "recordOut"
$ns at 0 "recordCwnd"

#life of basic node
$ns at 0 "$ftp1 start"
$ns at 0 "$ftp2 start"
$ns at $StopTime "$ftp1 stop"
$ns at $StopTime "$ftp2 stop"

#Schedule the stop of the simulation
$ns at [expr 1+$StopTime] "finish"

#Start the simulation
$ns run
