#!/bin/bash

# 绘制 html 列表图形

# edit this from mininet bufferbloat.sh

if [ $# -ne 2 ]
then
    echo "Usage: `basename $0` \$rootdir {experiment_name}"
    echo "  Examples: `basename $0` \$rootdir/data980 43.5-480-reno"
    echo "     Debug: `basename $0` \$rootdir/data999 43.5-480-reno"  # 调试数据
exit
fi

dir=$1
exp=$2

cd $dir

echo "Figure Names"

field=2
# 需要按 result0 文件的 field 顺序排列 cwnd rate ack, 便于 xgraph.py 绘图
# for x in cwnd rate ack; do
for x in queue0-size util0; do
  outfile="${exp}-${x}.html"
  echo "  outfile :  ${outfile} "
  rm -f ${outfile}
  touch ${outfile}
  echo "<html><head><title>FIGURES</title></head>" > ${outfile}
  echo "<body><ceter><h2>${exp} ${x}</h2><table border=\"1\">" >> ${outfile}
  echo "<tr><th> foldername </th><th> Figure</th></tr>" >> ${outfile}

  # 这里的循环应当同 output 目录下 保持一致
  for i in `ls -d1 ${dir}/*${exp}`;
  do
    # $i 绝对路径 /opt/ArsenalPython/ns2/cuc-buffer/output/data980/980-80-100-43.5-480-reno
    # $foldername 相对路径 980-80-100-43.5-480-reno
    foldername=`basename ${i}`
    figname=${x}
    
    if ! [[ -d  ${i} ]] ; then
      echo "ERROR: 目录 ${i} 不存在, 请检查参数 ..."
    else 
      echo cd ${i}
      cd ${i}
      #xgraph.py -l cwnd-${i} -f 1:2result0
      #xgraph.py -l ack-${i} -f 1:3 result0
      #xgraph.py -l rate-${i} -f 1:4 result0    
      # 这句循环后的结果和上面3句一样
      # echo xgraph.py -l ${figname}  -f 1:${field} result0
      # 在这里使用 xgraph.py 绘图, 而不是 在 run-linux.sh 中
      # xgraph.py -l ${figname} -f 1:${field} result0
      
      # xgraph.py -l grate-${i} rate0 # 需要在  run-linux.sh 激活使用 awk语句计算出 rate0
      cd ..
      echo "<tr><td>${foldername}</td><td><a href=\"${foldername}/${figname}.png\"><img style=\"width: 512px;height: 192px;\" src=\"${foldername}/${figname}.png\"/></a></td></tr>" >> ${outfile}
    fi
  done
  
  echo "</table></center></body></html>" >> ${outfile}
  echo 
  echo "在 $dir 生成了 ${outfile} 文件 ..."
  
  field=$(($field+1))

done

LISTEN=8890
netstat -nat | grep ${LISTEN} | grep LISTEN
if [[ $? -eq 0 ]] ; then
  echo "${LISTEN} 端口已经存在服务"
else
  #sudo pkill -9 -f SimpleHTTPServer
  echo python -m SimpleHTTPServer ${LISTEN}
  echo "请使用上面的python命令启动Server. "
fi

echo "Use http://localhost:${LISTEN}/ to see the figures on your browser"
