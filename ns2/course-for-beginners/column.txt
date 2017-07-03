#!/usr/bin/perl

# Mark Claypool
# Last significantly modified: December, 2001

# This program prints out fields of an indicated column.
# The columns are numbered 0, 1, 2, 3 ...

require 'getopts.pl';

&ParseCommandLine;
$line = <STDIN>;
while ($line) {
  $line =~ s/^\s+//;		# remove initial white-space
  $line =~ s/\s+/ /g;		# turn double-space into single space
  @word = split($split,$line);	# columns will then be $1, $2, $3 ...
  $i =0;
  while ($i <= $#col) {
    print "@word[@col[$i]]\t";
    $i += 1;
  }			
  print "\n";
  $line = <STDIN>;
}
exit;

#######################################################################
# ParseCommandLine
# check for the right number of command line arguments
# print usage message and quit if there is an error
# global variables are @col
sub ParseCommandLine   {

  # get token to split on
  &Getopts('t:');
  if ($opt_t) {
    $split = $opt_t;
  } else {
    $split = '\s+';
  }

  # get columns
  while ($#ARGV >= 0) {
    $arg = shift(@ARGV);
    if ($arg =~ /^(\d+)/) {
      push(@col, $1);
    } else {		
      &usage;
    }
  }
  if ($#col < 0) {
    &usage;
  }
}		

##########################################################################
# usage
# print a usage maessage and quit
sub usage
{
    print STDERR "column: print fields from an indicated column\n";
    print STDERR "Usage: column <flags>, where flags are:\n";
    print STDERR "       [-t str]\ttoken to use as a separator (default is white space)\n"; 
    print STDERR "       {# [#...]}\tcolumn(s) to print, numbered 0,1,2...\n"; 
	exit;

}
