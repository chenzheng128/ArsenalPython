BEGIN { FS = " "} { nl++ } { s=s+$1} END {print "average:" s/nl}
