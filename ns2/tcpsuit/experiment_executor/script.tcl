#### INIT #############################################################

#Create a simulator object

#remove-all-packet-headers
#add-packet-header IP TCP Flags
set ns [new Simulator]

set thravg 1

#### GLOBAL DEFAULT PARAMETERS AND VALUES #############################

set buffer  1333
set psize   1500

set avginterval(0) 240
set avginterval(1) 1

set max_window     20000
set tcp_tick       0.001
set dt 0.1 ; # sampling interval (in seconds) used when logging cwnd etc

set stop_time    600.0 
#### READ COMMAND LINE ARGS ##########################################

set read_arg 0
set fidx       [lindex $argv $read_arg]; incr read_arg
set prot1      [lindex $argv $read_arg]; incr read_arg
set prot2      [lindex $argv $read_arg]; incr read_arg
set buffer     [lindex $argv $read_arg]; incr read_arg
set stop_time  [lindex $argv $read_arg]; incr read_arg
set stop_sim   [expr $stop_time + 0.1]

set filename [format "data/%s%s%dresp" $prot1 $prot2 $fidx]
set resp_f  [open $filename w]
set filename [format "data/%s%s%dthr" $prot1 $prot2 $fidx]
set thrp_f  [open $filename w]
set filename [format "data/%s%s%dlog" $prot1 $prot2 $fidx]
set log_f  [open $filename w]

#### FINISH #########################################################

#Define a 'finish' procedure
proc finish {} {
        global ns
    puts "NS -- Ending Simulation..."
        $ns flush-trace
        exit 0
}

### PRINT INDIVIDUAL CWND #################################################
proc printtcp {fp tcp sink lastbytes rate T} {
  global ns dt tcp_tick

  set now [$ns now]
  if { $T >=1.0} {
      set rate [expr ([$sink set bytes_]-$lastbytes)*8.0/(1000000*$T) ]
      set lastbytes [$sink set bytes_]
      set T 0.0
   }
  puts $fp "[format %.2f $now] [$tcp set cwnd_] [expr [$tcp  set srtt_]/8*$tcp_tick*1000]  [$sink set bytes_] $rate"
  $ns at [expr $now+$dt] "printtcp $fp $tcp $sink $lastbytes $rate [expr $T+$dt]"
}

proc print-tcpstats {tcp sink starttime label} {
  global ns dt
  set fp [open "data4/$label.out" w]
  set lastbytes 0
  $ns at $starttime "printtcp $fp $tcp $sink 0 0 0"
}

### PRINT INDIVIDUAL BUFFERS ############################################
proc printqueue {fp queue} {
  global ns dt
  set now [$ns now]
  puts $fp "[format %.2f $now] [$queue set size_] [$queue set pkts_] [$queue set parrivals_] [$queue set barrivals_] [$queue set pdepartures_] [$queue set bdepartures_] [$queue set pdrops_] [$queue set bdrops_]";
  $ns at [expr $now+$dt] "printqueue $fp $queue"
}

proc print-qstats {fname queue} {
  global ns
  set fp [open "data4/$fname.out" w]
  $ns at 0.0 "printqueue $fp $queue"
}

#### CREATE NODES and LINKS ############################################################

set filename [format "model/topology-%d" $fidx]
set topo_f  [open $filename r]

gets $topo_f line
while {$line != ""} {
    scan $line "%d %d %s %s" n1 n2 bw delay
    if {[info exist node($n1)] != 1} {
	set node($n1) [$ns node]
	#puts "Create node $n1"
    }
    if {[info exist node($n2)] != 1} {
	set node($n2) [$ns node]
	#puts "Create node $n2"
    }

    $ns duplex-link $node($n1) $node($n2) $bw $delay DropTail
    $ns queue-limit $node($n1) $node($n2) $buffer
    $ns queue-limit $node($n2) $node($n1) $buffer
    # puts "MONITOR $n1-$n2 $bw $delay $buffer"
    
    gets $topo_f line
}
set qmon01 [$ns monitor-queue $node(0) $node(1) ""]
set qmon10 [$ns monitor-queue $node(1) $node(0) ""]
set qmon12 [$ns monitor-queue $node(1) $node(2) ""]
set qmon21 [$ns monitor-queue $node(2) $node(1) ""]
set qmon23 [$ns monitor-queue $node(2) $node(3) ""]
set qmon32 [$ns monitor-queue $node(3) $node(2) ""]
set qmon34 [$ns monitor-queue $node(3) $node(4) ""]
set qmon43 [$ns monitor-queue $node(4) $node(3) ""]
print-qstats queues_$fidx\_01 [set qmon01] ;
print-qstats queues_$fidx\_10 [set qmon10] ;
print-qstats queues_$fidx\_12 [set qmon12] ;
print-qstats queues_$fidx\_21 [set qmon21] ;
print-qstats queues_$fidx\_23 [set qmon23] ;
print-qstats queues_$fidx\_32 [set qmon32] ;
print-qstats queues_$fidx\_34 [set qmon34] ;
print-qstats queues_$fidx\_43 [set qmon43] ;
close $topo_f

