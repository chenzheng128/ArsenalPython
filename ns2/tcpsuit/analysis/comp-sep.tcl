#!/bin/tclsh
#######
####### Comparing two different protocols (separate run)
#######       Throughput improvement v.s. RTT, hop count, bottleneck link utilization
#######
# Input files
#    data2/(prot2)(prot2).*
# Output files
#    data3/(prot2)(prot2).fcompr
#       (throughput of prot2 in [prot2prot2]) / (throughput of prot1 in [prot1prot1]), sorted by RTT
#    data3/(prot2)(prot2).fcomph
#       (throughput of prot2 in [prot2prot2]) / (throughput of prot1 in [prot1prot1]), sorted by hop count
#    data3/(prot2)(prot2).fcompb
#       (throughput of prot2 in [prot2prot2]) / (throughput of prot1 in [prot1prot1]), sorted by bottleneck link utilization



####### Set of simulation senarios
set idxs "1 2 3 4 5 6 7 8 9 10"
#set idxs "1 2 7 8"

####### Set of ptorocols
set prots "renoreno compoundcompound cubiccubic htcphtcp wwarwwar arenoareno"

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

proc rangeavg {data range} {
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
        if {$i%10==0 || $i==[expr $idx-1]} {
            lappend result "$rtt($i) [expr $sum/($end-$start+1)]"
        }
    }
    return $result
}


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
    #array set rtt [readindexeddata [format "model/rtt-%d" $fidx]]
    #foreach fid [array names rtt] {
    #puts "$rtt($fid) [expr exp(int((log($rtt($fid))*10))/10.0)]"
    #set rtt($fid) [expr exp(int(log($rtt($fid))*5+0.5)/5.0)]
    #}
    #set rtts($fidx) [array get rtt]
}


foreach file $prots {
    puts "Processing... $file"
    set thrb ""
    set thrh ""
    set thrr ""
    foreach fidx $idxs {
	array set favg1 [readindexeddata data2/renoreno$fidx.favg]
	array set favg2 [readindexeddata data2/$file$fidx.favg]
	array set hop $hops($fidx)
	array set rtt $rtts($fidx)
	array set bneck $bnecks($fidx)
	foreach fid [array names favg1] {
	    set var [expr $favg2($fid)/$favg1($fid)]
	    if {$fid < $maxlflow} {
		lappend thrb "$bneck($fid) $var"
		lappend thrh "$hop($fid) $var"
		lappend thrr "$rtt($fid) $var"
		puts "$fid : $bneck($fid) $favg2($fid) $favg1($fid)"
	    }
	}
    }
    #set thrb [lsort -decreasing -real -index 0 $thrb]
    set thrb [lsort -decreasing -real -index 0 [rangeavg $thrb 20]]
    set thrh [lsort -decreasing -real -index 0 [indexavg $thrh]]
    #set thrr [lsort -decreasing -real -index 0 $thrr]
    set thrr [lsort -decreasing -real -index 0 [rangeavg $thrr 30]]
    writeplaindata data3/$file.fcompb $thrb
    writeplaindata data3/$file.fcomph $thrh
    writeplaindata data3/$file.fcompr $thrr
}
