#!/bin/bash

# Exit on any failure
set -e

# Check for uninitialized variables
set -o nounset

ctrlc() {
	sudo killall -9 python
	sudo mn -c
	exit
}

trap ctrlc SIGINT

start=`date`
exptid=`date +%b%d-%H:%M`
rootdir=results/dasdn-$exptid
bw=100

# Note: you need to make sure you report the results
# for the correct port!
# In this example, we are assuming that each
# client is connected to port 2 on its switch.

#for n in 1 2 3 4 5; do
for n in 5; do
    dir=$rootdir-n$n
		# 运行实验 的 主要参数区别
    sudo python dasdn.py --bw $bw \
        --dir $dir \
				-n $n \
				-t 10
				# -m 10

				# --switch_bw \
				#-m 114
				#-m 114


		# 清除 不需要的 eth99 数据
		sudo sed -e '/s2-eth99/d' $dir/bwm.txt > $dir/bwm2.txt
		# 绘图
    sudo python ../util/plot_rate.py --rx \
        --maxy $bw \
        --xlabel 'Time (s)' \
        --ylabel 'Rate (Mbps)' \
        -i 's2-eth*' \
        -f $dir/bwm2.txt \
        -o $dir/rate.png
#    sudo python ../util/plot_tcpprobe.py \
#        -f $dir/tcp_probe.txt \
#        -o $dir/cwnd.png
		# 手动重新绘图
		# cd dasdn-Apr02-22\:45-n5-fix/
		# bw=100; sudo python ../../../util/plot_rate.py --rx         --maxy $bw         --xlabel 'Time (s)'         --ylabel 'Rate (Mbps)'         -i 's2-eth*'  -f bwm2.txt -o rate.png
done

echo "Started at" $start
echo "Ended at" `date`
echo "Output saved to $rootdir"
