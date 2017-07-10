# caltech-ns2tcplinux

A Linux TCP implementation for NS2: http://netlab.caltech.edu/projects/ns2tcplinux/ns2linux/index.html

在 ubuntu 14.04 (ns-2.35)下复原了 14 个tcp 算法的 cwnd "14 different congestion control algorithms from Linux-2.6.22.6, as listed in the following table. "

备注: 除了 lp 图形不太一致, vegas 缺少一个小峰外, 其他算法的图形都是一致的.

## 基础环境

ubuntu 14.04 安装绘图用 gnuplot `sudo apt-get install gnuplot-x11`

## 运行方法

```
以某一组 (例如 1-100-64-900) 实验参数为例

# 进入 output . 可选删除某一组(例如 1-100-64-900)历史结果目录
cd output; rm -rf ../output/1-100-64-900-*; 
# 运行程序收集数据
../run-linux.sh 
  
# 在 MacOSX 打开浏览器看生成的 cwnd 图形; 
../plot_figures.sh 1-100-64-900 & open http://localhost:8888/1-100-64-900.html
```  

生成cwnd.png代码已经集成到 `run-linux.sh` 中, 可以不运行下面的代码
```
  # 在 MacOSX 下使用 gnuplot 生成的 cwnd 图形;
  for x in `ls -1d 1-100-64-900-*`; do cd $x; gnuplot ../../script-gnuplot.txt; ALG=`head -n2 ./config | tail -n1`; mv cwnd.png cwnd-$ALG.png; open cwnd-$ALG.png; cd .. ; done
```

## 文件说明

* `run-linux.sh` 运行脚本 (由`run-linux.csh`重命名而来), 其中的tcp 算法包括 bic cubic highspeed htcp hybla reno scalable vegas westwood veno lp yeah illinois compound  14 种算法; 考虑再追加上 dctcp
* `plot_figures.sh` 生成汇总页面图形脚本
* `script-gnuplot.txt` 单独绘图脚本
* `red.tcl` 拓扑脚本 (用途?)
# `output\` 结果输出目录

* `tutorial\` A mini-tutorial for TCP-Linux in NS-2 迷你指南使用 TCP-Linux, 包括
    - 新 `sack1.tcl` 代码
    - 旧 `linux.tcl` 代码
    - `linux-vegas.tcl` 定时修改参数的 tcp-vegas
    - 还包括如何引用新的 linux 内核 tcp 算法