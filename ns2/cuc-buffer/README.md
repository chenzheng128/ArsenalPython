# cuc-buffer 

研究传输缓存 从 `caltech-ns2tcplinux` 架构修改而来; 原来的 `/run/test/plot-` 后缀修改为 `buffer`

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
../run-buffer.sh

# 在 MacOSX 打开浏览器看生成的 cwnd / rate 图形;
../plot-buffer.sh 1-100-64-900 ; open http://localhost:8889/1-100-64-900-cwnd.html; http://localhost:8889/1-100-64-900-rate.html
```  

## 文件说明

* `run-buffer.sh` 运行脚本 
* `plot-buffer.sh` 生成汇总页面图形脚本 
* `verify/` 验证数据
  - `flows-vs-link.py` 验证多流吞吐是否和链路带宽一致 
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
