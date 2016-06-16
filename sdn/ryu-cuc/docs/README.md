

# 官方文档学习参考

# Writing Your Ryu Application

## The First Application 简单交换机
Source: http://ryu.readthedocs.io/en/latest/writing_ryu_app.html

`l2.py` 作所有数据的FLOOD操作. 修改为 OF1.3版本

这个交换机很傻(总是FLOOD) , 到 `ryu/app` directory and `integrated tests` directory 可以找到更多资源

## Ryu application API ryu event 事件处理
Source: http://ryu.readthedocs.io/en/latest/ryu_app_api.html

`l2_events.py` 学习处理 ryu 的事件机制. 每个app是一个单线程. 通过set_ev_cls 注册相关事件进行处理.  
执行下面的命令可以触发事件EventOFPPortStateChange
```
mininet> s1 ifconfig s1-eth2 up
```
可以在不同的app中注册不同的handle, 如果都注册, 则app都会收到消息

```
#启动两个监听器app
./bin/ryu-manager --log-config-file=cuc/logging_config.ini  cuc/docs/l2.py cuc/docs/l2_events.py
# 执行命令触发以下事件与处理 mininet> h1 ping h2
(handle by l2.py) EventOFPPacketIn: <ryu.controller.ofp_event.EventOFPPacketIn object at 0x10e184310>
# 执行命令触发以下事件与处理 mininet> s1 ifconfig s1-eth2 up
(handle by l2_events.py) EventOFPPortStateChange: <ryu.controller.ofp_event.EventOFPPortStateChange object at 0x10e16fdd0>
```

## Packet library
Source: http://ryu.readthedocs.io/en/latest/library_packet.html

`l2_lib_packet.py` 打印数据包结构, build 数据包, tcp包

## BGP speaker library
使用 `eventlet.monkey_patch()` 绿色线程打猴子补丁. 参考: Python——eventlet http://www.cnblogs.com/Security-Darren/p/4170031.html

## OVSDB Manager library
`ovsdb.py` 这个代码没有运行通过, 不是一个正确运行的代码


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


