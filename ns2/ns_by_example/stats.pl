#!/usr/bin/perl

#
# simple perl script to print some stats based on bottleneck router
# 

#######################################
# system defaults
$l1 = "1";
$l2 = "2";
$flow_type = "tcp";
$max_bwidth = 0;

#######################################
# Process command line args.
while ($_ = $ARGV[0], /^-/)
{
  shift;
  if (/^-h/)      { $Usage; }
  elsif (/^-v/)   { $verbose_mode = 1;}
  elsif (/^-t/)  { if ( $ARGV[0] ne '' ) {
		      $flow_type = $ARGV[0];  
                      shift; }}
  elsif (/^-m/)  { if ( $ARGV[0] ne '' ) {
		      $max_bwidth = $ARGV[0];  
                      shift; }}
  elsif (/^-l1/)  { if ( $ARGV[0] ne '' ) {
		      $l1 = $ARGV[0];  
                      shift; }}
  elsif (/^-l2/)  { if ( $ARGV[0] ne '' ) {
		      $l2 = $ARGV[0];  
                      shift; }}
  else            { warn "$_ bad option\n"; &Usage; }
}

# Now, make sure one and only one filename was specified
if (($ARGV[0] eq '') || ($ARGV[1] ne '')) {
  warn "Need to specify one and only one filename\n";
  &Usage;
}
$file = $ARGV[0];

# need to have specified max bwidth
if ($max_bwidth <= 0) {
  warn "Need to specify max bandwidth in Bps";
  &Usage;
}

if ($verbose_mode) {
  print "file: $file\n";
  print "l1: $l1\n";
  print "l2: $l2\n";
}

#######################################

# count the number of lines
$cmd = "cat $file | grep ^- | grep \" $l1 $l2 $flow_type \" | wc -l";
$lines = `$cmd`; 
chop($lines);
if ($lines == 0) {
  printf("No input lines in command:\n");
  printf("\t $cmd\n");
  printf("Exiting ...\n");
  exit(1);
}

# get drops
$drop = `cat $file | grep ^d | grep -c " $l1 $l2 $flow_type "`;
chop($drop);

# get output link packets for flow (actually dequeue)
$dq = `cat $file | grep " $l1 $l2 $flow_type "| grep -c ^-`;
chop($dq);

# get start/stop of flow
$start = `cat $file | grep "$flow_type"| head -1 | column 1`;
chop($start);
$stop = `cat $file | grep "$flow_type"| tail -1 | column 1`;
chop($stop);

# thruput and util
$thru = ($dq) / ($stop - $start);
$util = $thru / (($stop - $start) * ($max_bwidth * 1000));

if ($verbose_mode) {
  printf ("$flow_type lines: %d\n", $lines);
}
printf ("dropped:  %d packets\n", $drop);
printf ("   sent:  %d packets\n", $dq);
printf ("  start:  %.2f seconds\n", $start);
printf ("   stop:  %.2f seconds\n", $stop);
printf ("thruput:  %d Kbps\n", $thru);
printf ("   util:  %.2f\n", $util);

exit(1);

# print usage and quit
sub Usage {
  printf STDERR "usage: stats.pl [flags] <filename>, where:\n";
  printf STDERR "\t-t  {tcp|cbr} flow type (default tcp)\n";
  printf STDERR "\t-l1 #         start link bottlneck router (default 1)\n";
  printf STDERR "\t-l2 #         end link bottlneck router (default 2)\n";
  printf STDERR "\t-m #          max bandwidth of bottlneck link (in Mbps)\n";
  printf STDERR "\t-v            verbose output\n";
  printf STDERR "\t-h            this help message\n";
  exit(1);
}
