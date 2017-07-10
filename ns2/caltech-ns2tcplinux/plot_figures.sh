#!/bin/bash

# edit this from mininet bufferbloat.sh

if [ $# -ne 1 ]
then
    echo "Usage: `basename $0` {experiment_name}"
    echo "  Examples: `basename $0` 1-100-64-900"
exit
fi

exp=$1

# python plot_queue.py --maxy 100 --miny 0 -f ${exp}_sw0-qlen.txt -o cwnd-${exp}.png >/dev/null
# python plot_tcpprobe.py -f ${exp}_tcpprobe.txt -o ${exp}_tcp_cwnd_iperf.png -p 5001 >/dev/null
# python plot_tcpprobe.py -f ${exp}_tcpprobe.txt -o ${exp}_tcp_cwnd_wget.png -p 80 --sport >/dev/null

echo "Use http://localhost:8888/ to see the figures on your browser"
echo "Figure Names"
echo "CWND : ls ${exp}-*/cwnd*.png "

rm -f ${exp}.html
touch ${exp}.html

echo "<html><head><title>FIGURES</title></head>" > ${exp}.html
echo "<body><cetner><table border=\"1\">" >> ${exp}.html
echo "<tr><th>TCP_Name </th><th> Figure</th></tr>" >> ${exp}.html

# 这里的循环应当同 run-linux.csh 保持一致, 或是将来集成到 run-linux.csh 中
for i in bic cubic highspeed htcp hybla reno scalable vegas westwood veno lp yeah illinois compound ;
do  
  echo "<tr><td>${i}</td><td><a href=\"${exp}-${i}/cwnd-${i}.png\"><img style=\"width: 512px;height: 192px;\" src=\"${exp}-${i}/cwnd-${i}.png\"/></a></td></tr>" >> ${exp}.html
done
echo "</table></center></body></html>" >> ${exp}.html

#sudo pkill -9 -f SimpleHTTPServer
python -m SimpleHTTPServer 8888
