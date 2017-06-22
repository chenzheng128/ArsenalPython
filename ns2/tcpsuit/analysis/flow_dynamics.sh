mkdir $1
mkdir $2
mv data4/$1* $1
mv data4/$2* $2
DIR="$1"
DIR2="$2"

echo "
set term png
set output \"comb_queues2.png\"
plot \"$DIR/queues_2_12.out\" using 1:3 t '$1' with lines,\
\"$DIR2/queues_2_12.out\" using 1:3 t '$2' with lines
" | gnuplot

awk 'BEGIN {sum=0}{sum+=$2; print NR,sum}' $DIR/queues_2_12.out > queue1_cum.out
awk 'BEGIN {sum=0}{sum+=$2; print NR,sum}' $DIR2/queues_2_12.out > queue2_cum.out

echo "
set term png
set output \"comb_queuescum2.png\"
plot \"queue1_cum.out\" using 1:2 t '$1' with lines,\
\"queue2_cum.out\" using 1:2 t '$2' with lines
" | gnuplot

rm \-rf queue1_cum.out
rm \-rf queue2_cum.out

echo "
set term png
set output \"comb_losses2.png\"
plot \"$DIR/queues_2_12.out\" using 1:8 t '$1' with lines,\
\"$DIR2/queues_2_12.out\" using 1:8 t '$2' with lines
" | gnuplot

echo "
set term png
set logscale y
set output \"comb_cwnd_2_0.png\"
plot [][100:10000] \"$DIR/tcp_cwnd_2_0.out\" using 1:2 t '$1' with lines,\
\"$DIR2/tcp_cwnd_2_0.out\" using 1:2 t '$2' with lines
" | gnuplot

echo "
set term png
set logscale y
set output \"comb_cwnd_2_1.png\"
plot [][100:10000] \"$DIR/tcp_cwnd_2_1.out\" using 1:2 t '$1' with lines,\
\"$DIR2/tcp_cwnd_2_1.out\" using 1:2 t '$2' with lines
" | gnuplot

echo "
set term png
set logscale y
set output \"comb_cwnd_2_2.png\"
plot [][100:10000] \"$DIR/tcp_cwnd_2_2.out\" using 1:2 t '$1' with lines,\
\"$DIR2/tcp_cwnd_2_2.out\" using 1:2 t '$2' with lines
" | gnuplot

echo "
set term png
set logscale y
set output \"comb_cwnd_2_3.png\"
plot [][100:10000] \"$DIR/tcp_cwnd_2_3.out\" using 1:2 t '$1' with lines,\
\"$DIR2/tcp_cwnd_2_3.out\" using 1:2 t '$2' with lines
" | gnuplot

echo "
set term png
set logscale y
set output \"comb_cwnd_2_4.png\"
plot [][100:10000] \"$DIR/tcp_cwnd_2_4.out\" using 1:2 t '$1' with lines,\
\"$DIR2/tcp_cwnd_2_4.out\" using 1:2 t '$2' with lines
" | gnuplot

echo "
set term png
set logscale y
set output \"comb_cwnd_2_5.png\"
plot [][100:10000] \"$DIR/tcp_cwnd_2_5.out\" using 1:2 t '$1' with lines,\
\"$DIR2/tcp_cwnd_2_5.out\" using 1:2 t '$2' with lines
" | gnuplot

echo "
set term png
set output \"comb_cwnd_2_6.png\"
plot [][100:10000] \"$DIR/tcp_cwnd_2_6.out\" using 1:2 t '$1' with lines,\
\"$DIR2/tcp_cwnd_2_6.out\" using 1:2 t '$2' with lines
" | gnuplot

echo "
set term png
set output \"comb_cwnd_2_7.png\"
plot [][100:10000] \"$DIR/tcp_cwnd_2_7.out\" using 1:2 t '$1' with lines,\
\"$DIR2/tcp_cwnd_2_7.out\" using 1:2 t '$2' with lines
" | gnuplot

echo "
set term png
set output \"comb_cwnd_2_8.png\"
plot [][100:10000] \"$DIR/tcp_cwnd_2_8.out\" using 1:2 t '$1' with lines,\
\"$DIR2/tcp_cwnd_2_8.out\" using 1:2 t '$2' with lines
" | gnuplot

echo "
set term png
set output \"comb_cwnd_2_9.png\"
plot [][100:10000] \"$DIR/tcp_cwnd_2_9.out\" using 1:2 t '$1' with lines,\
\"$DIR2/tcp_cwnd_2_9.out\" using 1:2 t '$2' with lines
" | gnuplot

echo "
set term png
set output \"comb_cwnd_2_10.png\"
plot [][100:10000] \"$DIR/tcp_cwnd_2_10.out\" using 1:2 t '$1' with lines,\
\"$DIR2/tcp_cwnd_2_10.out\" using 1:2 t '$2' with lines
" | gnuplot

echo "
set term png
set output \"comb_cwnd_2_11.png\"
plot [][100:10000] \"$DIR/tcp_cwnd_2_11.out\" using 1:2 t '$1' with lines,\
\"$DIR2/tcp_cwnd_2_11.out\" using 1:2 t '$2' with lines
" | gnuplot

echo "
set term png
set output \"comb_cwnd_2_12.png\"
plot [][100:10000] \"$DIR/tcp_cwnd_2_12.out\" using 1:2 t '$1' with lines,\
\"$DIR2/tcp_cwnd_2_12.out\" using 1:2 t '$2' with lines
" | gnuplot

