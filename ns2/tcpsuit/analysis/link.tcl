#!/bin/tclsh
#######
####### Compute link utilization
#######
# Input files
#    data2/(prot1)(prot2).*
# Output files
#    data3/(prot1)(prot2).lavgs: Link utilization
#    data3/(prot1)(prot2).lvar: Link utilization variation


####### Set of simulation senarios
set idxs "1 2 3 4 5 6 7 8 9 10"
#set idxs "1 2 7 8"

####### Set of ptorocols
set prots "renoreno compoundcompound compoundreno cubiccubic cubicreno htcphtcp htcpreno wwarwwar wwarreno arenoareno arenoreno"

####### Model parameters
#set maxlink [lindex $argv 0]
set maxlink 6

#########################################################################

foreach file $prots {

    set tot 0
    set cnt 0
    for {set i 0} {$i < $maxlink} {incr i} {
	set sum($i) 0
	set num($i) 0
    }

    foreach idx $idxs {
	set link_f  [open data2/$file$idx.lavg r]
	gets $link_f line
	while {$line != ""} {
	    scan $line "%d %f" link val
	    if {$link < $maxlink} {
		set sum($link) [expr $sum($link)+$val]
		incr num($link)
	    }
	    gets $link_f line
	}
	close $link_f
    }

    set out_f  [open data3/$file.lavgs w]
    set max 0
    for {set i 0} {$i < $maxlink} {incr i} {
	set avg [expr $sum($i)/$num($i)]
	puts $out_f "$i $avg"
	set tot [expr $tot + $avg]
	if {$avg > $max} {set max $avg}
	incr cnt
	set sum($i) 0
	set num($i) 0
    }
    close $out_f
    puts "$file [expr $tot/$cnt]Mbps (Avg.) $max Mbps (Max)"

    foreach idx $idxs {
	set link_f  [open data2/$file$idx.lvar r]
	gets $link_f line
	while {$line != ""} {
	    scan $line "%d %f" link val
	    if {$link < $maxlink} {
		set sum($link) [expr $sum($link)+$val]
		incr num($link)
	    }
	    gets $link_f line
	}
	close $link_f
    }

    set out_f [open data3/$file.lvars w]
    for {set i 0} {$i < $maxlink} {incr i} {
	puts $out_f "$i [expr $sum($i)/$num($i)]"
	set sum($i) 0
	set num($i) 0
    }
    close $out_f
}
