#!/bin/bash

# Exit on any failure
#set -e

# Check for uninitialized variables
set -o nounset

ctrlc() {
	killall -9 python
	mn -c
	exit
}

trap ctrlc SIGINT

# 禁用 tracing. 不支持 ubuntu 14.40
#source ../tracing/trace.sh
#trace_init

start=`date`
exptid=`date +%b%d-%H-%M`

#rootdir=results/output/buffersizing-$exptid
rootdir=result-buffersizing-$exptid

plotpath=../util
iperf=~/iperf-patched/src/iperf

iface=s0-eth1

# 3 组时间总计约 45 分钟
for run in 1 2 3; do
# 1 组时间小计约 15 分钟, 
# for run in 1; do
	#for flows_per_host in 1 2 5 10 20 30 40 50 75 100 125 150 175 200 225 250 275 300 325 350 375 400; do
	#for flows_per_host in 1; do

	# orignal 
	# for flows_per_host in 1 2 5 10 50 100 200 300 400; do
	# 在 mininet 虚拟机上, 平均 2 分钟一组, 小计约15分钟
	# for flows_per_host in 1 2; do
	#for flows_per_host in 1 2 5 10 50 100 200 300 400; do
	# 参考 buffering-red 的流设置
	for flows_per_host in 10 25 50 100 200; do
	  	dir=$rootdir/nf$flows_per_host-r$run
	  	mkdir -p $dir

	    #trace_start $dir/mntrace

	    # 增加 PYTHONPATH , 修改 buffersizing.py 中的 add_link 方法等
	    # net.stop() 不能正常退出, 因此需要下面这句
		
		PYTHONPATH=/opt/mininet/ mn -c  # 每次运行前 clean 一下
	  	
		PYTHONPATH=/opt/mininet/ python buffersizing.py --bw-host 1000 \
			--bw-net 62.5 \
			--delay 43.5 \
			--dir $dir \
			--nflows $flows_per_host \
			-n 3 \
			--iperf $iperf

		# disable tracing 没用到
	    #trace_stop $dir/mntrace
	    #grep mn_ $dir/mntrace >  $dir/mntrace_trimmed


		# was:		--use-bridge

		python $plotpath/plot_queue.py -f $dir/qlen_$iface.txt -o $dir/q.png
		#python $plotpath/plot_tcpprobe.py -f $dir/tcp_probe.txt -o $dir/cwnd.png --histogram
	done
done

cat $rootdir/*/result.txt | sort -n -k 1
# cd results
python plot-results.py --dir $rootdir -o $rootdir/result.png
echo "Started at" $start
echo "Ended at" `date`
