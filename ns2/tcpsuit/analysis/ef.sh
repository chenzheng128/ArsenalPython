myFile="mixed_protocol"
while read myLine
do
	perl process_ef.pl data3/$myLine fcompb1 > file1
	perl process_ef.pl data3/$myLine fcompb2 > file2
	paste file1 file2 > file3
	rm -rf file1 file2
	mv file3 $myLine.dat
done < $myFile

awk '{print "set label \""($1)*20"%\" at "($4)+0.01","($2)+0.01}' *reno.dat > test

echo "set terminal png
set output 'ef.png'
set ylabel 'Utilization Ratio (G)'
set xlabel 'Throughput Ratio (L)'
set size 0.7,0.7
set x2tics ("1" 1)
set grid noxtics x2tics
set y2tics ("1" 1)
set grid noxtics y2tics" > ef_graph.gpl

cat test >> ef_graph.gpl
rm -rf test

echo "plot \
'compoundreno.dat' u 4:2 title 'compound' with linespoints 2,\
'cubicreno.dat' u 4:2 title 'cubic' with linespoints 3,\
'htcpreno.dat' u 4:2 title 'htcp' with linespoints 4,\
'wwarreno.dat' u 4:2 title 'wwar' with linespoints 5,\
'arenoreno.dat' u 4:2 title 'areno' with linespoints 6" >> ef_graph.gpl

cat links.txt | awk '{if (NR%2 != 0) print}' | awk '{print $2}' | sed "s/M.*//" | awk 'ORS=NR%100?" ":"\n"' | awk '{print "1.8",$_}' > links.dat

cat links.txt | awk '{if ((NR==1) || (NR%2 == 0)) print}' | awk '{print $2}' | sed "s/M.*//" | awk 'ORS=NR%100?" ":"\n"' | awk '{print "5",$_}' >> links.dat
