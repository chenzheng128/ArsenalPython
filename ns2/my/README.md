
我的 ns-2 代码

## 基础环境

Linux & MacOSX
* `xgraph.py` 链接指向-> `ns3/scratch/my_plot_helper.py` 我们的绘图工具, 用于取代 xgraph 以及 gnuplot
  - `ln -sf /opt/PycharmProjects/ArsenalPython/ns3/scratch/my_plot_helper.py /usr/local/bin/xgraph.py `
* MacOSX: 设置 display `sudo ln -sf /usr/bin/open /usr/bin/display` 快速打开图片方法
  
## 运行例子
```
cd output
ns ../xxxx.tcl
```

## 代码说明
* `monitor-link-usage.tcl` 监测并修改链路带宽利用率
  - `xgraph.py -d ratefile0` 查看链路带宽变化
* `monitor-queue.tcl` 监测队列利用率