
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
set UTILZ_THREDHOD [expr [gets $conf] / 1000.0]
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

puts "EndTime = $EndTime"

set SideBWNum [string map {Mb ""} $SideBW]

#Create a simulator object
set ns [new Simulator]

proc monitor {interval last_ack} {
    global FlowNumber tcp ns
    set nowtime [$ns now]

    for {set i 0} {$i < $FlowNumber} {incr i 1} {
        set win [open result$i a]
        
        #增加带宽统计功能
        #How many bytes have been received by the traffic sinks?
        #puts [$tcp($i) info vars]
        #puts [$tcp($i) set cwnd_]
        #puts [$tcp($i) set ack_]
        # 这里的 3代码, 不如 awk 一行代码来的清楚
        # cat result0 | awk 'BEGIN{old=0}{print $1, ($3-old)*1448*8*2}{old=$3}' > rate0
        set this_ack [$tcp($i) set ack_]
        set bw0 [expr $this_ack - $last_ack]
        if {$i == 3} {
          # TODO
          # 某些流的 this_ack 和 last_ack 没有正确传递, 导致数据产生负值 bw 计算失误, 取消在 tcl 中计算多流带宽, 仅记录 ack
          # puts "this_ack-last_ack $this_ack $last_ack $bw0"
        }
        #Calculate the bandwidth (in MBit/s) and write it to the files 
        # / $interval 就相当于 * 2, 1448 待解释
        set rate_interval [expr $bw0 / $interval * 1448 * 8 / 1000000]
        #Reset the bytes_ values on the traffic sinks
        
        # result0 格式为 $nowtime $cwnd $ack 取消在 tcl 中计算多流带宽, 仅记录 ack
      	puts $win "[format "%.1f %d %d" $nowtime [$tcp($i) set cwnd_] $this_ack]"
      	close $win
    }
    $ns after $interval "monitor $interval $this_ack"
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

# debug: 增加 nam 输出, 便于查看拓扑
# 正式运行时关闭, 因为生成 tcp.nam 文件很大
# $ns namtrace-all [open tcp.nam w]

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

# 计算中位数  Source: https://wiki.tcl.tk/750
proc median {l} {
  if {[set len [llength $l]] % 2} then {
    return [lindex [lsort -real $l] [expr {($len - 1) / 2}]]
  } else {
    return [expr {([lindex [set sl [lsort -real $l]] [expr {($len / 2) - 1}]] \
                   + [lindex $sl [expr {$len / 2}]]) / 2.0}]
  }
}

$ns queue-limit $bs $br $MainBuffer
set MIN_Q 1
set MAX_Q $MainBuffer
set MON_RATES [list]
proc monitor_rates {utilz} { ;# 监测带宽并保存在数组 list 中
  global MON_RATES
  if { [llength $MON_RATES] > 4} {
    set MON_RATES [lreplace $MON_RATES 0 0] ;# 已有足够元素, 移除第一个元素
  }
  lappend MON_RATES $utilz ;# 追加到最后一个元素中
  # puts "$.f \n"
}
proc bufferSweep {link qmon interval} {
  global ns bs br FlowNumber MIN_Q MAX_Q MON_RATES UTILZ_THREDHOD
  set now_time [$ns now]
  $ns at [expr $now_time + $interval] "bufferSweep $link $qmon $interval"  
  
  set bandw [[$link link] set bandwidth_]
  set utilz [expr 8*[$qmon set bdepartures_]/[expr 1.*$interval*$bandw]]
  
  if { [expr {abs($MAX_Q-$MIN_Q)} >=2] } {
    
        # 二分法进行搜索, 效果欠佳
        set mid [ expr ($MIN_Q + $MAX_Q) / 2]
        
        # 修改为每次缩减 1/6 步长
        set step [ expr round(ceil(($MAX_Q - $MIN_Q) / 6))]
        # step 太小时, 修订一下, 加快收敛速度
        if {$step <= 3} { incr step }
        set mid  [ expr $MAX_Q - $step]
        set mid2 [ expr $MIN_Q + $step]
        # 二分法进行搜索, 效果欠佳
        
        
        puts -nonewline [format "%.2f Trying q=%d  %d-%d step=%d " $now_time $mid $MIN_Q $MAX_Q  $step]
        
        # 调整队列大小会导致带宽进行抖动, 需要寻找更好的评估办法
        $ns queue-limit $bs $br $mid
        
        # 获取带宽中位数
        set fraction [median $MON_RATES]
        #puts "debug: [format MON_RATES: %.4f ] $MON_RATES" # 调试打印监控带宽值
        if { $fraction > $UTILZ_THREDHOD } {
          puts "[format "当前带宽为 %.4f > %.4f --" $fraction $UTILZ_THREDHOD ] "
          set MAX_Q $mid
        } else {
          puts "[format "当前带宽为 %.4f < %.4f ++" $fraction $UTILZ_THREDHOD ] "
          set MIN_Q [expr $mid2 + 1]
    }
  } else {
    puts [open result.txt w] "$FlowNumber $MAX_Q [expr $MAX_Q*1500]"
    puts "结束搜索, 最终队列搜索结果: $FlowNumber 流 pkts=$MAX_Q [expr $MAX_Q*1500]"
    $ns at [expr $now_time + $interval - 1] "finish"  
  }
}

set ratefile [open rate0 w]
set utilfile [open util0 w]
set queuefile [open queue0 w]
proc linkDump {link qmon interval} {
	global ns ratefile utilfile queuefile
	set now_time [$ns now]
	$ns at [expr $now_time + $interval] "linkDump $link $qmon $interval"  
  
  # 获取 queue_monitor 中的相关变量
  $qmon instvar size_ pkts_ barrivals_ bdepartures_ parrivals_ pdepartures_ bdrops_ pdrops_ 
  
	set bandw [[$link link] set bandwidth_]
  set rate0 [expr 8*[$qmon set bdepartures_]]
  set utilz [expr 8*[$qmon set bdepartures_]/[expr 1.*$interval*$bandw]]
  
  # 记录当前带宽
  monitor_rates $utilz
  
  # 计算 banw 的方法
  # set bandw [expr $rate0 * 2 / 1000 / 100] ;# TODO 为什么 * 2 / 100 待分析. 
  
  # 关闭一些暂时没用的输出
	#puts [format "%s \tLink %s: Util=%.3f\tDrRt=%.3f\tADel=%.1fms\tAQuP=%.0f\tAQuB=%.0f" $now_time "thisname" $utilz $drprt $a_delay $apd_queue $abd_queue]
	#puts -nonewline [format "%.3f\t" $utilz]
  
  # 输出速率占用
  puts $ratefile "[format "%s %.3f" $now_time $rate0]"
  # 输出速率占用百分比
  puts $utilfile "[format "%s %.3f" $now_time $utilz]"
  # 输出队列占用
  puts $queuefile "[format "%s %d" $now_time $size_]"

	$qmon reset
}

# 对链路带宽进行统计, 将这里的两个节点 bs br 指定为要监测的节点, 即可进行链路带宽监测
set qmon_xy [$ns monitor-queue $bs $br ""]  ;
$ns at 0.5 "linkDump [$ns link $bs $br] $qmon_xy 0.5" 
$ns at 10 "bufferSweep [$ns link $bs $br] $qmon_xy 10" ;# 支持用更低的频率检查带宽



#call the monitor at the end
$ns at 0 "monitor 0.5 0"

#Call the finish procedure after 1 seconds of simulation time
$ns at $EndTime+2 "finish"

puts "start"
#Run the simulation
$ns run
