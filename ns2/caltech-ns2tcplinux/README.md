# caltech-ns2tcplinux

A Linux TCP implementation for NS2: http://netlab.caltech.edu/projects/ns2tcplinux/ns2linux/index.html

ubuntu 14.04 安装绘图用 gnuplot `sudo apt-get install gnuplot-x11`

* `tutorial` A mini-tutorial for TCP-Linux in NS-2 迷你指南使用 TCP-Linux, 包括
    - 新 `sack1.tcl` 代码
    - 旧 `linux.tcl` 代码
    - `linux-vegas.tcl` 定时修改参数的 tcp-vegas
    - 还包括如何引用新的 linux 内核 tcp 算法

* `run-linux.csh` 运行脚本
* `red.tcl` 拓扑脚本
* `script-gnuplot.txt` 绘图脚本