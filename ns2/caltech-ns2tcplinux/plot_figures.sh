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


field=2
# 需要按 result0 文件的 field 顺序排列 cwnd rate ack, 便于 xgraph.py 绘图
# for x in cwnd rate ack; do
for x in cwnd rate; do
  outfile="${exp}-${x}.html"
  echo "  outfile :  ${outfile} "
  rm -f ${outfile}
  touch ${outfile}
  echo "<html><head><title>FIGURES</title></head>" > ${outfile}
  echo "<body><ceter><h2>${exp} ${x}</h2><table border=\"1\">" >> ${outfile}
  echo "<tr><th>TCP_Name </th><th> Figure</th></tr>" >> ${outfile}

  # 这里的循环应当同 run-linux.csh 保持一致, 或是将来集成到 run-linux.csh 中
  for i in bic cubic highspeed htcp hybla reno scalable vegas westwood veno lp yeah illinois compound cong;
  do
    echo cd ${exp}-${i}
    cd ${exp}-${i}
    #xgraph.py -l cwnd-${i} -f 1:2result0
    #xgraph.py -l ack-${i} -f 1:3 result0
    #xgraph.py -l rate-${i} -f 1:4 result0    
    # 这句循环后的结果和上面3句一样
    echo xgraph.py -l ${x}-${i} -f 1:${field} result0
    # 使用 xgraph.py 绘图, 而不是 run-linux.sh 中的 gnuplot
    # xgraph.py -l ${x}-${i} -f 1:${field} result0
    
    # xgraph.py -l grate-${i} rate0 # 需要在  run-linux.sh 激活使用 awk语句计算出 rate0
    cd ..
    echo "<tr><td>${i}</td><td><a href=\"${exp}-${i}/${x}-${i}.png\"><img style=\"width: 512px;height: 192px;\" src=\"${exp}-${i}/${x}-${i}.png\"/></a></td></tr>" >> ${outfile}
  done
  echo "</table></center></body></html>" >> ${outfile}
  
  field=$(($field+1))

done

netstat -nat | grep 8888
if [[ $? -eq 0 ]] ; then
  echo "8888 端口已经存在服务"
else
  #sudo pkill -9 -f SimpleHTTPServer
  python -m SimpleHTTPServer 8888 & 
fi
