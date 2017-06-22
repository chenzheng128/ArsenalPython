# NSDIR="/home/cesar/ns-allinone-2.31/ns-2.31"
TOPO="parking"
NW_SIZE="5"
CAPACITY="1000"
DELAY="15"
SHORT_LIVED="0"
LONG_LIVED="40"
SEEDS="1 2 3 4 5 6 7 8 9 10 11 12"

for l in $LONG_LIVED
do
	mkdir model
	for c in $SEEDS
	do
		echo "nlong_lived=$l seed=$c"
$NSDIR/ns topogen.tcl $TOPO $NW_SIZE 0 $CAPACITY $DELAY $l $SHORT_LIVED p2p
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
