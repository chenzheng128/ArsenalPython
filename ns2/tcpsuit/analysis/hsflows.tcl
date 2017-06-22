#!/bin/tclsh
#######
####### Characteristics of high-speed flows
#######       Throughput v.s. RTT, hop count, bottleneck link utilization
#######
# Input files
#    data2/(prot1)(prot1).*
# Output files
#    data3/(prot1)(prot1).favgr
#       (throughput of prot1 in [prot1prot1]) sorted by RTT
#    data3/(prot1)(prot1).favgh
#       (throughput of prot1 in [prot1prot1]) sorted by hop count
#    data3/(prot1)(prot1).favgb
#       (throughput of prot1 in [prot1prot1]) sorted by bottleneck link utilization



####### Set of simulation senarios
set idxs "1 2 3 4 5 6 7 8 9 10"
#set idxs "1 2 7 8"

####### Set of ptorocols
set prots "compoundcompound cubiccubic htcphtcp wwarwwar arenoareno renoreno"

####### Model parameters
set maxlink [lindex $argv 0]
set maxflow [lindex $argv 1]
set maxlflow [lindex $argv 2]

#########################################################################
proc readindexeddata {fname} {
    set file  [open $fname r]
    gets $file line
    while {$line != ""} {
	set idx [lindex $line 0]
	set val [lrange $line 1 end]
	set data($idx) $val
	gets $file line
    }
    close $file
    return [array get data]
}

proc readdata {fname} {
    set file  [open $fname r]
    set idx 0
    gets $file line
    while {$line != ""} {
	set data($idx) $line
	incr idx
	gets $file line
    }
    close $file
    return [array get data]
}

proc writeplaindata {fname data} {
    set file  [open $fname w]
    foreach element $data {
	puts $file $element
    }
    close $file
}

proc indexavg {data} {
    set result ""
    foreach element $data {
	set idx [lindex $element 0]
	set val [lindex $element 1]
	if {[info exist sum($idx)] == 0} {
	    set sum($idx) $val
	    set num($idx) 1
	} else {
	    set sum($idx) [expr $sum($idx) + $val]
	    incr num($idx)
	}
    }
    foreach idx [array name sum] {
	lappend result "$idx [expr $sum($idx)/$num($idx)]"
    }
    return $result
}

proc rangeavg {data range step} {
    set result ""
    set data [lsort -decreasing -real -index 0 $data]
    set idx 0
    foreach element $data {
	set rtt($idx) [lindex $element 0]
	set thr($idx) [lindex $element 1]
	incr idx
    }
    for {set i 0} {$i<$idx} {incr i} {
	set start [expr $i-$range]
	if {$start < 0} {set start 0}
	set end [expr $i+$range+1]
	if {$end > $idx} {set end $idx}
	set sum 0
	set num 0
	for {set j $start} {$j < $end} {incr j} {
	    set sum [expr $sum + $thr($j)]
	    set num [expr $num + $rtt($j)]
	}
        if {$i%$step==0 || $i==[expr $idx-1]} {
            lappend result "$rtt($i) [expr $sum/($end-$start+1)]"
	}
    }
    return $result
}

proc rangeavg2 {data range step} {
    set result ""
    set data [lsort -decreasing -real -index 0 $data]
    set idx 0
    foreach element $data {
	set rtt($idx) [lindex $element 0]
	set thr($idx) [lindex $element 1]
	incr idx
    }
    set priv 0
    set sum 0
    set num 0
    for {set i 0} {$i<$idx} {incr i $step} {
	set cur [expr int($rtt($i)/$range)]
	if {$cur != $priv && $num > 0} {
	    lappend result "[expr ($priv+0.5)*$range] [expr $sum/$num]"
	    set sum 0
	    set num 0
	}
	set sum [expr $sum + $thr($i)]
	incr num
	set priv $cur
    }
    if {$num > 0} {
	lappend result "[expr ($priv+0.5)*$range] [expr $sum/$num]"
    }
    return $result
}


####### read files

foreach fidx $idxs {

    # Bottleneck BW
    array set lset [readindexeddata [format "model/link-%d" $fidx]]
    array set lavg [readindexeddata [format "data2/renoreno%d.lavg" $fidx]]
    foreach fid [array names lset] {
	set links $lset($fid)
	if {$fid < $maxlflow} {
	    set bbw 0
	    foreach lid $links {
		if {$lid < $maxlink} {
		    set util $lavg($lid)
		    if {$util > $bbw} {
			set bbw $util
		    }
		}
	    }
	    set bneck($fid) [expr $bbw]
	}
    }
    set bnecks($fidx) [array get bneck]

    # Hops
    array set hop [readdata [format "model/flow-%d" $fidx]]
    foreach fid [array names hop] {
	set hop($fid) [lindex $hop($fid) 2]
    }
    set hops($fidx) [array get hop]

    # Read RTT
    set rtts($fidx) [readindexeddata [format "model/rtt-%d" $fidx]]
}


foreach file $prots {
    set thrb ""
    set thrh ""
    set thrr ""
    foreach fidx $idxs {
	array set favg [readindexeddata data2/$file$fidx.favg]
	array set hop $hops($fidx)
	array set rtt $rtts($fidx)
	array set bneck $bnecks($fidx)
	foreach fid [array names favg] {
	    if {$fid < $maxlflow} {
		lappend thrb "$bneck($fid) $favg($fid)"
		lappend thrh "$hop($fid) $favg($fid)"
		lappend thrr "$rtt($fid) $favg($fid)"
	    }
	}
    }
    set thrb [lsort -decreasing -real -index 0 [rangeavg $thrb 80 20]]
    #set thrb [lsort -decreasing -real -index 0 [rangeavg2 $thrb 50 20]]
    set thrh [lsort -decreasing -real -index 0 [indexavg $thrh]]  
    set thrr [lsort -decreasing -real -index 0 [rangeavg $thrr 40 20]]
    #set thrr [lsort -decreasing -real -index 0 [rangeavg2 $thrr 50 10]]
    writeplaindata data3/$file.favgb $thrb
    writeplaindata data3/$file.favgh $thrh
    writeplaindata data3/$file.favgr $thrr
}
