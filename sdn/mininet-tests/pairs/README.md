## Running

TODO：将试验结果参考 dasdn 存放至按日期存放的目录中

### 运行试验
```
./pair_intervals_links_debug.sh  # 测试脚本速度快
./pair_intervals_links.sh  # 普通脚本

```

### 绘图
```
绘制其他图表
 ./plot_pair_intervals.py -lrsebc results/links*.out

绘制 cpu bar 图 # 速度会慢一些
./plot_pair_intervals.py -p results/links*.out


不要绘制 iperf 图表， 会出现数据错误
'-i', '--iperf'
```
# 通过 packetcount.c 读取网络统计信息
cat /proc/stat
cat /proc/net/dev
