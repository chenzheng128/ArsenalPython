# cuc-buffer 

研究传输缓存 从 `caltech-ns2tcplinux` 架构修改而来; 原来的 `/run/test/plot-` 后缀修改为 `buffer`
初步恢复了 buffersizing 图形

## 基础环境

ubuntu 14.04 安装绘图用 gnuplot `sudo apt-get install gnuplot-x11`

MacOSX
* 设置 display `sudo ln -sf /usr/bin/open /usr/bin/display` 快速打开图片方法
* `xgraph.py` 链接指向-> `ns3/scratch/my_plot_helper.py` 我们的绘图工具, 用于取代 xgraph 以及 gnuplot
  - `ln -sf /opt/PycharmProjects/ArsenalPython/ns3/scratch/my_plot_helper.py /usr/local/bin/xgraph.py `

## 运行方法

```
# 进入 output . 可选删除某一组历史结果目录
cd output; rm -rf ../output/*-150;

# 运行程序收集数据
../run-buffer.sh

# 使用 buffersizing 绘图工具制图
cd mininet-tests/buffersizing
rootdir=/opt/ArsenalPython/ns2/cuc-buffer/output
python ./plot-results.py --dir=$rootdir
```

## 文件说明

* `run-buffer.sh` 运行脚本 
* `plot-buffer.sh` 生成汇总页面图形脚本 
* `verify/` 验证数据
  - `run-flows-vs-link.sh` 验证多流吞吐是否和链路带宽一致 
# `output\` 结果输出目录
  - `result.txt` 格式为 flowNumber packetNum packetSize

