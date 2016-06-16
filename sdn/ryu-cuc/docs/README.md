

# 官方文档学习参考

## 简单交换机
`l2.py` 作所有数据的FLOOD操作. 修改为 OF1.3版本

## 拓扑查看器
参考: http://ryu.readthedocs.io/en/latest/gui.html

在mininet中运行
```
sudo mn --controller remote,ip=192.168.57.2 --topo tree,depth=3
```

再运行ryu命令
```
PYTHONPATH=. ./bin/ryu run --observe-links ryu/app/gui_topology/gui_topology.py
```

(TODO: 分析 run --observe-links 的代码调用路径.)  

打开浏览器 http://localhost:8080/ 效果如下:

![](http://ryu.readthedocs.io/en/latest/_images/gui.png)