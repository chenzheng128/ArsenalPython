#!/usr/bin/perl

$seed=$ARGV[0];
system 'sed "s/[0-9]*$//" link-' .$seed . ' | awk \'{print $1,$3,$4,$5,$6}\' | awk \'{sub(/[ \t]+$/, "");print}\' | head -n 30 > processing2';

@mylist = ();
open(FILE, "processing2");

while (<FILE>) {
	if ($_ =~ /(\d+)*\ *(\d+)*\ *(\d+)*\ *(\d+)\ *(\d+)*/) {
		$ab = $2 ."-". $3 ."-". $4 ."-". $5;
		@mylist = ();
		#print "$ab $1\n";
		if (!defined $vector{$ab}) {
			$vector{$ab} = $1;
			#print "first element $ab | $1 | $vector{$ab}\n";
		} else {
			#print "mylist @mylist\n";
			@mylist = split(/-/, $vector{$ab});
			#print "mylist @mylist\n";
			push(mylist,$1);
			#print "mylist @mylist\n";
			$updatelist = join('-', @mylist);
			$vector{$ab} = $updatelist;
			#print "second or more element $ab | @mylist | $updatelist | $vector{$ab}\n";
		} 
	}
}

@mycolor = ("red","blue","green","yellow");
@static_list = (0, 2, 4, 6);
print "digraph G {\n";
print "\tsubgraph cluster {\n";
print "\t\tstyle=filled;\n";
print "\t\tcolor=lightgrey;\n";
print "\t\tnode [style=filled,color=white];\n"; 
while( my ($k, $v) = each %vector ) {
	if ($k =~ /(\d*)-(\d*)-(\d*)-(\d*)/) {
		$newk = $1 . $2 . $3 . $4;
		#print "$newk\n";
	}
	if ($newk%2 == 0) { 
		#print "key: $k, value: $v.\n";
		# forward clusters 
		@flowlist = split(/-/, $v);
		@forwardlinklist = split(/-+/, $k);

		# sanity check and clean up
		for($e=0;$e<=$#forwardlinklist;$e++) {
			if (length($forwardlinklist[$e])==0) {
				splice(@forwardlinklist, $e, 1);
			}
		}

		# connecting the nodes to the first link
		foreach $a (@flowlist) {
			print "\t\tfs".$a." -> link".$forwardlinklist[0].";\n";
		}	

                # connecting the last link to the receiver nodes
                foreach $c (@flowlist) {
                        print "\t\tlink".$forwardlinklist[$#forwardlinklist]." -> fr".$c.";\n";
                }
	}
}
		# coloring nodes
		$count = 0;
                foreach $d (@static_list) {
			if ($d != 6) {
			print "\t\tlink" .$count." -> link".($count+2).";\n";
                        }
			print "\t\tlink".$d. " [color=".$mycolor[($d/2)]."];\n";
                	$count+=2;
		}
print "}}";
