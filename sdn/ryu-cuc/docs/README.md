

# 官方文档学习参考


## 拓扑查看器
参考: http://ryu.readthedocs.io/en/latest/gui.html

在mininet中运行以下拓扑命令
```
sudo mn --controller remote,ip=192.168.57.2 --topo tree,depth=3
sudo mn --controller remote --topo tree,4
sudo mn --controller remote --topo linear,4
sudo mn --controller remote --topo single,4     #单个交换机, 4个主机
sudo mn --controller remote --topo reversed,4   #单个交换机, host-eth 接口顺序反转
sudo mn --controller remote --topo torus        #未运行成功
```
(TODO: topo view 目前不显示主机, 而且 tree 模型下面的交换机显示状态不好 )

再运行ryu命令
```
PYTHONPATH=. ./bin/ryu run --observe-links ryu/app/gui_topology/gui_topology.py
```

(TODO: 分析 run --observe-links 的代码调用路径.)  

打开浏览器 http://localhost:8080/ 效果如下:

![](http://ryu.readthedocs.io/en/latest/_images/gui.png)

## Snort 端口监听 (mininet)

建立监听拓扑 h1 h2 为通讯主机, h3为监听主机 (使用s1-eth3 口);  启动ryu控制器
```
sudo mn --controller remote --topo single,3 --switch ovs,protocols=OpenFlow13

PYTHONPATH=. ./bin/ryu-manager --log-config-file=./cuc/logging_config.ini ryu/app/simple_switch_snort.py
```

参考文档安装snort, 并进行监听; 文档涉及 `eth1` 均换为 `s1-eth3` (恰好也是代码 `self.snort_port = 3` 中使用的3号口)
```
sudo ifconfig s1-eth3 promisc #设置网卡为监听模式 ( 可通过  ifconfig s1-eth3 | grep PROM 进行检查) 
snort -i s1-eth3 -A unsock -l /tmp -c /etc/snort/snort.conf
```

在mininet执行 h1 h2 ping, 之后再 ryu 控制器页面可以看到文档中类似的icmp输出, 表明实验成功. 如果有问题, 可通过`sudo tcpdump -i s1-eth2` 命令检查数据包是否正常复制. 
```
mininet> h1 ping h2
```

`ryu/app/simple_switch_snort.py`的端口复制关键代码如下 

```python 
 #数据包除了发送到 out_port之外, 还都会复制一份送到 snort_port(id=3 即s1-eth3) 端口
 actions = [parser.OFPActionOutput(out_port),
                   parser.OFPActionOutput(self.snort_port)]

        self.logger.debug ("out_port: %s" % out_port)
```