#### CREATE CONNECTION #################################################

# Create TCP Connection
proc createTCPConn {prot a src dest typ} {
    global ns node agent ftp psize stop_time nextstart rng sink fidx
    global max_window tcp_tick idx group
    global cwnd_f ssth_f rtt_f thr_f
    global avginterval type active

    if { ($prot == "RENO") } {
	set agent($a) [new Agent/TCP/Sack1]
	$agent($a) set windowOption_ 1
    } else {
	set agent($a) [new Agent/TCP/Linux]
	$ns at 0 "$agent($a) select_ca $prot"
    }
    set idx($agent($a)) $a

    $agent($a) set class_ $a      # flow ID
    $agent($a) set flowid_ $a
    $agent($a) set timestamps_ true
    $agent($a) set parcial_ack_ true
    $agent($a) set window_  $max_window
    $agent($a) set maxcwnd_ $max_window
    $agent($a) set packetSize_ [expr $psize - 40]
    $agent($a) set tcpTick_ $tcp_tick
    #$agent($a) set overhead_ 0.0001

    $ns attach-agent $node($src) $agent($a)

    # TCP Sink
    set sink($a) [new Agent/TCPSink/Sack1]
    $ns attach-agent $node($dest) $sink($a)

    # connect
    $ns connect $agent($a) $sink($a)
    print-tcpstats [set agent($a)] [set sink($a)] 0 tcp_cwnd_$fidx\_$a ;

    # FTP
    set ftp($a) [new Application/FTP]
    $ftp($a) attach-agent $agent($a)

    # start
    set type($a) $typ
    set active($a) 0
    set rng($a) [new RNG]
    $rng($a) seed [expr (int(exp($a % 10)+5) % 1000) + (int(exp($a/10)+5) % 1000) + $a*1000]
    set interval [new RandomVariable/Exponential]
    $interval use-rng $rng($a)
    $interval set avg_ $avginterval($typ)
    set nextstart($a) [expr [$interval value] / 4]
    #puts "$a [expr int($nextstart($a))]"
    $ns at $nextstart($a) "tcpbackground $a"
    $agent($a) proc done {} {
	tcpbackground_done $self
    }
}
# end create conn


proc tcpbackground {a} {
    global ns ftp agent sink psize nextstart stime burstsize rest rng max_window
    global avgsize avginterval active type log_f thravg privseq

    if {$type($a) == 0} {
	set bsize 4700000000
	puts $log_f "[$ns now] BURST $a $bsize"
	flush $log_f
    } else {
	set size [new RandomVariable/ParetoII]
	$size use-rng $rng($a)
	$size set avg_ 100000
	$size set shape_ 1.2
	set bsize [expr [$size value] + $psize]
    }
    set stime($a) [$ns now]
    set burstsize($a) $bsize
    set rest($a) $bsize
    set privseq($a) [$agent($a) set t_seqno_ ]
    set active($a) 1

    #$agent($a) set ssthresh_ $max_window
    #$agent($a) set cwnd_ 1
    $agent($a) reset
    $sink($a) reset
    $ftp($a) producemore [expr $bsize/$psize]

    set typ $type($a)
    set interval [new RandomVariable/Exponential]
    $interval use-rng $rng($a)
    $interval set avg_ $avginterval($typ)
    set nextstart($a) [expr $nextstart($a) + [$interval value]]
}

proc tcpbackground_done {obj} {
    global tcp_tick agent ns stime idx burstsize nextstart resp_f active

    set a $idx($obj)

    set active($a) 0

    set now [$ns now]
    set delay [expr $now-$stime($a)]
    set t_rtt [$agent($a) set rtt_ ]
    set rtt [ expr $t_rtt * $tcp_tick ]

#puts "FINISH $a NOW$now"
    #puts "[format "%.4f %d start %.4f next %.4f size %.0f del %.4f rtt %.4f" $now $a $stime($a) $nextstart($a) $burstsize($a) $delay $rtt]"
    puts $resp_f "[format "%.4f %d %.0f %.4f %.4f" $now $a $burstsize($a) $delay $rtt]"

    if {$now > $nextstart($a)} {
	tcpbackground $a
    } else {
	$ns at $nextstart($a) "tcpbackground $a"
    }
}

