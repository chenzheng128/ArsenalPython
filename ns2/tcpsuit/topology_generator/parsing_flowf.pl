#!/usr/bin/perl

$seed=$ARGV[0];
system 'sed "s/[0-9]*$//" link-' .$seed . ' | awk \'{print $1,$3,$4,$5,$6}\' | awk \'{sub(/[ \t]+$/, "");print}\' | head -n 30 > processing1';

@mylist = ();
open(FILE, "processing1");

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
print "digraph G {\n";
$counter = 0;
while( my ($k, $v) = each %vector ) {
	if ($k =~ /(\d*)-(\d*)-(\d*)-(\d*)/) {
		$newk = $1 . $2 . $3 . $4;
		#print "$newk\n";
	}
	if ($newk%2 == 0) { 
		#print "key: $k, value: $v.\n";
		# forward clusters 
		print "\tsubgraph cluster_$counter {\n";
		print "\t\tstyle=filled;\n";
		print "\t\tcolor=lightgrey;\n";
		print "\t\tnode [style=filled,color=white];\n"; 
		@flowlist = split(/-/, $v);
		@forwardlinklist = split(/-+/, $k);

		#$test = join(':', @forwardlinklist);
		#print "list1=$test $#forwardlinklist\n";
		# get rid of empty positions in the forwardlinklist

		# sanity check and clean up
		for($e=0;$e<=$#forwardlinklist;$e++) {
			if (length($forwardlinklist[$e])==0) {
				splice(@forwardlinklist, $e, 1);
			}
		}
		#$test2 = join(':', @forwardlinklist);
		#print "list2=$test2 $#forwardlinklist\n";

		# good vectors insert invisible nodes
		$number_invisible_nodes = ($forwardlinklist[0]/2);
		if ($number_invisible_nodes > 0) {
			#creating the invisible nodes
			print "\t\t{ node [shape=circle style=invis]\n\t\t\t";
			for ($f=0;$f<$number_invisible_nodes;$f++) {
				print "$f ";
			}
			print "\n\t\t}\n";

			#connecting the invisible to the first flow node
                        print "\t\tnode [style=filled,color=white];\n";
                        print "\t\t{ edge [style=invis]\n";
                        for ($g=0;$g<($number_invisible_nodes-1);$g++) {
                                print "\t\t\t" . $g . "->" . ($g+1) . "\n";
                        }
                        print "\t\t\t".($number_invisible_nodes-1)." -> fs".$flowlist[0]."_c$counter\n";
                        print "\t\t}\n";
	
		}

		# connecting the nodes to the first link
		foreach $a (@flowlist) {
			print "\t\tfs".$a."_c$counter -> link".$forwardlinklist[0]."_c$counter;\n";
		}	

		# connecting the links together
		for($b=0;$b<$#forwardlinklist;$b++) {
print "\t\tlink" .$forwardlinklist[$b]."_c$counter -> link". $forwardlinklist[$b+1]."_c$counter;\n"
		}
 
                # connecting the last link to the receiver nodes
                foreach $c (@flowlist) {
                        print "\t\tlink".$forwardlinklist[$#forwardlinklist]."_c$counter -> fr".$c."_c$counter;\n";
                }

                # coloring nodes
                foreach $d (@forwardlinklist) {
                        print "\t\tlink".$d. "_c$counter [color=".$mycolor[($d/2)]."];\n";
                }

		#print "key: $k, value: $v.\n";
		$label_string = join(' ', @flowlist);
		print "\t\tlabel = \"Flows " . $label_string . "\";\n";
		print "\t}\n\n";
	}
	$counter++;
}
print "}";
