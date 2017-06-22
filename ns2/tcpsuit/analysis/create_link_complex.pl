$trial = $ARGV[0];

system ("awk '{if (\$1%2==0) print}' topology-$trial > top_even");
system ("awk '{if (\$1%2!=0) print}' topology-$trial > top_odd");
system ("paste top_odd top_even | awk '{print \$1,\$2\$6,\$5,\$4,\$8}' | sed \"s/ms//\" > top");

# simple case 
$start=6;
$counter=0;
$long_lived=30;
open(TOPO,">link-$trial");
open(RTT,">rtt-$trial");
open(FLOW,">flow-$trial");
open(FILE, "top");
@read_file = <FILE>;
	foreach (@read_file) {
		chomp($_);
		if ($_ =~ /(.*) (.*) (.*) (.*) (.*)$/) {
			print FLOW "$1 $3";
			print TOPO "$counter $start";
			$delay = $4 + $5;
			print "$4 $5 $delay\n";
			if ($2 eq "10") {
				print TOPO " 5 ";
				$middle_delay = 143.666;
				print FLOW " 16 ";
			}

			if ($2 eq "01") {
				print TOPO " 0 ";
				$middle_delay = 143.666;
				print FLOW " 14 ";
			}

			if ($2 eq "20") {
				print TOPO " 3 ";
				$middle_delay = 208.5295;
				print FLOW " 8 ";
			}

			if ($2 eq "02") {
				print TOPO " 2 ";
				$middle_delay = 208.5295;
				print FLOW " 14 ";
			}
			
			if ($2 eq "12") {
				print TOPO " 1 ";
				$middle_delay = 240.63;
				print FLOW " 16 ";
			}

			if ($2 eq "21") {
				print TOPO " 4 ";
				$middle_delay = 240.63;
				print FLOW " 11 ";
			}
			
			print TOPO $start+=2;
		}
		$start++;
		$total_delay = ($delay*2) + $middle_delay;
		print TOPO "\n";
		print RTT "$counter $total_delay\n";

		if ($counter < $long_lived) { 
			print FLOW "0\n";
		} else { 
			print FLOW "1\n";
		}

		$counter++;
	}
close(FLOW);
close(TOPO);
close(RTT);
