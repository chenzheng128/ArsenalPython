#!/bin/tclsh
#######
####### Basic data processings
#######
# Input files
#    data/(prot1)(prot2)(idx)thr
# Output files
#    data2/(prot1)(prot2)(idx).favg: Per-flow agerage throughput (sorted by flow ID)
#    data2/(prot1)(prot2)(idx).favgs: Per-flow agerage throughput (sorted by throughput)
#    data2/(prot1)(prot2)(idx).fvar: Per-flow agerage throughput variation (sorted by flow ID)
#    data2/(prot1)(prot2)(idx).fvars: Per-flow agerage throughput variation (sorted by throughput)
#    data2/(prot1)(prot2)(idx).lavg: Link utilization (sorted by link ID)
#    data2/(prot1)(prot2)(idx).lavgs: Link utilization (sorted by link utilization)
#    data2/(prot1)(prot2)(idx).lvar: Link utilization variation (sorted by link ID)
#    data2/(prot1)(prot2)(idx).lvars: Link utilization variation (sorted by link utilization)
#    data2/(prot1)(prot2)(idx).lutil: Time series of link utilization


####### Set of simulation senarios
set idxs "1 2 3 4 5 6 7 8 9 10"
#set idxs "1 2 7 8"

####### Set of ptorocols
set prots "renoreno compoundcompound compoundreno cubiccubic cubicreno htcphtcp htcpreno wwarwwar wwarreno arenoareno arenoreno"

###### Model parameters
set maxlink [lindex $argv 0]
set maxflow [lindex $argv 1]
set maxlflow [lindex $argv 2]

#########################################################################

foreach prot $prots {
foreach fidx $idxs {

puts "Processing $prot $fidx"

####### Link-set

set filename [format "model/link-%d" $fidx]
set link_f  [open $filename r]

gets $link_f line
while {$line != ""} {
    set llist [split $line " "]
    set flow [lindex $llist 0]
    set links($flow) [lrange $llist 1 end]
    #puts "$flow : $links($flow)"
    gets $link_f line
}
close $link_f


####### Average

set filename [format "data/%s%dthr" $prot $fidx]
set thr_f  [open $filename r]
set filename [format "data2/%s%d.lutil" $prot $fidx]
set util_f  [open $filename w]

for {set i 0} {$i < $maxlink} {incr i} {
    set util($i) 0
    set lsum($i) 0
}
for {set i 0} {$i < $maxflow} {incr i} {
    set fsum($i) 0
    set fnum($i) 0
}

set num 0
set curtime 0
gets $thr_f line
while {$line != ""} {
    scan $line "%f %d %f %f %f" time flow thr rtt cwnd
    if {$thr > 0.1} {
	set fsum($flow) [expr $fsum($flow)+$thr]
	incr fnum($flow)
    }
    foreach link $links($flow) {
	if {$link < $maxlink} {
	    set util($link) [expr $util($link)+$thr]
	}
    }
    scan $line "%f" time
    if {$curtime != $time || $line == ""} {
	if {$time > 200} {
	    for {set i 0} {$i < $maxlink} {incr i} {
		set lsum($i) [expr $lsum($i)+$util($i)]
	    }
	    incr num
	}
	for {set i 0} {$i < $maxlink} {incr i} {
	    #puts "$curtime $i $util($i)"
	    puts $util_f "$curtime $i $util($i)"
	    set util($i) 0
	}
	set curtime $time
    }
    gets $thr_f line
}

close $thr_f

set filename [format "data2/%s%d.favg" $prot $fidx]
set flow_f  [open $filename w]
set filename [format "data2/%s%d.lavg" $prot $fidx]
set link_f  [open $filename w]

for {set i 0} {$i < $maxflow} {incr i} {
    	set favg($i) [expr $fsum($i)/$fnum($i)]
    	puts $flow_f "$i $favg($i)"
}
for {set i 0} {$i < $maxlink} {incr i} {
    set lavg($i) [expr $lsum($i)/$num]
    puts $link_f "$i $lavg($i)"
}

close $flow_f
close $link_f


####### Variance

set filename [format "data/%s%dthr" $prot $fidx]
set thr_f  [open $filename r]

for {set i 0} {$i < $maxlink} {incr i} {
    set util($i) 0
    set lsum($i) 0
}
for {set i 0} {$i < $maxflow} {incr i} {
    set fsum($i) 0
    set fnum($i) 0
}

set num 0
set curtime 0
gets $thr_f line
while {$line != ""} {
    scan $line "%f %d %f %f %f" time flow thr rtt cwnd
    if {$thr > 0.1} {
	set fsum($flow) [expr $fsum($flow)+$thr]
	set fsum($flow) [expr $fsum($flow)+($favg($flow)-$thr)*($favg($flow)-$thr)]
	incr fnum($flow)
    }
    foreach link $links($flow) {
	if {$link < $maxlink} {
	    set util($link) [expr $util($link)+$thr]
	}
    }
    scan $line "%f" time
    if {$curtime != $time || $line == ""} {
	for {set i 0} {$i < $maxlink} {incr i} {
	    #puts "$i $util($i)"
	    if {$time > 200} {
		set lsum($i) [expr $lsum($i)+($lavg($i)-$util($i))*($lavg($i)-$util($i))]
	    }
	    incr num
	}
	set util($i) 0
	set curtime $time
    }
    gets $thr_f line
}

close $thr_f

set filename [format "data2/%s%d.fvar" $prot $fidx]
set flow_f  [open $filename w]
set filename [format "data2/%s%d.lvar" $prot $fidx]
set link_f  [open $filename w]

for {set i 0} {$i < $maxflow} {incr i} {
    set fvar($i) [expr $fsum($i)/$fnum($i)]
    puts $flow_f "$i $fvar($i)"
}
for {set i 0} {$i < $maxlink} {incr i} {
    set lvar($i) [expr $lsum($i)/$num]
    puts $link_f "$i $lvar($i)"
}

close $flow_f
close $link_f

####### Sorting (link)

set utils ""
for {set i 0} {$i < $maxlink} {incr i} {
    lappend utils "$i $lavg($i) $lvar($i)"
}
set utils [lsort -decreasing -real -index 1 $utils]

set filename [format "data2/%s%d.lavgs" $prot $fidx]
set avg_f  [open $filename w]
set filename [format "data2/%s%d.lvars" $prot $fidx]
set var_f  [open $filename w]

for {set i 0} {$i < $maxlink} {incr i} {
    puts $avg_f "$i [expr [lindex [lindex $utils $i] 1] /1000]"
    puts $var_f "$i [expr [lindex [lindex $utils $i] 2] /1000000]"
}
close $avg_f
close $var_f

####### Sorting (flow)

set utils ""
for {set i 0} {$i < $maxlflow} {incr i} {
    lappend utils "$i $favg($i) $fvar($i)"
}
set utils [lsort -decreasing -real -index 1 $utils]

set filename [format "data2/%s%d.favgs" $prot $fidx]
set avg_f  [open $filename w]
set filename [format "data2/%s%d.fvars" $prot $fidx]
set var_f  [open $filename w]

for {set i 0} {$i < $maxlflow} {incr i} {
    puts $avg_f "$i [lindex [lindex $utils $i] 1]"
    puts $var_f "$i [lindex [lindex $utils $i] 2]"
}
close $avg_f
close $var_f

}
}
