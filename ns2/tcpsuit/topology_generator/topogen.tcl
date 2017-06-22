#### READ ARGUMENTS #############################################################
set read_arg 0
set topology [lindex $argv $read_arg]; incr read_arg
set nw_size [lindex $argv $read_arg]; incr read_arg
set degree [lindex $argv $read_arg]; incr read_arg
set bw [lindex $argv $read_arg]; incr read_arg
set delay [lindex $argv $read_arg]; incr read_arg
set lflows [lindex $argv $read_arg]; incr read_arg
set sflows [lindex $argv $read_arg]; incr read_arg
set traffic [lindex $argv $read_arg]; incr read_arg

### OPEN FILES ###

set topology_f  [open model-topology w]
set flow_f  [open model-flow w]

### CREATE TOPOLOGY ###

proc printlink {i j bw del} {
    global topology_f
    set delay_str [format "%sms" $del]
    set bw_str    [format "%sMb" $bw]
    puts $topology_f "$i $j $bw_str $delay_str"
    #puts "LINK $i $j $bw_str $delay_str"
}

proc createlink {i j bw del} {
    global nw_size used
    set used([expr $i*$nw_size + $j]) $del
    set used([expr $j*$nw_size + $i]) $del
    printlink $i $j $bw $del
}

for {set i 0} {$i < [expr $nw_size * $nw_size] } {incr i 1} {
    set used($i) 0
}
for {set i 0} {$i < $nw_size } {incr i 1} {
    set group($i) 0
}

#Random network
proc grouping {src} {
    global groupnum group nw_size used
    set group($src) $groupnum
    for {set i 0} {$i < $nw_size } {incr i 1} {
	if {$used([expr $src*$nw_size + $i]) > 0 && $group($i) == 0} {
	    grouping $i
	}
    }
}

if {$topology == "random"} {
    if {[expr ($nw_size * ($nw_size-1))/2] < [expr $degree * $nw_size / 2]} {
	puts "Too much degree"
	exit
    }
    for {set i 0} {$i < [expr $nw_size * $degree / 2]} {incr i 1} {
	set src [expr int(rand() * $nw_size)]
	set dest [expr int(rand() * $nw_size)]
	while {$used([expr $src*$nw_size + $dest]) != 0 || $src >= $dest} {
	    set src [expr int(rand() * $nw_size)]
	    set dest [expr int(rand() * $nw_size)]
	}
	set rng1 [new RNG]
	$rng1 seed 0
	set del [new RandomVariable/Exponential]
	$del use-rng $rng1
	$del set avg_ $delay
	createlink $src $dest $bw [$del value]
    }
    #grouping
    set groupnum 0
    for {set i 0} {$i < $nw_size } {incr i 1} {
	if {$group($i) == 0} {
	    incr groupnum 1
	    grouping $i
	}
    }
}

#BA mobel
if {$topology == "BAmode"} {
    puts "BA model is not available yet, sorry"
    exit
}

#Tree network
if {$topology == "tree"} {
    for {set i 1} {$i < [expr $nw_size * $nw_size] } {incr i 1} {
	set used($i) 0
    }
    set parentnode 0
    set curnode 1
    set leftnode 1
    set rightnode [expr $degree-1]
    set level 1
    set count 1
    while {$curnode < $nw_size} {
	set rng1 [new RNG]
	$rng1 seed 0
	set del [new RandomVariable/Exponential]
	$del use-rng $rng1
	$del set avg_ $delay
	createlink $parentnode $curnode $bw [$del value]
	incr curnode
	incr count
	if {$curnode > $rightnode} {
	    set rightnode [expr ($rightnode-$leftnode+1)*($degree-1)+$curnode-1]
	    incr level 1
	    set parentnode $leftnode
	    set leftnode $curnode
	    set count 1
	    puts "Left$leftnode Right$rightnode Parent$parentnode Current$curnode"
	} elseif {$count == $degree} {
	    incr parentnode
	    set count 1
	}
    }
}

#Parking-lot network
if {$topology == "parking"} {
    for {set i 0} {$i < [expr $nw_size-1] } {incr i 1} {
	set rng1 [new RNG]
	$rng1 seed 0
	set del [new RandomVariable/Exponential]
	$del use-rng $rng1
	$del set avg_ $delay
	createlink $i [expr $i + 1] $bw [$del value]
    }
}


### CREATE CONNECTION ###

#count hop count
proc counthops {src dest} {
    global hopcnt nw_size used

    #puts "Search start $src=>$dest"
    set hopcnt 0
    for {set i 0} {$i < $nw_size} {incr i 1} {
	set visited($i) 0
    }
    set search "$src"
    while {[llength $search] > 0} {
	incr hopcnt 1
	set next ""
	#puts "($search) HOP$hopcnt"
	foreach j $search {
	    #puts "Searching $j"
	    for {set i 0} {$i < $nw_size} {incr i 1} {
		if {$used([expr $j*$nw_size + $i]) != 0 && $visited($i)==0} {
		    if {$i == $dest} {
			set search ""
			# puts "Found $i at HOP$hopcnt"
		    } else {
			# puts "VISITED $j=>$i HOP$hopcnt"
			set visited($i) 1
			lappend next $i
		    }
		}
	    }
	}
	#puts "Searching next $next"
	if {[llength $search] > 0} {
	    set search $next
	}
    }
}

set flows [expr $sflows + $lflows]
for {set i 0} {$i < $flows} {incr i 1} {
    # Determine source and destimation
    if {$traffic == "cs"} {
	set src [expr int(rand() * $nw_size) % 10 * 10]
	set dest [expr int(rand() * $nw_size) % 10 * 10 + int(rand()*9) + 1]
	while {$src == $dest || ($topology=="random" && $group($src)!=$group($dest))} {
	    set src [expr int(rand() * $nw_size) % 10 * 10]
	    set dest [expr int(rand() * $nw_size) % 10 * 10 + int(rand()*9) + 1]
	}
    } elseif {$traffic == "p2p"} {
	set src [expr int(rand() * $nw_size)]
	set dest [expr int(rand() * $nw_size)]
	while {$src == $dest || ($topology=="random" && $group($src)!=$group($dest))} {
	    set src [expr int(rand() * $nw_size)]
	    set dest [expr int(rand() * $nw_size)]
	}
    }
    counthops $src $dest

    # Set up links
    set rng1 [new RNG]
    $rng1 seed 0
    set del [new RandomVariable/Exponential]
    $del use-rng $rng1
    $del set avg_ $delay
    set srcnd [expr $nw_size+$i*2]
    set destnd [expr $nw_size+$i*2+1]
    printlink $srcnd $src $bw [$del value]
    printlink $destnd $dest $bw [$del value]
    if {$i < $lflows} {
	puts $flow_f "$srcnd $destnd [expr $hopcnt+2] 0"
	#puts "FLOW$i ($srcnd,$src) ($dest,$destnd) [expr $hopcnt+2] 0"
    } else {
	puts $flow_f "$srcnd $destnd [expr $hopcnt+2] 1"
	#puts "FLOW$i ($srcnd,$src) ($dest,$destnd) [expr $hopcnt+2] 1"
    }
}
