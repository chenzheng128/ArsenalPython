# comes from ch02  and toolbox/ex2.tcl
# initailization and termination

puts "新建模拟器对象 ns New a Simulator ..."
set ns [new Simulator]

puts "设定输出 trace 文件 ch02_out.tr ..."
set tracefile1 [ open ch02_out.tr w]
$ns trace-all $tracefile1

puts "设定输出 nam 文件 ch02_out.nam ..."
set namfile [open ch02_out.nam w]
$ns namtrace-all $namfile

# 定义finish函数, 关闭 trace 与 nam 文件
proc finish {} {
  global ns tracefile1 namfile
  $ns flush-trace
  close $tracefile1
  close $namfile
  exec nam ch02_out.nam &
  exit 0
}


set n0 [$ns node]
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]

puts "创建 duplex-link; 包含两个  simplex-link, 参考 pp.17 Fig 2.1 simplex-link "
puts "创建哑铃拓扑, 参考 pp.18 Fig2.2 拓扑图"
#Create links between the nodes
$ns duplex-link $n0 $n2 0.3Mb 10ms DropTail
$ns duplex-link $n1 $n2 0.3Mb 10ms DropTail
$ns simplex-link $n2 $n3 0.3Mb 10ms DropTail
$ns simplex-link $n3 $n2 0.3Mb 10ms DropTail
$ns duplex-link $n3 $n4 0.5Mb 10ms DropTail
$ns duplex-link $n3 $n5 0.5Mb 10ms DropTail

puts "设定可视化布局 pp.25"
#Give node position (for NAM)
$ns duplex-link-op  $n0 $n2 orient right-down
$ns duplex-link-op  $n1 $n2 orient right-up
$ns simplex-link-op $n2 $n3 orient right
$ns simplex-link-op $n3 $n2 orient left
$ns duplex-link-op  $n3 $n4 orient right-up
$ns duplex-link-op  $n3 $n5 orient right-down

# 设定链路颜色为绿色 geen link
$ns duplex-link-op  $n0 $n2 color green
#color flow
$ns color 1 Blue
$ns color 2 Red

# TODO: label 命令的格式不对
#$n3 lable "active"

set qsize 20
puts "修改队列大小为 $qsize"
$ns queue-limit $n2 $n3 $qsize ;# ns-default.tcl 设置默认值50;  Queue set limit_ 50

puts "建立 tcp agent 与ftp连接"
set tcp [new Agent/TCP]
set sink [new Agent/TCPSink]
$ns attach-agent $n0 $tcp
$ns attach-agent $n4 $sink
$ns connect $tcp $sink
$tcp set fid_ 1
$tcp set packetSize_ 552

set ftp [new Application/FTP]
$ftp attach-agent $tcp

puts "建立 udp agent 与cbr连接"
set udp [new Agent/UDP]
$ns attach-agent $n1 $udp
set null [new Agent/Null]
$ns attach-agent $n5 $null
$ns connect $udp $null
$udp set fid_ 2

set cbr [new Application/Traffic/CBR]
$cbr attach-agent $udp
$cbr set packetSize_ 1000
$cbr set rate_ 0.01mb
$cbr set random_ 1
$cbr set interval_ 0.005

set source [new Application/Traffic/Exponential]
set source [new Application/Traffic/Pareto]


$ns at 0.1 "$cbr start"
$ns at 0.5 "$ftp start"
$ns at 120 "$ftp stop"
$ns at 124.5 "$cbr stop"
# puts "模拟结束时, 调用 finsh() 函数 ..."
$ns at 125.0 "finish" ;#

$ns run
