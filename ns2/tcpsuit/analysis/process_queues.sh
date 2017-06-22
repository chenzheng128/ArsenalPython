queues="0463 0469 1465 1467 2463 4630 463464 4641 465466 466468 466469 467468 4682 4690 469466" 
window="1 2 3 4 5" 

for c in $queues
do 
	echo "
	set term png
	set output \"queue_util_2_$c.png\"
plot \"reno_reno_real/data4/queues_2_$c.out\" using 1:6 t 'reno' with lines,\
\"wwar_wwar_real/data4/queues_2_$c.out\" using 1:6 t 'wwar' with lines,\
\"cubic_cubic_real/data4/queues_2_$c.out\" using 1:6 t 'cubic' with lines,\
\"compound_compound_real/data4/queues_2_$c.out\" using 1:6 t 'compound' with lines,\
\"htcp_htcp_real/data4/queues_2_$c.out\" using 1:6 t 'htcp' with lines
	" | gnuplot

	echo "
	set term png
	set output \"queue_loss_2_$c.png\"
plot \"reno_reno_real/data4/queues_2_$c.out\" using 1:8 t 'reno' with lines,\
\"wwar_wwar_real/data4/queues_2_$c.out\" using 1:8 t 'wwar' with lines,\
\"cubic_cubic_real/data4/queues_2_$c.out\" using 1:8 t 'cubic' with lines,\
\"compound_compound_real/data4/queues_2_$c.out\" using 1:8 t 'compound' with lines,\
\"htcp_htcp_real/data4/queues_2_$c.out\" using 1:8 t 'htcp' with lines
	" | gnuplot

done

for b in $window
do 
	echo "
	set term png
	set output \"cwnd_2_$b.png\"
	set logscale y
plot [1:1200][1:] \"reno_reno_real/data4/tcp_cwnd_2_$b.out\" using 1:5 t 'reno' with lines,\
\"wwar_wwar_real/data4/tcp_cwnd_2_$b.out\" using 1:5 t 'wwar' with lines,\
\"cubic_cubic_real/data4/tcp_cwnd_2_$b.out\" using 1:5 t 'cubic' with lines
	" | gnuplot
done
