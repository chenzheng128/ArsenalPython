#!/bin/bash

# 打开 DEFAULT 值, 即可以还原图形

endtime=900
sidebw=100
tcpstartinterval=0.0 # DEFAULT 控制不同 tcp 流的启动时间, 会影响流之间的同步
tmin=4.0 			 #DEFAULT
bw=100				 #DEFAULT
link_delay=250us
link_cap=100
K=20
run_time=10.0
# DEFAULT

#run_time=3.0  # fig12 不需要太长运行时间
tcpstartinterval=0.0

tmin=0.0 # 设置 tmin 为 0, 便于观察流的同步
#for num_flows in 2 ; # DEFAULT 
for num_flows in 2;
do
	for K in 45  # DEFAULT
	#for tcpstartinterval in 0.05 0.1
	do
		#for link_delay in 250us 100us
		for link_delay in 250us
		do
			#for bw in 500
			for link_cap in 100
			do
				#for i in highspeed reno htcp cubic hybla westwood bic vegas scalable
#highspeed reno vegas bic htcp cubic westwood hybla scalable
#htcp westwood cubic highspeed reno vegas
				#for i in veno lp yeah illinois compound

				#for i in DCTCP TCP
				for i in DCTCP
				# bic cubic highspeed htcp hybla reno scalable vegas westwood veno lp yeah illinois compound cong;
				# for i in cubic;
				do
					### PRE SCRIPT ...
					if [[ ! -d ../output ]]; then
						echo "please cd output/ and exec ../run.sh "
						exit
					fi

					dirname=$tmin-$num_flows-$link_delay-$link_cap-$K-$i
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
					export num_flows=$num_flows
					export tcpstartinterval=$tcpstartinterval
					export tmin=$tmin
					export link_delay=$link_delay
					export link_cap=$link_cap
					export congestion_algs=$i
					export K=$K
					export run_time=$run_time

					### RUNNING SCRIPT START ...
					sttime=`cat /proc/uptime | awk '{print $1}'`
					date > time_report.txt
					pwd
					# ns ../../test-linux.tcl > txt
					# 打开调试信息
					python ../../run_sim.py --fig_14
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
