if [ $# -ne 1 ]
then
    echo "Usage: `basename $0` {experiment_name}"
    echo "  Examples: `basename $0` 100-64-900-cubic"
    echo "     Debug: `basename $0` 150-64-60-cubic"  # 调试数据
exit
fi

exp=$1
for flownum in 5 2 1; do
  
  foldername=${flownum}-${exp}
  
  if ! [[ -d  ${foldername} ]] ; then
    echo "ERROR: 目录 ${foldername} 不存在, 请检查参数 ..."
  else 
    
    # 在终端显示 
    #../verify/flows-vs-link.py --dir 5-150-64-60-cubic/ | column -t 
    
    # 输出 rate0-flows
    ../verify/flows-vs-link.py --out rate0-flows --dir ${foldername}/ 
    cd ${foldername}
     rm -f rate*.png
     echo "*** 验证显示 ${flownum}条流 的带宽图形"
     xgraph.py -m rate*
    cd ..
  fi
done