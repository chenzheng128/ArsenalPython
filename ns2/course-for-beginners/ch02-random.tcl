puts "随机变量例子 ch02, pp. 30 copy from rv1.tcl"

# 测试数量
set count 5
for {set i 0} {$i<2} {incr i} {
	set seed $i
	puts "===== i = $i "

	set MyRng1 [new RNG]
	$MyRng1 seed $seed

	set MyRng2 [new RNG]
	$MyRng2 seed $seed

	set r1 [new RandomVariable/Pareto]
	$r1 use-rng $MyRng1
	$r1 set avg_ 10.0
	$r1 set shape_ 1.2
	puts stdout "Testing Pareto Distribution, avg = [$r1 set avg_] shape = [$r1 set shape_]"

	# 生成测试数量的变量
	$r1 test $count

	set r2 [new RandomVariable/Pareto]
	$r2 use-rng $MyRng2
	$r2 set avg_ 10.0
	$r2 set shape_ 1.2
	puts stdout "Testing Pareto Distribution, avg = [$r2 set avg_] shape = [$r2 set shape_]"
	$r2 test $count

	set rstart [$r2 test 1]
	puts "随机变量: $rstart"
}


