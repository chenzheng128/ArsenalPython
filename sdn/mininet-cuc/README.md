# CUC Mininet 实验

## 准备

将 sdn mininet 代码链接至 $MININET_HOME/cuc 目录
```
MININET_HOME=/opt/mininet
cd $MININET_HOME
ln -sf /opt/sdn/mininet-cuc/ cuc
```

## 实验拓扑

拓扑图: https://www.processon.com/view/link/5752d7f1e4b0695484404d39

- `hailong_remote.orignial.py` 最初的 远程 controller 拓扑
- `hailong_local_no_qos.py`  本地 ovs controller 控制器, 无 qos 策略, 便于作 tc qos 命令行设置
- `hailong_local_qos.py`     本地 ovs controller 控制器, 有 qos 策略.  通过设置的 QoS 策略 (4mqos, 5mqos), 
当使用 iperf 在 h1和h3直接进行传输时应能看到拥塞情况. 具体测试方法运行 `sudo python cuc/hailong_local_qos.py` 后可查看.   
 

```
cd /opt/mininet
sudo ./bin/ovsdb-rc.sh #(可选) 启动自安装 ovsdb 服务
sudo ./bin/ovs-rc-vswitchd.sh #(可选) 启动自安装 ovs-vswitch服务
sudo mn -c && sudo python cuc/hailong_topo_local_controller.py  #设置拓扑
```
