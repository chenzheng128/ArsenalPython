# CUC Mininet 实验

建立一个 QoS / tc 队列拥塞控制的实验拓扑, 用于评估测试我们的队列拥塞级联自适应控制算法.   

算法TODO
- 5m 链路下的队列大小设置, 计算方法?
- 依据评估出的tc控制算法效率/延时级别(us? ms?), 考虑拥塞级联自适应控制算法的基本框架. 

实现TODO 
- Python: 目前仅在交换机端口上作了 tc 策略. 需要在 host 主机 eth0 网卡上启动后自动配置 tc 策略. 考虑用 h1.sendCmd() 或 ssh 命令完成.
- C: 测试 tc 效率(命令行/直接访问), 测试 unix socket C/S效率, 控制tc队列时的延时级别(us? ms?).
- C: 编译 tc 命令, 研究 tc 命令获取 queue (p) 等大小方法
- C: tc控制短发效率评估, 建立 Host/Switch unix socket server, 监控节点(外部/ovs交换机内部)可向上级网卡通告拥塞状况, 或调节上级发送效率.
 

## 准备

自定义 hosts 文件, 便于在xterm终端中直接使用 `ping h1` 或 `iperf -c h3` 进行测试. 
```
vi /etc/hosts
10.0.0.1 h1
10.0.0.2 h2
10.0.0.3 h3
10.0.0.4 h4
```

将 sdn mininet 代码链接至 $MININET_HOME/cuc 目录
```
MININET_HOME=/opt/mininet
cd $MININET_HOME
ln -sf /opt/sdn/mininet-cuc/ cuc
```

## 实验拓扑

启动拓扑: `ssh -X mininet sudo python /opt/mininet/cuc/hailong_local_qos.py`

增加xterm测试终端
```
mininet>
xterm h1
xterm h1
xterm h1
xterm h3
xterm h3
xterm h2
xterm h4
xterm s2
```

Mininet实验拓扑Node: 4个主机, 4个交换机的linear配置, s3-s4之间存在(10ms)延时链路.

实验拓扑图: https://www.processon.com/view/link/5752d7f1e4b0695484404d39


拓扑代码
- `hailong_local_qos.py`     本地 ovs controller 控制器, 有 qos 策略.  通过设置的 QoS 策略 (4mqos, 5mqos),
- `hailong_local_no_qos.py`  本地 ovs controller 控制器, 无 qos 策略, 便于作 tc qos 命令行设置
- `hailong_remote.orignial.py` 最初的 远程 controller 拓扑
当使用 iperf 在 h1和h3直接进行传输时应能看到拥塞情况. 具体测试方法运行 `sudo python cuc/hailong_local_qos.py` 后可查看.

## qos 策略
tc 默认在网卡出(out)的地方进行控制. 然而在ovs交换机内部传输流量时(即使是out, 如 s1-eth1/s2-eth1 流量经过 s2-eth1 到 s2-eth2), 
也不会产生包统计与队列操作,  无流量记录信息, tc策略无法生效.  ( TODO: 为增加控制级别, 可考虑在 s2-eth2 最近的一个上级口 s4-eth2 追加 tc 策略.)  
因此, 在拓扑中支持 tc 策略的网卡拥塞自适应级联控制应为:  
- h1<->h3: h3-eth0 -> s2-eth2 -> (s4-eth2) -> s1-eth3 -> h1-eth0
- h2<->h4: h4-eth0 -> s2-eth3 -> (s4-eth2) -> s1-eth3 -> h2-eth0

目前所有的网卡策略尽量保持一致
- 设定3个class, 对应3个 pfifo handle, 可调整队列n大小(limit n) (不要用sfq, 不容易通过 icmp 测试延时)
- filter策略( tc filter )如下
    * 将 5001 5002 5003 对于到不同的3个队列pfifo handle
    * 将 h1(10.0.0.1) 所有流量映射到队列2 
    * 将 icmp 所有流量映射到队列2
这样通过h1 <-> h3 5002 之间的 udp iperf 流量测试, 以及 h1 ping h3 之间测试可以看出流量拥塞对于延时的影响.


## 补充备忘

如自编译ovs交换机, 应先启动自编译的ovs交换机服务
```
cd /opt/mininet
sudo ./bin/ovsdb-rc.sh #(可选) 启动自安装 ovsdb 服务
sudo ./bin/ovs-rc-vswitchd.sh #(可选) 启动自安装 ovs-vswitch服务
sudo mn -c && sudo python cuc/hailong_topo_local_controller.py  #设置拓扑
```
