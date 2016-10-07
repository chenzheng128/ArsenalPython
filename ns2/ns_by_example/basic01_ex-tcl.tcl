# 基本运算 
# Writing a procedure called "test"
proc test {} {
    set a 43
    set b 27
    set c [expr $a + $b]
    set d [expr [expr $a - $b] * $c]
    for {set k 0} {$k < 10} {incr k} {
	if {$k < 5} {
	    puts "k < 5, pow = [expr pow($d, $k)]"
	} else {
	    puts "k >= 5, mod = [expr $d % $k]"
	}
    }
}

# Calling the "test" procedure created above
test
