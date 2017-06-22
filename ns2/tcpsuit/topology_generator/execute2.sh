NSDIR="/home/cesar/ns-allinone-2.31/ns-2.31"
TOPO="random"
NW_SIZE="3"
CAPACITY="1000"
DELAY="3"
SHORT_LIVED="100"
LONG_LIVED="40"
SEEDS="1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30"

for l in $LONG_LIVED
do
	mkdir model
	for c in $SEEDS
	do
		echo "nlong_lived=$l seed=$c"
$NSDIR/ns topogen.tcl $TOPO $NW_SIZE 2 $CAPACITY $DELAY $l $SHORT_LIVED p2p
		size=$((NW_SIZE-1))
		perl ./generate_link.pl $size
		mv model-flow model/flow-$c
		mv model-link model/link-$c
		mv model-rtt model/rtt-$c
		mv model-topology model/topology-$c
	done
	mv model slived_$SHORT_LIVED\_llived$l
	sleep 2
done
