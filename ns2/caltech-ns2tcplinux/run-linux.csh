for flownum in 1
do
	for bw in 100
	do
		sidebw=1000
		for onewaydelay in 64
		do
			buffer=220
			for endtime in 900
			do
				for i in highspeed reno htcp cubic hybla westwood bic vegas scalable lp yeah compound veno illinois
				do
					dirname=$flownum-$bw-$onewaydelay-$endtime-$i
					mkdir $dirname
					cd $dirname
					echo "Agent/TCP/Linux" > config
					echo $i >> config
					echo $flownum >> config
					echo $bw"Mb" >> config
					echo $onewaydelay"ms" >> config
					echo $buffer >> config
					echo $sidebw"Mb" >> config
					echo $endtime >> config

					sttime=`cat /proc/uptime | awk '{print $1}'`
					date > time_report
					~/ns-allinone-2.28/ns-2.31-linux-doc/ns ../test-linux.tcl > txt
					edtime=`cat /proc/uptime | awk '{print $1}'`
					date >> time_report
					echo "$edtime - $sttime" | bc >> time_report
					cat result0 | awk 'BEGIN{old=0}{print $1, ($3-old)*1448*8*2}{old=$3}' > rate0
					cd ..
				done
			done
		done
	done
done
