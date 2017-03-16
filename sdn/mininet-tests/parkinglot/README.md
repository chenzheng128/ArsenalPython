
##required
* termcolor
 # 输出命令时可显示队列颜色

 pip install termcolor  
* ../util
 git clone https://github.com/mininet/mininet-util.git ../util
*  bwm-ng  # 带宽监测
git clone https://github.com/vgropp/bwm-ng.git
cd bwm-ng/
./autogen.sh && make && sudo make install


## Running

sudo ./parkinglot-sweep.sh
