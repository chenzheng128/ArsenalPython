# rename from run-linux.csh to un-linux.sh for .sh bash color highlight

for flownum in 5 2 1
#2 8 32 128
do

	for bw in 150
#1 10 100 1000
	do
		#sidebw=`echo "$bw*4" | bc`
		sidebw=1500
		for onewaydelay in 64
#2 8 32 128
		do
			#buffer=`echo "$bw*$onewaydelay*25/1448" | bc`
			#if [ $buffer -lt 100 ]
			#then
			#	buffer=100
			#fi
			# BDP = Mbps * ms *2 = Kbps * s * 2 = Kb *2 = Kb * 2 /8bpB / 1448Bp pkt = 1000*2/8*1448=250/1448
			# We use 1/10 of BDP
			buffer=220
			
			# 减小 endtime 可以起到加快测试的效果
			for endtime in 60
			#for endtime in 900
#20 200
			do
				#for i in highspeed reno htcp cubic hybla westwood bic vegas scalable
#highspeed reno vegas bic htcp cubic westwood hybla scalable
#htcp westwood cubic highspeed reno vegas
				#for i in veno lp yeah illinois compound

				# for i in bic cubic highspeed htcp hybla reno scalable vegas westwood veno lp yeah illinois compound cong;
				for i in cubic;
				do
					dirname=$flownum-$bw-$onewaydelay-$endtime-$i
#					rm $dirname -r
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
					pwd
					# ns ../../test-linux.tcl > txt
					# 打开调试信息
					ns ../../test-buffer.tcl
					
					edtime=`cat /proc/uptime | awk '{print $1}'`
					date >> time_report
					echo "$edtime - $sttime" | bc >> time_report
					
					# 使用 awk 通过 result0 中的 ack 计算速率; 1448 是什么?  8是Byte->bit; 2是每 0.5 秒取的数据, 需要按1秒算?
					# cat result0 | awk 'BEGIN{old=0}{print $1, ($3-old)*1448*8*2}{old=$3}' > rate0

					# xgraph.py 支持 -f 参数后, 不必再拆分数据
					# cat result0 | cut -d" " -f 1,3 > result0-ack
					# cat result0 | cut -d" " -f 1,4 > result0-bw
					
					# 注释 使用 plot_figures.sh 中的 xgraph.py 进行绘图
					# cwnd 图形
					# 使用这个命令可获取和网站一样的图形
					# 使用 gnuplot 绘图,
					# gnuplot ../../script-gnuplot.txt;
					# mv cwnd.png cwnd-$i.png;
					# mv rate.png rate-${i}.png;
					# echo "生成 ${dirname}/cwnd-${i}.png rate-${i}.png图形"
					
					cd ..
				done
			done
		done
	done
done
