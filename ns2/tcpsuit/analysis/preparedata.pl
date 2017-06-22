
	#system ("ls data | sed \"s/[0-9].*//\" | uniq > protocols");
	open(LOC_FILE, "process_protocol");
	@read_file = <LOC_FILE>;

	$allprot = '';
	$hsprot = '';
	$renoprot = '';
	$mixedprot = '';

	foreach (@read_file) {
		chomp($_);
               	$allprot = $allprot . $_ . ' ';
		
		if ($_ =~ /^renoreno/) { 
			$renoprot = $_;
		} else { 
		  if ($_ =~ /.*[b-z]reno/) {
			$mixedprot = $mixedprot . $_ . ' ';
			} else {
			$hsprot = $hsprot . $_ . ' ';
			}
		}
	}
	print "all protocols: $allprot\n";
	print "ly high speed: $hsprot\n";
	print "ly mixed reno: $mixedprot\n";
	print "ly reno reno: $renoprot\n";

	# processthr.tcl
	chop($allprot);
	system("sed \"s/set prots.*/set prots \\\"$allprot\\\"/\" processthr.tcl > processthr.tcl2");
	system("mv processthr.tcl2 processthr.tcl");

	# hsflow.tcl
	chop($hsprot);
	system("sed \"s/set prots.*/set prots \\\"$hsprot $renoprot\\\"/\" hsflows.tcl > hsflows.tcl2");
	system("mv hsflows.tcl2 hsflows.tcl");

	# link.tcl
	system("sed \"s/set prots.*/set prots \\\"$allprot\\\"/\" link.tcl > link.tcl2");
	system("mv link.tcl2 link.tcl");
	
	# comp-sep.tcl
	system("sed \"s/set prots.*/set prots \\\"$renoprot $hsprot\\\"/\" comp-sep.tcl > comp-sep.tcl2");
	system("mv comp-sep.tcl2 comp-sep.tcl");
	
	# comp-mix.tcl
	system("sed \"s/set prots.*/set prots \\\"$mixedprot\\\"/\" comp-mix.tcl > comp-mix.tcl2");
	system("mv comp-mix.tcl2 comp-mix.tcl");
