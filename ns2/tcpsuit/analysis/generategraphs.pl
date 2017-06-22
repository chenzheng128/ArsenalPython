#system ("ls data | sed \"s/[0-9].*//\" | uniq > protocols");
        open(LOC_FILE, "graph_protocol");
        @read_file = <LOC_FILE>;

        $allprot = '';
        $hsprot = '';
        $renoprot = '';
        $mixedprot = '';
	@aloneprot = [];
	$i = 0;

        foreach (@read_file) {
                chomp($_);
                $allprot = $allprot . $_ . ' ';

                if ($_ =~ /^renoreno/) { 
                        $renoprot = $_;
                } else { 
                  if ($_ =~ /(.*[b-z])reno/) {
                        $mixedprot = $mixedprot . $_ . ' ';
			$aloneprot[$i] = $1;
			$i++;
                  } else {
                        $hsprot = $hsprot . $_ . ' ';
                  }
                }
        }
        #print "all protocols: $allprot\n";
        #print "ly high speed: $hsprot\n";
        #print "ly mixed reno: $mixedprot\n";
        #print "ly reno reno: $renoprot\n";
#	foreach (@aloneprot) {
#		print "$_\n";
#	}

# Generate a big graph generator based on the files on data
# 1 fcompb1
$msg = "echo \"\n"
. "set terminal png\n"
. "set ylabel 'Relative throughput'\n"
. "set xlabel 'Bottleneck link utilization [Mbps]'\n"
. "set size 0.7,0.7\n"
. "set output 'vsreno-fcompb1.png'\n"
. "plot 1 notitle,\\\n";
@mix = split(/ /, $mixedprot);
$i = 0;
foreach (@mix) {
	$a = $i + 1;
	$msg = $msg . "'data3/$_.fcompb1' title '$aloneprot[$i]' with linespoints $a,\\\n";
	$i++;
}

chop($msg);
chop($msg);
chop($msg);
chop($msg);

$msg = $msg . "\n \" | gnuplot ; ";
print $msg;
print ("\n\n");

# 2 fcompb2
$msg2 = "echo \"\n"
. "set terminal png\n"
. "set ylabel 'Throughput degradation'\n"
. "set xlabel 'Bottleneck link utilization [Mbps]'\n"
. "set size 0.7,0.7\n"
. "set output 'vsreno-fcompb2.png'\n"
. "plot 1 notitle,\\\n";
@mix = split(/ /, $mixedprot);
$i = 0; 
foreach (@mix) {
        $a = $i + 1;
        $msg2 = $msg2 . "'data3/$_.fcompb2' title '$aloneprot[$i]' with linespoints $a,\\\n";
        $i++;
}

chop($msg2);
chop($msg2);
chop($msg2);
chop($msg2);

$msg2 = $msg2 . "\n \" | gnuplot ; ";
print $msg2;
print ("\n\n");

# 3 fcomph1
$msg3 = "echo \"\n"
. "set terminal png\n"
. "set ylabel 'Relative throughput'\n"
. "set xlabel 'Number of hops'\n"
. "set size 0.7,0.7\n"
. "set xtics 1\n"
. "set output 'vsreno-fcomph1.png'\n"
. "plot 1 notitle,\\\n";
@mix = split(/ /, $mixedprot);
$i = 0;
foreach (@mix) {
        $a = $i + 1;
        $msg3 = $msg3 . "'data3/$_.fcomph1' title '$aloneprot[$i]' with linespoints $a,\\\n";
        $i++;
}

chop($msg3);
chop($msg3);
chop($msg3);
chop($msg3);

$msg3 = $msg3 . "\n \" | gnuplot ; ";
print $msg3;
print ("\n\n");

