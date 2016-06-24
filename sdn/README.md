

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
