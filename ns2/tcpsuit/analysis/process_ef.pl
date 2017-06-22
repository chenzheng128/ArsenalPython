$filename = @ARGV[0];
$ext = @ARGV[1];
open (FILE, "$filename.$ext");
@lines = <FILE>;

%cluster1;
%cluster2;

foreach $line (@lines) {
	chomp($line);
	($band, $utiliz) = split(/ /, $line);
	#print "$band $utiliz = ";
	$index = int($band / 200);
	if (not defined($cluster1{$index})) {
		#print "not def ";
		$cluster1{$index} = $utiliz;
		$cluster2{$index} = 1;	
	} else {
		#print "def ";
		$temp = $cluster1{$index};
		$temp = $temp + $utiliz;
		$cluster1{$index} = $temp;
		$cluster2{$index} = $cluster2{$index} + 1;
	}
	#print "$index ($cluster1{$index}/$cluster2{$index})\n";
}

foreach $key (sort(keys %cluster1)) {
	$avg = $cluster1{$key} / $cluster2{$key};
	print "$key $avg\n";
}
