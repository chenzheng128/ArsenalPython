# 0 1 1000Mb 3.087841e+01ms
# 1 2 1000Mb 1.057665e+01ms
# 2 3 1000Mb 2.369631e+00ms
# 3 4 1000Mb 4.336767e+01ms
# 5 4 1000Mb 3.633943e+01ms
$core = $ARGV[0];

open(LOC_FILE, "model-topology");
open(LINK, "> model-link");
open(RTT, "> model-rtt");
@read_file = <LOC_FILE>;
$entries = @read_file;
@core = [];
%links = {};

#print "core = $core\n\n";
$corenumber = 0;
for ($i=0; $i<$core; $i++) { 
	$line = $read_file[$i];
	chomp($line);	
	if ($line =~ /(\d+) (\d+) (\d+)Mb (\d+\.\d+)e([\+\-])(\d+)ms/) {
		if ($5 eq "+") {
			$expoent = (10**$6);
		} else {
			$expoent = (10**($6*(-1)));
		}
		$core[$1] = $4 * $expoent;
		#print "$1 $core[$1]\n";

                if (($1 % 2) == 0) {
                        $even_src = $1;
                        $even_dst = $2;
                        $even_rtt = $4 * $expoent;
                } else {
                        #print "even $1 $2 $3 $4 $expoent\n";
                        $odd_src = $1;
                        $odd_dst = $2;
                        $odd_rtt = $4 * $expoent;

                        $index = $even_src . "," . $even_dst;
			$index3 = $even_dst . "," . $even_src;
			$links{$index} = ($corenumber-1)*2;
			$links{$index3} = (($corenumber-1)*2)+1;
                        
			$index2 = $odd_src . "," . $odd_dst;
			$index4 = $odd_dst . "," . $odd_src;
                        $links{$index2} = ($corenumber*2);
                        $links{$index4} = ($corenumber*2)+1;
                        
			#print "$index ($links{$index}) $index3 ($links{$index3}) $index2 ($links{$index2}) $index4 ($links{$index4})\n";
		}
	}
$corenumber++;
}

$flownumber = 0;
for ($j=$core; $j<$entries; $j++) {
	$line = $read_file[$j];
	chomp($line);
	if ($line =~ /(\d+) (\d+) (\d+)Mb (\d+\.\d+)e([\+\-])(\d+)ms/) {
	# new flow
		if ($5 eq "+") {
			$expoent = (10**$6);
		} else {
			$expoent = (10**($6*(-1)));
		}
		#print "$1 $2 $3 $4 $expoent\n";
		if (($1 % 2) != 0) { 
			$odd_src = $1;
			$odd_dst = $2;
			$odd_rtt = $4 * $expoent;
			$cum = 0;
			$path = "";
			# "odd $1 $2 $3 $4 $expoent\n";
		} else { 
			#print "even $1 $2 $3 $4 $expoent\n";
			$even_src = $1;
			$even_dst = $2;
			$even_rtt = $4 * $expoent;
			
			$index = $odd_src . "," . $odd_dst; 
			$links{$index} = (($flownumber + $core)*2) + (($flownumber) * 2);
			
			$index3 = $odd_dst . "," . $odd_src; 
			$links{$index3} = ((($flownumber + $core)*2) + (($flownumber) * 2))+1;

			$index2 = $even_src . "," . $even_dst; 
			$links{$index2} = (($flownumber + $core)*2) + (($flownumber+1) * 2);
			
			$index4 = $even_dst . "," . $even_src; 
			$links{$index4} = ((($flownumber + $core)*2) + (($flownumber+1) * 2))+1;
			
#			print "$index ($links{$index}) $index3 ($links{$index3}) $index2 ($links{$index2}) $index4 ($links{$index4})\n";

			if ($odd_dst > $even_dst) {
				$direction = "reverse $odd_dst $even_dst";
				for ($a = $even_dst; $a < $odd_dst; $a++) {
					$next = $a + 1;
					$path = $path . "$a,$next ";
					$cum += $core[$a];
				}
			} else {
				$direction = "forward $odd_dst $even_dst";
				for ($a = $odd_dst; $a < $even_dst; $a++) {
					$next = $a + 1;
					$path = $path . "$a,$next ";
					$cum += $core[$a];
				}
			}
		
		chop($path);
		if ($direction =~ /reverse/) { 
			$path2 = reverse($path);
			$path = $path2;
		}

#print "flow ($odd_src,$odd_dst to $even_dst,$even_src) $direction\n";
	$total_rtt = ($odd_rtt + $even_rtt + $cum) * 2;
	print LINK "$flownumber ";
	$source = $odd_src . "," . $odd_dst;
	$source_val = $links{$source};
	print LINK "$source_val ";
	
	@unfold_path = split(/ /, $path);
	
	foreach $segment (@unfold_path) { 
		$link = $links{$segment};
		print LINK "$link ";	
	}

	$destination = $even_dst . "," . $even_src;
	$dest_val = $links{$destination};
	print LINK "$dest_val\n";

print RTT "$flownumber $total_rtt\n";
$flownumber++;
		}
	}
}

close(LINK);
close(RTT);
