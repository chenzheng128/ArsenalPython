NSDIR="/home/cesar/ns-allinone-2.31/ns-2.31"
SAMPLES="1 2 3 4 5 6 7 8 9 10"
version="1 2 3 4 5 6 7"
prot1="reno"
prot2="reno"
buffer="1333"
duration="1200"

for i in $version
do
	for c in $SAMPLES
	do
		echo "#!/bin/tcsh" > exp$i-seed$c

case "$i" in 
     '1') 
       	prot2="reno"
	prot1="reno"
         ;; 
     '2') 
       	prot2="cubic"
	prot1="cubic"
         ;; 
     '3') 
       	prot2="reno"
	prot1="cubic"
         ;; 
     '4') 
       	prot2="htcp"
	prot1="htcp"
         ;; 
     '5') 
       	prot2="reno"
	prot1="htcp"
         ;; 
     '6') 
       	prot2="compound"
	prot1="compound"
         ;; 
     '7') 
       	prot2="reno"
	prot1="compound"
         ;; 
esac

#		if [[ $i == "2" ]] 
#		then prot2="reno"
#		else prot2=$prot1
#		fi
		echo $NSDIR"/ns ./script.tcl $c $prot1 $prot2 $buffer $duration" >> exp$i-seed$c
		echo "nohup sh ./exp$i-seed$c > exp$i-seed$c.output &" >> submit_batch$i.sh
	done
chmod 755 exp$i-seed?
chmod 755 exp$i-seed??
done

chmod 755 submit_batch1.sh
chmod 755 submit_batch2.sh
