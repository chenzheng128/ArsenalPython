# buffersizing-red

参考 buffersizng 修改, 对 red 队列进行测试

## 文件说明

* `.gitignore` 忽略 result 目录;
* `plot-results.py ` 绘图程序完成3组数值
  - 数值1: 公式计算
  - 数值2: 公式计算
  - 数值3: `result-buffersizing-xxx` 目录下的 result.txt
  - 平均计算方法: 如运行多轮 -r1 -r2 -r3 , 则将数据放入 list [r1, r2, r3] 中, 然后取平均值

## 运行方法

1. `build-patched-iperf.sh` 在 $HOME 路径下安装 patched iperf.
1. `sudo service openvswitch-switch start` 启动 ovs 交换机
1. `sudo ./buffersizing-sweep.sh` 运行脚本; 在对应的 `result-buffersizing-xxx` trace 目录下生成了 `result.png`
    2. 增加 `buffersizing.py` 参数 `--red` 以使用 red 进行AQM 队列管理
1. 如果绘图执行失败. 可以 `$rootdir` 重新执行绘图程序

