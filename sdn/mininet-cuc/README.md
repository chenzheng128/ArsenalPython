# CUC Mininet 实验

建立一个 QoS / tc 队列拥塞控制的实验拓扑, 用于评估测试我们的队列拥塞级联自适应控制算法. 目前完成的实验包括
- 基于 red AQM 队列的实验效果评估( 带宽时延)
- 基于 SDN 的队列管理
  + ecn_ip: 在队列拥塞时, 使用 openflow (自定义ovs-ofctl)修改 ip tos ecn 标记
  + ecn_tcp: 在队列拥塞时, 使用 openflow (自定义ovs-ofctl + 修改协议与ovs内核模块) 修改 tcp ecn flag 标记

## 实验拓扑

Mininet实验拓扑Node: 4个主机, 4个交换机的linear配置, s3-s4之间存在(50ms)延时链路.

实验拓扑图: https://www.processon.com/view/link/5752d7f1e4b0695484404d39

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


=======
## 实验拓扑
Mininet实验拓扑Node: 4个主机, 4个交换机的linear配置, s3-s4之间存在(10ms)延时链路.

实验拓扑图: https://www.processon.com/view/link/5752d7f1e4b0695484404d39


## 实验文件

拓扑代码
- `ecn_topo.py` 将topo文件变更为新的ecn拓扑文件. 节点不变. 但是增加了数据收集, ssh, ECNInf 等类封装, 更易于使用
- `ecn_ovs_helper.py`   队列状态监控与Openflow ecn_ip ecn_tcp 控制
- `ecn_qdisc_helper.py` 队列维护的快捷代码
- `ecn_result/` 结果日志

## 实验命令
```
# 启动拓扑:
 ssh -Y mininet; cd /opt/mininet/cuc;  sudo python ecn_topo.py [remote] [debug] # 是否使用remote控制器, 是否debug输出
# 启动 ryu remote 控制器
 cd /opt/ryu; PYTHONPATH=/opt/ryu/ /opt/ryu/bin/ryu-manager ryu.app.rest_qos cuc.book.qos_simple_switch_13 ryu.app.rest_conf_switch
# 监控带宽 与 flow表
 watch -n 0.2 tc -s qdisc show dev s1-eth3
 watch -n 1  ovs-ofctl dump-flows s1
# 打开wireshark 分析抓包  
 export DISPLAY="127.0.0.1:10.0" ; wireshark &
# 手工运行外部 openflow ecn_ip ecn_tcp, 而不是使用 ovs_openflow=False 开关, 便于观察日志
  /usr/bin/python /opt/mininet/cuc/ecn_ovs_helper.py ecn_ip 70000 200

# 清除多次运行后的余留 netserver 进程
 for x in `ps -ef | grep netserver | awk {'print $2'}`; do kill $x; done
# 启动自编译的 ovs 交换机
 ovs-rc-vswitchd.sh restart && ovsdb-rc.sh restart
```

## 测试用例
在 `ecn_topo.py` 拓扑中可以运行在 `ecn_test_case.py` 中的多个实验评估

* `test01_base()` no ecn 测试
* `test02_04_base_ecn_red()` ecn base 测试
* `ovs_openflow_ecn(ecn_tcp_flag=True)` ecn_tcp 测试
* `ovs_openflow_ecn(ecn_tcp_flag=False)` ecn_ip 测试
* `ecn_test_case.test11_base()` 需要使用ryu remote控制器, 测试结果记录在ecn_result/2016-06-01_ecn_openflow.txt 中, openflow的ecn参数测试, 不同队列大小. 用外部命令`ecn_ovs_helper.py start`来控制ecn标志修改.
* `ecn_test_case.test01_04_ecn_red()` enc red测试,  测试结果记录 ecn_result/2016-06-28_ecn_red.txt 中, red的ecn参数测试, 4组实验. 可以看打开red参数后, min队列值越小, 带宽利用率稍微下降, avg平均延时越小, mdev分布越稳定, 测试结果记录

