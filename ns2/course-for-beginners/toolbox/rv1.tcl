## simple example demonstrating use of the RandomVariable class from tcl

set count 3
for {set i 0} {$i<3} {incr i} {

puts "===== i = $i "

set MyRng1 [new RNG]
$MyRng1 seed $i

set MyRng2 [new RNG]
$MyRng2 seed $i

set r1 [new RandomVariable/Pareto]
$r1 use-rng $MyRng1
$r1 set avg_ 10.0
$r1 set shape_ 1.2
puts stdout "Testing Pareto Distribution, avg = [$r1 set avg_] shape = [$r1 set shape_]"
$r1 test $count

set r2 [new RandomVariable/Pareto]
$r2 use-rng $MyRng2
$r2 set avg_ 10.0
$r2 set shape_ 1.2
puts stdout "Testing Pareto Distribution, avg = [$r2 set avg_] shape = [$r2 set shape_]"
$r2 test $count
}
