

# 官方文档学习参考


## 拓扑查看器
参考: http://ryu.readthedocs.io/en/latest/gui.html


运行命令
```
PYTHONPATH=. ./bin/ryu run --observe-links ryu/app/gui_topology/gui_topology.py
```

(TODO: 分析 run --observe-links 的代码调用路径.)  

打开浏览器 http://localhost:8080/ 效果如下:

![](http://ryu.readthedocs.io/en/latest/_images/gui.png)