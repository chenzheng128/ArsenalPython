# CUC Mininet 实验

## 准备

将 sdn mininet 代码链接至 $MININET_HOME/cuc 目录
```
MININET_HOME=/opt/mininet
cd $MININET_HOME
ln -sf /opt/sdn/mininet-cuc/ cuc
sudo python cuc/hailong_local_qos.py
```

## 实验拓扑

拓扑图: https://www.processon.com/view/link/5752d7f1e4b0695484404d39

- `hailong_local_qos.py` 本地 ovs，追加qos策略
- `hailong_topo_local_controller.py` 本地ovs controller 拓扑, 作本地测试用
- `hailong_topo.py` 远程 controller 拓扑,


```
cd /opt/mininet
sudo ./bin/ovsdb-rc.sh #(可选) 启动自安装 ovsdb 服务
sudo ./bin/ovs-rc-vswitchd.sh #(可选) 启动自安装 ovs-vswitch服务
sudo mn -c && sudo python cuc/hailong_topo_local_controller.py  #设置拓扑
```