测试结果    |无red ecn| 有redmimmax条件1| 条件2  | 条件3
-----------|-----|--------|-----
bw:        |9.42M|9.29M| 9.24M  | 9.37M
ping avg:  |375ms|110ms| 118ms  | 127ms
ping mdev: | 99ms|7.4ms| 10.9ms | 13.6ms

* `print_mininet_objs(net)`  # 打印 mininet 拓扑对象
* `test_diff_bw(net)`        # 设置不同带宽条件qos, 并使用 iperf测试
* `test_diff_latency(net)`   # 设置不同延时条件qos, 并使用 ping 测试



## 参数修改

```
# ecn_topo.py 拓扑中一些可修改的参数
setLogLevel("debug")  # 打开 debug 日志
ecn_qos_init(remote_controller=True)  # 使用外部 ryu remote 控制器, 支持openflow13,  qos_ecn_table=0, fw_table=1
ecn_qos_init(remote_controller=False) # 使用内置控制器
# ecn_test_case.py 中修改参数
(ovs_helper=True) 是否自动启动 ovs_helper
```


## 命令备忘

增加xterm测试终端
```
mininet>
xterm h1 h2 h3
```

qidisc维护助手 `./ecn_qdisc_helper.py` 使用助手维护延时, 带宽信息 (不必重启mn拓扑)
```
Usage: ./ecn_qdisc_helper.py help
       ./ecn_qdisc_helper.py <all|handle|class|filter|netem|red> ["port1 port2 port3"] ...
       ./ecn_qdisc_helper.py netem <TX_QUEUE_LEN> <delay> ["port1 port2 port3"] #netem 队列延时并不稳定
       ./ecn_qdisc_helper.py red [minmax] #red 队列策略
       ./ecn_qdisc_helper.py class host <rate>
       ./ecn_qdisc_helper.py class switch <rate>
       example: ./ecn_qdisc_helper.py netem 100 10.0ms ["s1-eth3 s2-eth3"] #设定默认链路队列/延时
       example: ./ecn_qdisc_helper.py netem 100 10.0ms "s3-eth2 s4-eth2" #设定特定链路队列/延时
       example: ./ecn_qdisc_helper.py red "min 60000 max 75000 avpkt 1500" #快速设定red策略
       example: ./ecn_qdisc_helper.py class host 500mbit # 设定主机高速接口带宽
       example: ./ecn_qdisc_helper.py class switch 5mbit # 设定交换低速接口带宽
```


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

旧的拓扑代码
- `hailong_local_qos.py`
     * 2016-07-08 改由 qidisc维护助手 `./qdisc_helper.py` 维护延时带宽, 取消内部延时链路, red 策略等,
     * 本地 ovs controller 控制器, 有 qos 策略.  通过设置的 QoS 策略建立哑铃带宽拓扑
     * 增加 red qdisc 策略, 支持 ecn mark 策略.
- `hailong_local_no_qos.py`  本地 ovs controller 控制器, 无 qos 策略, 便于作 tc qos 命令行设置
- `hailong_remote.orignial.py` 最初的 远程 controller 拓扑
当使用 iperf 在 h1和h3直接进行传输时应能看到拥塞情况. 具体测试方法运行 `sudo python cuc/hailong_local_qos.py` 后可查看.


如自编译ovs交换机, 应先启动自编译的ovs交换机服务
```
cd /opt/mininet/cuc
sudo ./bin/ovsdb-rc.sh #(可选) 启动自安装 ovsdb 服务
sudo ./bin/ovs-rc-vswitchd.sh #(可选) 启动自安装 ovs-vswitch服务
sudo mn -c && sudo python <your-topo>.py  #设置拓扑
```

## ovs (for ecn_tcp) 内核编译

* 参考: https://github.com/chenzheng128/ovs/tree/ecn240
* linux 内核头文件
```
 # 进入内核头文件路径
 cd /usr/src/linux-headers-`uname -r` # 3.13.0-86-generic
 # 在目录下查找相关的头文件, 复制到上级目录便于查看并添加注释
 grep "some_code" * -R
 cp <some_file>.h ../linux-header/

```
