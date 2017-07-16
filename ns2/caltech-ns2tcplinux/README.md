# caltech-ns2tcplinux

A Linux TCP implementation for NS2: http://netlab.caltech.edu/projects/ns2tcplinux/ns2linux/index.html

在 ubuntu 14.04 (ns-2.35)下复原了 14 个tcp 算法的 cwnd "14 different congestion control algorithms from Linux-2.6.22.6, as listed in the following table. "

单流环境下的 cwnd 窗口 / rate 速率实验与图表

备注:
1. 除了 lp 图形不太一致, vegas 缺少一个小峰外, 其他算法的图形都是一致的.
1. 通过查看 ns 源代码目录 `find . -name tcp_cubic.c`, 增加了 `cong` 算法，图形增加到 15 个。
1. 基于[ns2 dctcp版本](https://github.com/chenzheng128/ns-allinone-2.35/releases) 对ns2tcplinux代码进行了测试，输出结果一致。说明 dctcp 代码的集成对原有的 Agent/TCP/Linux 没有影响


## 基础环境

ubuntu 14.04 安装绘图用 gnuplot `sudo apt-get install gnuplot-x11`

MacOSX
* 设置 display `sudo ln -sf /usr/bin/open /usr/bin/display` 快速打开图片方法
* `xgraph.py` 链接指向-> `ns3/scratch/my_plot_helper.py` 我们的绘图工具, 用于取代 xgraph 以及 gnuplot
  - `ln -sf /opt/PycharmProjects/ArsenalPython/ns3/scratch/my_plot_helper.py /usr/local/bin/xgraph.py `

## 运行方法

```
以某一组 (例如 1-100-64-900) 实验参数为例

# 进入 output . 可选删除某一组(例如 1-100-64-900)历史结果目录
cd output; rm -rf ../output/1-100-64-900-*;
# 运行程序收集数据
../run-linux.sh

# 在 MacOSX 打开浏览器看生成的 cwnd / rate 图形;
../plot_figures.sh 1-100-64-900 ; open http://localhost:8888/1-100-64-900-cwnd.html; http://localhost:8888/1-100-64-900-rate.html
```  

## 文件说明

* `run-linux.sh` 运行脚本 (由`run-linux.csh`重命名而来), 其中的tcp 算法包括 bic cubic highspeed htcp hybla reno scalable vegas westwood veno lp yeah illinois compound  14 种算法; 考虑再追加上 dctcp
* `plot_figures.sh` 生成汇总页面图形脚本 
* `script-gnuplot.txt` 单独绘图脚本; 可改为使用 `plot_figures.sh` 中的 `xgraph.py`
* `red.tcl` 拓扑脚本 (用途?) 暂时没用到
# `output\` 结果输出目录
  - `result0` result0 格式为 $nowtime $cwnd $rate $ack; `column -t result0` 格式化 result0 更便于查看 
  - ~~`output/rate0` rate0 格式为 $nowtime $rate; 在 run-linux.sh 中使用 awk 从 result0 中的 ack 生成~~ 改为在tcl 中计算至 result0 中

* `tutorial\` A mini-tutorial for TCP-Linux in NS-2 迷你指南使用 TCP-Linux, 包括
    - 新 `sack1.tcl` 代码
    - 旧 `linux.tcl` 代码
    - `linux-vegas.tcl` 定时修改参数的 tcp-vegas
    - 还包括如何引用新的 linux 内核 tcp 算法
    
    
## 旧命令备忘
使用 awk 通过 result0 中的 ack 计算速率; 
```
cat result0 | awk 'BEGIN{old=0}{print $1, ($3-old)*1448*8*2}{old=$3}' > rate0
```



按栏拆分数据
```
cat result0 | cut -d" " -f 1,3 > result0-ack
cat result0 | cut -d" " -f 1,4 > result0-bw
```
