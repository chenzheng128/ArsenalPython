
# SDN 实验相关
以 [Hailong 拓扑][1]为基础, 使用 tc 完成 queue 控制.
TODO:
1. 5m 链路条件下 合适的 queue 大小
2. 通过 ipc 控制  h1 / h2 带宽队列
  

# 收集 SDN 代码

## 收集 ryu 代码

收集命令
```
cd ~/PycharmProjects/ryu
git branch zhchen #切换至 zhchen 分支
cd PycharmProjects/
mkdir -p ArsenalPython/sdn/ryu-cuc
rsync -avv ryu/cuc/ ArsenalPython/sdn/ryu-cuc
```

## 其他代码
 
` ovsdb/ovsdb_client.py `  : [Simple Socket Client](https://fredhsu.wordpress.com/2013/10/15/ovsdb-client-in-python/)

## 单元测试 


[1]: https://www.processon.com/view/link/5752d7f1e4b0695484404d39