
## pp. 8-9
set b 0.5

set x $b

puts "[expr 1/60]"

## pp. 9
puts "浮点运算: [expr 1.0/60.0]"

# 打开一个文件以写模式
set file1 [open test.write w]

# 写入数据
puts $file1 "1 1"
puts $file1 "2 $b"

# exec xgraph test.write &

# 循环
for { set i 0 } { $i < 5 } { incr i } {
  puts "循环 $i  "
}

proc test {} {
  set a 43
  set b 27
  set c [expr $a + $b]

  puts "调用函数 c = $c"
}

# 调用函数
test

proc blue { a } {
  global b ;#使用 b 为全局变量 b=0.5
  set c [expr $a + $b]
  puts "调用函数(含参数) c = $c"
  return $c
}

# 调用函数
blue 43