echo "
set term png
set output \"comb_cwnd_2_13.png\"
plot [][100:10000] \"$DIR/tcp_cwnd_2_13.out\" using 1:2 t '$1' with lines,\
\"$DIR2/tcp_cwnd_2_13.out\" using 1:2 t '$2' with lines
" | gnuplot

echo "
set term png
set output \"comb_cwnd_2_14.png\"
plot [][100:10000] \"$DIR/tcp_cwnd_2_14.out\" using 1:2 t '$1' with lines,\
\"$DIR2/tcp_cwnd_2_14.out\" using 1:2 t '$2' with lines
" | gnuplot

echo "
set term png
set output \"comb_cwnd_2_15.png\"
plot [][100:10000] \"$DIR/tcp_cwnd_2_15.out\" using 1:2 t '$1' with lines,\
\"$DIR2/tcp_cwnd_2_15.out\" using 1:2 t '$2' with lines
" | gnuplot

echo "
set term png
set output \"comb_cwnd_2_16.png\"
plot [][100:10000] \"$DIR/tcp_cwnd_2_16.out\" using 1:2 t '$1' with lines,\
\"$DIR2/tcp_cwnd_2_16.out\" using 1:2 t '$2' with lines
" | gnuplot

echo "
set term png
set output \"comb_cwnd_2_17.png\"
plot [][100:10000] \"$DIR/tcp_cwnd_2_17.out\" using 1:2 t '$1' with lines,\
\"$DIR2/tcp_cwnd_2_17.out\" using 1:2 t '$2' with lines
" | gnuplot

echo "
set term png
set output \"comb_cwnd_2_18.png\"
plot [][100:10000] \"$DIR/tcp_cwnd_2_18.out\" using 1:2 t '$1' with lines,\
\"$DIR2/tcp_cwnd_2_18.out\" using 1:2 t '$2' with lines
" | gnuplot

echo "
set term png
set output \"comb_cwnd_2_19.png\"
plot [][100:10000] \"$DIR/tcp_cwnd_2_19.out\" using 1:2 t '$1' with lines,\
\"$DIR2/tcp_cwnd_2_19.out\" using 1:2 t '$2' with lines
" | gnuplot

echo "
set term png
set output \"comb_cwnd_2_20.png\"
plot [][100:10000] \"$DIR/tcp_cwnd_2_20.out\" using 1:2 t '$1' with lines,\
\"$DIR2/tcp_cwnd_2_20.out\" using 1:2 t '$2' with lines
" | gnuplot

echo "
set term png
set output \"comb_cwnd_2_21.png\"
plot [][100:10000] \"$DIR/tcp_cwnd_2_21.out\" using 1:2 t '$1' with lines,\
\"$DIR2/tcp_cwnd_2_21.out\" using 1:2 t '$2' with lines
" | gnuplot

echo "
set term png
set output \"comb_cwnd_2_22.png\"
plot [][100:10000] \"$DIR/tcp_cwnd_2_22.out\" using 1:2 t '$1' with lines,\
\"$DIR2/tcp_cwnd_2_22.out\" using 1:2 t '$2' with lines
" | gnuplot

echo "
set term png
set output \"comb_cwnd_2_23.png\"
plot [][100:10000] \"$DIR/tcp_cwnd_2_23.out\" using 1:2 t '$1' with lines,\
\"$DIR2/tcp_cwnd_2_23.out\" using 1:2 t '$2' with lines
" | gnuplot

echo "
set term png
set output \"comb_cwnd_2_24.png\"
plot [][100:10000] \"$DIR/tcp_cwnd_2_24.out\" using 1:2 t '$1' with lines,\
\"$DIR2/tcp_cwnd_2_24.out\" using 1:2 t '$2' with lines
" | gnuplot

echo "
set term png
set output \"comb_cwnd_2_25.png\"
plot [][100:10000] \"$DIR/tcp_cwnd_2_25.out\" using 1:2 t '$1' with lines,\
\"$DIR2/tcp_cwnd_2_25.out\" using 1:2 t '$2' with lines
" | gnuplot

echo "
set term png
set output \"comb_cwnd_2_26.png\"
plot [][100:10000] \"$DIR/tcp_cwnd_2_26.out\" using 1:2 t '$1' with lines,\
\"$DIR2/tcp_cwnd_2_26.out\" using 1:2 t '$2' with lines
" | gnuplot

echo "
set term png
set output \"comb_cwnd_2_27.png\"
plot [][100:10000] \"$DIR/tcp_cwnd_2_27.out\" using 1:2 t '$1' with lines,\
\"$DIR2/tcp_cwnd_2_27.out\" using 1:2 t '$2' with lines
" | gnuplot

echo "
set term png
set output \"comb_cwnd_2_28.png\"
plot [][100:10000] \"$DIR/tcp_cwnd_2_28.out\" using 1:2 t '$1' with lines,\
\"$DIR2/tcp_cwnd_2_28.out\" using 1:2 t '$2' with lines
" | gnuplot

echo "
set term png
set output \"comb_cwnd_2_29.png\"
plot [][100:10000] \"$DIR/tcp_cwnd_2_29.out\" using 1:2 t '$1' with lines,\
\"$DIR2/tcp_cwnd_2_29.out\" using 1:2 t '$2' with lines
" | gnuplot
