# udping
在不同节点的数量（CPU 利用率）下，绘制udping 的 box 与 bar 图

## required
../cpuiso make

../lib  

## run
```
make
./run_udpong.sh
export DISPLAY=127.0.0.1:10.0

./plot_udpong.sh     # 绘制 bar 图
./plot_udpong_box.sh # 绘制 box 图

# 绘图样例可参考搜索 evernotes "mininet-tests"
```
