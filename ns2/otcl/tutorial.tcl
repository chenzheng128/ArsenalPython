puts "定义类"
Class Bagel
# Bagel

# 这种生成实例和 new 的区别?
puts "生成实例"
Bagel abagel
Bagel abagelA
Bagel abagelB
puts "new成实例"
set aba [new Bagel]
# abagel

puts "查看实例class"
puts [abagel info class]
puts " new 出来的 set 实例必须要用 $ 获取, $ 相当于 set x 的简写; 下面这两句是等效的"
puts [$aba info class] ;
puts [[set aba] info class] ;
# Bagel

puts "\n设置 instance 变量"
abagel set toasted 0
# 0

puts "查看 instance 所属变量 vars"
abagel info vars
# toasted
puts "查看 instance 所属变量值;  otcl 没有 get, set 不带参数就可以了"
abagel set toasted

puts "定义init初始化 函数 "
Bagel instproc init {args} {
  $self set toasted 11 
  eval $self next $args ;#这句话什么意思? 
}
puts "定义 toast {} 函数 "
Bagel instproc toast {} {
  $self instvar toasted
  incr toasted
  if {$toasted>1} then {
    error "something's burning!"
  }
  return {}
}

puts "\n查看class 的 实例信息  info instances"
puts [Bagel info instances]
# abagel
puts "查看class 的 函数信息  info instprocs"
puts [Bagel info instprocs]
# abagel

puts "再创建实例时, 变量已经被初始化了 toasted=11"
Bagel bagel2
# bagel2
bagel2 info vars
# toasted
puts [bagel2 set toasted]
#0

abagel toast
# 这句命令执行会发生错误   error "something's burning!"
# abagel toast ;

puts "查看类的继承关系与信息 info superclass|heritage"
Class SpreadableBagel -superclass Bagel
# SpreadableBagel
puts "SpreadableBagel info superclass: [SpreadableBagel info superclass]"
# Bagel
puts "SpreadableBagel info heritage: [SpreadableBagel info heritage]"
# Bagel Object



