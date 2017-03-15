# CS244 Programming Assignment 1: Bufferbloat
Source: https://web.stanford.edu/class/cs244/pa1.html

更多实验结果记录在  Evernote "CS244 PA1  Bufferbloat Programming Assignment 1" 中

## 安装依赖包
sudo apt-get -y install screen
sudo apt-get -y install python-matplotlib

## 相关文件

* `bufferbloat.py` 创建拓扑,记录数据 Creates the topology, measures cwnd, queue sizes and RTTs and spawns a webserver.
* `plot_queue.py` Plots the queue occupancy at the bottleneck router
* `plot_ping.py` Parses and plots the RTT reported by ping
* `plot_tcpprobe.py` Plots the cwnd time-series for a flow specified by its destination port
* `run.sh` 运行所有实验并绘图 Runs the experiment and generates all graphs in one go.

## 运行实验
### 100pkt
sudo ./run.sh
sudo python exp_monitor.py --exp out/100pkt
./plot_figures.sh out/100pkt

### 20pkt
sudo ./run-minq.sh
sudo python exp_monitor.py --exp out/20pkt
./plot_figures.sh out/20pkt

http://192.168.57.4:8888/
