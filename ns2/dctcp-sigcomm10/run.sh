#!/bin/bash

# 打开 DEFAULT 值, 即可以还原图形

endtime=900
sidebw=100
tcpstartinterval=0.0 # DEFAULT 控制不同 tcp 流的启动时间, 会影响流之间的同步
tmin=4.0 			 #DEFAULT



tmin=0.0
for flownum in 2; # DEFAULT 
#for flownum in 2 20;
do
	for tcpstartinterval in 0.0  # DEFAULT
	#for tcpstartinterval in 0.05 0.1
	do
		for onewaydelay in 25
		do
			for bw in 100
			do
				#for i in highspeed reno htcp cubic hybla westwood bic vegas scalable
#highspeed reno vegas bic htcp cubic westwood hybla scalable
#htcp westwood cubic highspeed reno vegas
				#for i in veno lp yeah illinois compound

				for i in dctcp
				# bic cubic highspeed htcp hybla reno scalable vegas westwood veno lp yeah illinois compound cong;
				# for i in cubic;
				do
					### PRE SCRIPT ...
					if [[ ! -d ../output ]]; then
						echo "please cd output/ and exec ../run.sh "
						exit
					fi

					dirname=$tmin-$flownum-$bw-$onewaydelay-$tcpstartinterval-$i
#					rm $dirname -r
					mkdir $dirname
					cd $dirname
					# 旧的参数读取方法
					# echo "Agent/TCP/Linux" > config
					# echo $i >> config
					# echo $flownum >> config
					# echo $bw"Mb" >> config
					# echo $onewaydelay"ms" >> config
					# echo $buffer >> config
					# echo $sidebw"Mb" >> config
					# echo $endtime >> config

					# 新的参数读取
					export onewaydelay=$onewaydelay
					export flownum=$flownum
					export tcpstartinterval=$tcpstartinterval
					export tmin=$tmin

					### RUNNING SCRIPT START ...
					sttime=`cat /proc/uptime | awk '{print $1}'`
					date > time_report.txt
					pwd
					# ns ../../test-linux.tcl > txt
					# 打开调试信息
					python ../../run_sim.py --fig_1
					# ns ../../test-linux.tcl
					
					edtime=`cat /proc/uptime | awk '{print $1}'`
					date >> time_report
					echo "$edtime - $sttime" | bc >> time_report.txt
					### RUNNING SCRIPT STOP ....
					
					
					### POST SCRIPT ...

					cd ..
				done
			done
		done
	done
done