# 4 fcomph2
$msg4 = "echo \"\n"
. "set terminal png\n"
. "set ylabel 'Throughput degradation'\n"
. "set xlabel 'Number of hops'\n"
. "set size 0.7,0.7\n"
. "set xtics 1\n"
. "set output 'vsreno-fcomph2.png'\n"
. "plot 1 notitle,\\\n";
@mix = split(/ /, $mixedprot);
$i = 0;
foreach (@mix) {
        $a = $i + 1;
        $msg4 = $msg4 . "'data3/$_.fcomph2' title '$aloneprot[$i]' with linespoints $a,\\\n";
        $i++;
}

chop($msg4);
chop($msg4);
chop($msg4);
chop($msg4);

$msg4 = $msg4 . "\n \" | gnuplot ; ";
print $msg4;
print ("\n\n");

# 5 fcompr1
$msg5 = "echo \"\n"
. "set terminal png\n"
. "set ylabel 'Relative throughput'\n"
. "set xlabel 'Round trip delay [msec]'\n"
. "set size 0.7,0.7\n"
. "set output 'vsreno-fcompr1.png'\n"
. "plot 1 notitle,\\\n";
@mix = split(/ /, $mixedprot);
$i = 0;
foreach (@mix) {
        $a = $i + 1;
        $msg5 = $msg5 . "'data3/$_.fcompr1' title '$aloneprot[$i]' with linespoints $a,\\\n";
        $i++;
}

chop($msg5);
chop($msg5);
chop($msg5);
chop($msg5);

$msg5 = $msg5 . "\n \" | gnuplot ; ";
print $msg5;
print ("\n\n");

# 6 fcompr2
$msg6 = "echo \"\n"
. "set terminal png\n"
. "set ylabel 'Throughput degradation'\n"
. "set xlabel 'Round trip delay [msec]'\n"
. "set size 0.7,0.7\n"
. "set output 'vsreno-fcompr2.png'\n"
. "plot 1 notitle,\\\n";
@mix = split(/ /, $mixedprot);
$i = 0;
foreach (@mix) {
        $a = $i + 1;
        $msg6 = $msg6 . "'data3/$_.fcompr2' title '$aloneprot[$i]' with linespoints $a,\\\n";
        $i++;
}

chop($msg6);
chop($msg6);
chop($msg6);
chop($msg6);

$msg6 = $msg6 . "\n \" | gnuplot ; ";
print $msg6;
print ("\n\n");

# 7 favgb
$msg7 = "echo \"\n"
. "set terminal png\n"
. "set ylabel 'Average per-flow throughput (Mbps)'\n"
. "set xlabel 'Bottleneck link utilization [Mbps]'\n"
. "set size 0.7,0.7\n"
. "set output 'vshs-favgb.png'\n"
. "plot 1 notitle,\\\n";
@mix = split(/ /, $hsprot);
$i = 0;

if (defined($renoprot)) {
$msg7 = $msg7 . "'data3/$renoprot.favgb' title 'reno' with linespoints 1,\\\n";
}

foreach (@mix) {
        $a = $i + 2;
        $msg7 = $msg7 . "'data3/$_.favgb' title '$aloneprot[$i]' with linespoints $a,\\\n";
        $i++;
}

chop($msg7);
chop($msg7);
chop($msg7);
chop($msg7);

$msg7 = $msg7 . "\n \" | gnuplot ; ";
print $msg7;
print ("\n\n");

# 8 favgh
$msg8 = "echo \"\n"
. "set terminal png\n"
. "set ylabel 'Average per-flow throughput (Mbps)'\n"
. "set xlabel 'Number of hops'\n"
. "set size 0.7,0.7\n"
. "set xtics 1\n"
. "set logscale y\n"
. "set output 'vshs-favgh.png'\n"
. "plot 1 notitle,\\\n";
@mix = split(/ /, $hsprot);
$i = 0;

if (defined($renoprot)) {
$msg8 = $msg8 . "'data3/$renoprot.favgh' title 'reno' with linespoints 1,\\\n";
}

foreach (@mix) {
        $a = $i + 2;
        $msg8 = $msg8 . "'data3/$_.favgh' title '$aloneprot[$i]' with linespoints $a,\\\n";
        $i++;
}