proc tcpbackground_done_a {a} {
    global tcp_tick agent ns stime idx burstsize nextstart resp_f active

    set active($a) 0

    set now [$ns now]
    set delay [expr $now-$stime($a)]
    set t_rtt [$agent($a) set rtt_ ]
    set rtt [ expr $t_rtt * $tcp_tick ]

#puts "FINISH $a NOW$now"
    #puts "[format "%.4f %d start %.4f next %.4f size %.0f del %.4f rtt %.4f" $now $a $stime($a) $nextstart($a) $burstsize($a) $delay $rtt]"
    puts $resp_f "[format "%.4f %d %.0f %.4f %.4f" $now $a $burstsize($a) $delay $rtt]"

    if {$now > $nextstart($a)} {
	tcpbackground $a
    } else {
	$ns at $nextstart($a) "tcpbackground $a"
    }
}

#### CONNECTIONS AND AGENTS ##################################################

set filename [format "model/flow-%d" $fidx]
set flow_f  [open $filename r]

set na 0
gets $flow_f line
while {$line != ""} {
    scan $line "%d %d %d %d" src dest hop typ

    if {$na % 2 == 0} {
	createTCPConn "$prot1" $na $src $dest $typ
	#puts "- Created TCP agent $na, node $src-$dest Hops$hop, $prot1"
    } else {
	createTCPConn "$prot2" $na $src $dest $typ
	#puts "- Created TCP agent $na, node $src-$dest Hops$hop, $prot2"
    }
    incr na
    gets $flow_f line
}


#### RECORD BWE ########################################

# Procedure to record the bwe for the TCP Westwood agents
set cnt 0
for {set b 0} {$b < $na} {incr b 1} {
    for {set a 0} {$a < $thravg} {incr a 1} {
	set index [expr $b*$thravg+$a]
	set p_seq($index) 0
    }
}

proc record_basics {} {
    global ns agent agent_type ftp sink
    global cwnd_f rtt_f thr_f qmon na thrp_f log_f
    global agent_start agent_end
    global tcp_tick thravg active burstsize rest privseq
    global cnt p_seq ;# For Throughput Calculation
    global psize ;# packet size
    set time 1
    set now [$ns now]

    set na [array size agent]
    for {set a 0} {$a < $na} {incr a 1} {

	set cwnd [$agent($a) set cwnd_ ]
	set no_txed [$agent($a) set t_seqno_ ]
	#set no_txed [$agent($a) set ack_ ]
	set t_rtt [$agent($a) set rtt_ ]
	set rtt [ expr $t_rtt * $tcp_tick ]
	#puts $cwnd_f($a) "$now $cwnd"
	#puts $rtt_f($a) "$now $rtt"

	# Throughput Calculation
	set seq [expr $no_txed]
	if {$seq < 0} {set seq 0}
	set index [expr $a*$thravg+$cnt]
	set thr [expr ($seq - $p_seq($index))/1000000.0 *8 *$psize/$time/$thravg]
	if {$thr < 0} {set thr 0}
	#puts "$index:  $seq $p_seq($index) $thr"
	set p_seq($index) $seq
	puts $thrp_f "[format "%.1f %d %.4f %.4f %.0f" $now $a $thr $rtt $cwnd]"

	#CHECKPOINT for LONGLIVED FLOWS
	if {$active($a) > 0 && $thr==0 && $now > 1} {
	    incr active($a)
	}
	if {$active($a) == 4 && $thr==0 && $now > 1} {
	    #puts "< $no_txed $privseq($a)"
	    set sent [expr ($no_txed-$privseq($a)) * $psize]
	    set rest($a) [expr $rest($a) - $sent]
	    $agent($a) reset
	    $sink($a) reset
	    set ssth [$agent($a) set ssthresh_]
	    set cwnd [$agent($a) set cwnd_]
	    set no_txed [$agent($a) set t_seqno_ ]
	    if {$rest($a) > $psize} {
		set privseq($a) $no_txed
		$ftp($a) producemore [expr $rest($a)/$psize]
		set active($a) 1
	    } else {
		tcpbackground_done_a $a
	    }
	    puts "> $no_txed $privseq($a)"
	    puts "[$ns now] Restart $a CWND $cwnd SSTH $ssth SIZE $burstsize($a) SENT $sent REST $rest($a)"
	    puts $log_f "[$ns now] Restart $a CWND $cwnd SSTH $ssth SIZE $burstsize($a) SENT $sent REST $rest($a)"
	    flush $log_f
	}
    }
    incr cnt 1
    if { ($cnt == $thravg) } { set cnt 0; puts $now } 
    #if { ($cnt == $thravg) } { set cnt 0; } 

    $ns at [expr $now+$time] "record_basics"
}
#First call to the record_bwe procedure
$ns at 1.0 "record_basics"


#### START / STOP SIMULATION ###########################

#Call the finish procedure
$ns at $stop_sim "finish"
#Run the simulation
puts "NS -- Starting Simulation..."
$ns run
