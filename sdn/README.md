

# 收集 SDN 代码

## 收集 ryu 代码

收集命令
```
cd PycharmProjects/ryu
git branch zhchen #切换至 zhchen 分支
cd PycharmProjects/
mkdir -p ArsenalPython/sdn/ryu-cuc
rsync -avv ryu/cuc/ ArsenalPython/sdn/ryu-cuc
```
