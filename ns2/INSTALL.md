
# 从源代码安装 ns2

### 补丁安装

TODO： 未成功， 产生了.rej文件
```
####
# 安装 dctcp 补丁
patch -p1  < ../dctcp.patch
# 还原 dctcp 补丁
patch -p1 -R  < ../dctcp.patch
```

### 基础安装

ubuntu 14.04 ns-2.35

#### 设定环境目录

```
### C.1 设定目录
NS2_SRC_HOME=/opt/coding/ns-allinone-2.35-github
DST_DIR=~/PycharmProjects/ArsenalPython/ns2
```
#### 收集代码

```
### C.2 collect 收集代码
cd $NS2_SRC_HOME
cp .gitignore $DST_DIR/gitignore
cp ns-2.35/linkstate/ls.h  $DST_DIR/ls.h
```

#### 重新发布并编译
```
### P.1 重新发布 ， 初始化 2.35 源代码

cd $NS2_SRC_HOME
# 重新初始化分支
git branch -n master-20170715
# 在 github 撤销所有提交
# 删除所有代码
rm -rf ../ns-allinone-2.35-github/*
# 复制所有原始代码
cp -r ../ns-allinone-2.35-orig/* .
cp $DST_DIR/gitignore .gitignore

# 重新提交
git commit -m "init with .gitignore"

### P.2  修复 ubutu 14.04 补丁，并编译安装
cp $DST_DIR/ls.h ns-2.35/linkstate/ls.h
# 修复decomp链接
ln -sf /usr/share/automake-1.14/depcomp xgraph-12.2/depcomp

git commit -am "ubuntu14.04 patched"


# 删除旧的ns程序
sudo rm -rf /usr/local/bin/ns
sudo rm -rf /usr/local/bin/nam
# 重新安装
sudo ./install

# 检查安装
which ns; which nam;
# 测试
cd ns-2.35; ./validate

# 提交 ubuntu 14.04 下编译出的一些文件
git commit -am "ubuntu14.04 builded"
```

#### 设定PATH等环境变量
```
### NS2 ENV SETTING START ###
# LD_LIBRARY_PATH
NS2_ALL_HOME=/opt/coding/ns-allinone-2.35
OTCL_LIB=$NS2_ALL_HOME/otcl-1.14
NS2_LIB=$NS2_ALL_HOME/lib
X11_LIB=/usr/X11R6/lib
USR_LOCAL_LIB=/usr/local/lib
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$OTCL_LIB:$NS2_LIB:$X11_LIB:$USR_LOCAL_LIB
# TCL_LIBRARY
TCL_LIB=$NS2_ALL_HOME/tcl8.5.10/library
USR_LIB=/usr/lib
export TCL_LIBRARY=$TCL_LIB:$USR_LIB
# PATH
XGRAPH=$NS2_ALL_HOME/bin:$NS2_ALL_HOME/tcl8.5.10/unix:$NS2_ALL_HOME/tk8.5.10/unix
#the above two lines beginning from xgraph and ending with unix should come on the same line
NS=$NS2_ALL_HOME/ns-2.35/
NAM=$NS2_ALL_HOME/nam-1.15/
PATH=$PATH:$XGRAPH:$NS:$NAM
### NS2 ENV SETTING END ###
````
