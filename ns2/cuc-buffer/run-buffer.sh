# rename from run-linux.csh to run-linux.sh for .sh bash color highlight

#for sidebw in 100 150 500  
#  使用不同节点带宽, 循环多次 生成不同 dataxxx目录;  类似于 buffersizing 中的 r1 r2 r3 
#  汇总数据在 plot.py 中的 print "debug: parse_data data[x] 可以打印出进行查看
#  最后绘图时, 实际取用的是平均值
for sidebw in 100 150 500;
do
	# 最大链路有效率
	# 链路利用率 *1000
	# for utilz in 995 995 980 
	for utilz in 980 995 999 # 995 980 
	do
	 #for flownum in `seq 50 10 150` 50~100 10组实验约 7分钟 
	 for flownum in `seq 50 10 150`
	 # 流数量
	 #for flownum in 50
	 do
		for onewaydelay in 43.5
		do
			# 参考论文设置 设置瓶颈链路带宽
			buffer=360
			bw=62.5
			#buffer=`echo "$bw*$onewaydelay*25/1448" | bc`
			#if [ $buffer -lt 100 ]
			#then
			#	buffer=100
			#fi
			# BDP = Mbps * ms *2 = Kbps * s * 2 = Kb *2 = Kb * 2 /8bpB / 1448Bp pkt = 1000*2/8*1448=250/1448
			# We use 1/10 of BDP
			#sidebw=`echo "$bw*4" | bc`
			
			
			# 减小 endtime 可以起到加快测试的效果
			for endtime in 480
			#for endtime in 900
#20 200
			do
				#for i in highspeed reno htcp cubic hybla westwood bic vegas scalable
#highspeed reno vegas bic htcp cubic westwood hybla scalable
#htcp westwood cubic highspeed reno vegas
				#for i in veno lp yeah illinois compound

				# for i in bic cubic highspeed htcp hybla reno scalable vegas westwood veno lp yeah illinois compound cong;
				for i in reno;
				do
				 # 建立利用率分组目录;
				 datadir="data"$utilz
				 if ! [[ -d ${datadir} ]]; then mkdir ${datadir} ; fi
				 cd ${datadir}
					dirname=$utilz-$flownum-$sidebw-$onewaydelay-$endtime-$i
					echo "创建结果文件夹 $dirname"
#					rm $dirname -r
					mkdir $dirname
					cd $dirname
					echo "Agent/TCP/Linux" > config
					echo $i >> config
					echo $flownum >> config
					echo $bw"Mb" >> config          # 瓶颈带宽
					echo $onewaydelay"ms" >> config
					echo $buffer >> config
					echo $sidebw"Mb" >> config			# 节点带宽
					echo $endtime >> config
					echo $utilz >> config

					sttime=`cat /proc/uptime | awk '{print $1}'`
					date > time_report
					pwd
					# ns ../../test-linux.tcl > txt
					# 过滤部分调试信息
					ns ../../../test-buffer.tcl | sed -e '/cmd select_ca/d'
					
					edtime=`cat /proc/uptime | awk '{print $1}'`
					date >> time_report
					echo "$edtime - $sttime" | bc >> time_report
					
					# -${dirname}
					# 绘制队列占用图形
					xgraph.py -l queue0-size queue0
					xgraph.py -l util0 util0
					
					cd ..
				 cd ..
				done
			done
		done
	done
 done
done
