#process_dir="long_lived30"
process_dir=$1
vector="1 2 3 4 5 6 7 8 9 10 11 12"
echo "cd $process_dir"
for i in $vector
do
	echo "cp ../parsing_flowf.pl ."
	echo "cp ../parsing_flowr.pl ."
	echo "cp ../parsing_overf.pl ."
	echo "perl parsing_flowf.pl $i > seed"$i"_clusterf.dot"
	echo "perl parsing_flowr.pl $i > seed"$i"_clusterr.dot"
	echo "perl parsing_overf.pl $i > seed"$i"_overallf.dot"
	echo "dot -Tpng -o s"$i"cf.png seed"$i"_clusterf.dot"
	echo "dot -Tpng -o s"$i"cr.png seed"$i"_clusterr.dot"
	echo "dot -Tpng -o s"$i"of.png seed"$i"_overallf.dot"
done
echo "cd .."
