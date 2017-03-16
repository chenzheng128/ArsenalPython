
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
# 收集数据
sudo ./run.sh  

# 绘图
./plot.sh results/dasdn-Mar16-23\:10/

```
