#Create a simulator object
set ns [new Simulator]

#Define different colors for data flows (for NAM)
$ns color 1 Blue
$ns color 2 Red

#Open the NAM trace file
set nf [open out.nam w]
$ns namtrace-all $nf

#Define a 'finish' procedure
proc finish {} {
        global ns nf
        $ns flush-trace
        #Close the NAM trace file
        close $nf
        # Execute NAM on the trace file
        # exec nam out.nam &
        # exec xgraph.py ratefile0
        # exec xgraph ratefile0
        exit 0
}

# copy from ex/jobs-cn2002
set ratefile [open ratefile0 w]
proc linkDump {link binteg pinteg qmon interval} {
	global ns cbr ratefile
	set now_time [$ns now]
	$ns at [expr $now_time + $interval] "linkDump $link $binteg $pinteg $qmon $interval"
  
	set bandw [[$link link] set bandwidth_]
	set queue_bd [$binteg set sum_]
	set abd_queue [expr $queue_bd/[expr 1.*$interval]]
	set queue_pd [$pinteg set sum_]
	set apd_queue [expr $queue_pd/[expr 1.*$interval]]
	set utilz [expr 8*[$qmon set bdepartures_]/[expr 1.*$interval*$bandw]]
	if {[$qmon set parrivals_] != 0} {
		set drprt [expr [$qmon set pdrops_]/[expr 1.*[$qmon set parrivals_]]]
	} else {
		set drprt 0
	}
	if {$utilz != 0} {
		set a_delay [expr ($abd_queue*8*1000)/($utilz*$bandw)]
	} else {
		set a_delay 0.
	}
  if {$utilz > 0.9} {
    puts "debug: decrease udp rate"
    $cbr set rate_ 1mb
  }
  # 关闭一些暂时没用的输出
	#puts [format "%s \tLink %s: Util=%.3f\tDrRt=%.3f\tADel=%.1fms\tAQuP=%.0f\tAQuB=%.0f" $now_time "thisname" $utilz $drprt $a_delay $apd_queue $abd_queue]
	#puts -nonewline [format "%.3f\t" $utilz]
  puts $ratefile "[format "%s %.3f" $now_time $utilz]"
	$binteg reset
	$pinteg reset
	$qmon reset
}



#Create four nodes
set n0 [$ns node]
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
 

#Create links between the nodes
$ns duplex-link $n0 $n2 2Mb 10ms DropTail
$ns duplex-link $n1 $n2 2Mb 10ms DropTail
$ns duplex-link $n2 $n3 1.7Mb 20ms DropTail

#Set Queue Size of link (n2-n3) to 10
$ns queue-limit $n2 $n3 10

#Give node position (for NAM)
$ns duplex-link-op $n0 $n2 orient right-down
$ns duplex-link-op $n1 $n2 orient right-up
$ns duplex-link-op $n2 $n3 orient right

#Monitor the queue for link (n2-n3). (for NAM)
$ns duplex-link-op $n2 $n3 queuePos 0.5




#Setup a TCP connection
set tcp [new Agent/TCP]
$tcp set class_ 2
$ns attach-agent $n0 $tcp
set sink [new Agent/TCPSink]
$ns attach-agent $n3 $sink
$ns connect $tcp $sink
$tcp set fid_ 1

#Setup a FTP over TCP connection
set ftp [new Application/FTP]
$ftp attach-agent $tcp
$ftp set type_ FTP


#Setup a UDP connection
set udp [new Agent/UDP]
$ns attach-agent $n1 $udp
set null [new Agent/Null]
$ns attach-agent $n3 $null
$ns connect $udp $null
$udp set fid_ 2

#Setup a CBR over UDP connection
set cbr [new Application/Traffic/CBR]
$cbr attach-agent $udp
$cbr set type_ CBR
$cbr set packet_size_ 1000
$cbr set rate_ 2mb
$cbr set random_ false


# 进行带宽统计
set qmon_xy [$ns monitor-queue $n1 $n2 ""]
set bing_xy [$qmon_xy get-bytes-integrator]
set ping_xy [$qmon_xy get-pkts-integrator]
$ns at 0.5 "linkDump [$ns link $n1 $n2] $bing_xy $ping_xy $qmon_xy 0.5"  

#Schedule events for the CBR and FTP agents
$ns at 0.1 "$cbr start"
$ns at 1.0 "$ftp start"
$ns at 4.0 "$ftp stop"
$ns at 4.5 "$cbr stop"

#Detach tcp and sink agents (not really necessary)
$ns at 4.5 "$ns detach-agent $n0 $tcp ; $ns detach-agent $n3 $sink"

#Call the finish procedure after 5 seconds of simulation time
$ns at 5.0 "finish"

#Print CBR packet size and interval
puts "CBR packet size = [$cbr set packet_size_]"
puts "CBR interval = [$cbr set interval_]"

#Run the simulation
$ns run
