
##Required
* termcolor # 输出命令时可显示队列颜色
```
 pip install termcolor
```
* ../util
```
 git clone https://github.com/mininet/mininet-util.git ../util
```
*  bwm-ng  # 带宽监测
```
git clone https://github.com/vgropp/bwm-ng.git
cd bwm-ng/
./autogen.sh && make && sudo make install
```

## Running

```

sudo ./run.sh       # 运行5个节点完整实验（时间较长），收集数据，绘图
sudo ./run-debug.sh # 运行2个节点部分实验（时间短），进入 CLI，自定义收集数据，绘图

线程 monitor_thread_switch_bw() 在 [10, 20] 将调整带宽从 50m 到 100m , 然后恢复

# 绘图结果
./results/dasdn-Mar16-23\:10/rate.png



```
