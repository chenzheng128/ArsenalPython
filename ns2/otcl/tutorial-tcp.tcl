
set ns [new Simulator]


# 这种生成实例和 new 的区别?
puts "生成实例"
Agent/TCP ttt
puts "new成实例"
set tcp [new Agent/TCP]
# $tcp

puts "查看实例class"
puts [ttt info class]
puts " new 出来的 set 实例必须要用 $ 获取, $ 相当于 set x 的简写; 下面这两句是等效的"
puts [$tcp info class] ;
puts [[set tcp] info class] ;
# Bagel

puts "\n设置 instance 变量"
$tcp set toasted 0
# 0

puts "查看 instance 所属变量 vars"
$tcp info vars
# toasted
puts "查看 instance 所属变量值;  otcl 没有 get, set 不带参数就可以了"
# $tcp set toasted

puts "定义init初始化 函数 "

puts "定义 toast {} 函数 "


puts "\n查看class 的 实例信息  info instances"
puts [Agent/TCP info instances]
# $tcp
puts "查看class 的 函数信息  info instprocs"
puts [Agent/TCP info instprocs]
# $tcp

puts "再创建实例时, 变量已经被初始化了 toasted=11"
set reno [new Agent/TCP]
# $reno
$reno info vars
# toasted
# puts [$reno set toasted]
#0

puts "查看类的继承关系与信息 info superclass|heritage"
# Class SpreadableBagel -superclass Bagel
# SpreadableBagel

puts "Agent/TCP/Reno info superclass: [Agent/TCP/Reno info superclass]"
# Bagel
puts "Agent/TCP/Reno info heritage: [Agent/TCP/Reno info heritage]"
# Bagel Object



