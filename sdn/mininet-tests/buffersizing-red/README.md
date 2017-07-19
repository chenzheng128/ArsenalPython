# buffersizing-red

参考 buffersizng 修改, 使用 red 进行队列管理

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
1. `gen.sh` 执行绘图程序, 生成相关数据图表

## 调试方法

`buffersizing.py` 激活 `--cli` , `--simu_rate` 命令行参数便于调试 red 队列
```
 # 初始化 red 队列 最小值为 limit 12000 ;
sudo tc qdisc del dev s0-eth1 parent 5:1; sudo tc qdisc add dev s0-eth1 parent 5:1 handle 10: red limit 12000 avpkt 1000
# 监看队列的配置效果
 watch -n 1 tc -s qdisc show dev s0-eth1
# 效果如下 max= limit /4; min = max /3 ; min = limit/12 因为 min 至少要大于 1个 avpkt, 所以 limit 应设置为 avpkt 的12倍
qdisc red 10: parent 5:1 limit 12000b min 1000b max 3000b
```