chop($msg8);
chop($msg8);
chop($msg8);
chop($msg8);

$msg8 = $msg8 . "\n \" | gnuplot ; ";
print $msg8;
print ("\n\n");

# 9 favgr
$msg9 = "echo \"\n"
. "set terminal png\n"
. "set ylabel 'Average per-flow throughput (Mbps)'\n"
. "set xlabel 'Round trip delay [msec]'\n"
. "set size 0.7,0.7\n"
. "set logscale y\n"
. "set output 'vshs-favgr.png'\n"
. "plot 1 notitle,\\\n";
@mix = split(/ /, $hsprot);
$i = 0;

if (defined($renoprot)) {
$msg9 = $msg9 . "'data3/$renoprot.favgr' title 'reno' with linespoints 1,\\\n";
}

foreach (@mix) {
        $a = $i + 2;
        $msg9 = $msg9 . "'data3/$_.favgr' title '$aloneprot[$i]' with linespoints $a,\\\n";
        $i++;
}

chop($msg9);
chop($msg9);
chop($msg9);
chop($msg9);

$msg9 = $msg9 . "\n \" | gnuplot ; ";
print $msg9;
print ("\n\n");

# 10 fcompb
$msg10 = "echo \"\n"
. "set terminal png\n"
. "set ylabel 'Relative throughput'\n"
. "set xlabel 'Bottleneck link utilization [Mbps]'\n"
. "set size 0.7,0.7\n"
. "set output 'vshs-fcompb.png'\n"
. "plot 1 notitle,\\\n";
@mix = split(/ /, $hsprot);
$i = 0;

if (defined($renoprot)) {
$msg10 = $msg10 . "'data3/$renoprot.fcompb' title 'reno' with linespoints 1,\\\n";
}

foreach (@mix) {
        $a = $i + 2;
        $msg10 = $msg10 . "'data3/$_.fcompb' title '$aloneprot[$i]' with linespoints $a,\\\n";
        $i++;
}

chop($msg10);
chop($msg10);
chop($msg10);
chop($msg10);

$msg10 = $msg10 . "\n \" | gnuplot ; ";
print $msg10;
print ("\n\n");

# 11 fcomph
$msg11 = "echo \"\n"
. "set terminal png\n"
. "set ylabel 'Relative throughput'\n"
. "set xlabel 'Number of hops'\n"
. "set size 0.7,0.7\n"
. "set xtics 1\n"
. "set output 'vshs-fcomph.png'\n"
. "plot 1 notitle,\\\n";
@mix = split(/ /, $hsprot);
$i = 0;

foreach (@mix) {
        $a = $i + 2;
        $msg11 = $msg11 . "'data3/$_.fcomph' title '$aloneprot[$i]' with linespoints $a,\\\n";
        $i++;
}

chop($msg11);
chop($msg11);
chop($msg11);
chop($msg11);

$msg11 = $msg11 . "\n \" | gnuplot ; ";
print $msg11;
print ("\n\n");

# 12 fcompr
$msg12 = "echo \"\n"
. "set terminal png\n"
. "set ylabel 'Relative throughput'\n"
. "set xlabel 'Round trip delay [msec]'\n"
. "set size 0.7,0.7\n"
. "set output 'vshs-fcompr.png'\n"
. "plot 1 notitle,\\\n";
@mix = split(/ /, $hsprot);
$i = 0;

foreach (@mix) {
        $a = $i + 2;
        $msg12 = $msg12 . "'data3/$_.fcompr' title '$aloneprot[$i]' with linespoints $a,\\\n";
        $i++;
}

chop($msg12);
chop($msg12);
chop($msg12);
chop($msg12);

$msg12 = $msg12 . "\n \" | gnuplot ; ";
print $msg12;
print ("\n\n");

# 13 ef
print ("gnuplot ef_graph.gpl\n");

print ("gnuplot link_graph.gpl\n"); 
