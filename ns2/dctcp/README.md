## DcCubic

Source: Original from https://github.com/chenleiming/DcCubic

## DCTCP
在ns2.35版本中仿真DCTCP ,仿真脚本文件：dctcp-dumbbell.tcl

### 环境与补丁准备
    先把DCTCP加入ns2。 把文件dctcp.patch 放在 ns-allinone-2.35/ns-2.35 目录下 ，
    进入 ns-allinone-2.35/ns-2.35 目录,执行命令：`patch -p1 --ignore-whitespace -i dctcp.patch`
    然后 make ,即可安装好DCTCP.

### 运行

    `cd output` 目录

    运行脚本命令： output$ `ns ../dctcp-dumbbell.tcl` ， 成功运行后产生cwnd 数据文件和图像。      

## CUBIC
在ns2.35版本中仿真TCP Cubic，获得cwnd数据和图像，仿真脚本文件：cubic-2flows-dumbbell.tcl

    在 ns-allinone-2.35 目录下，执行命令：mkdir output ，新建文件夹output

    进入output文件夹的命令: cd output，便于将数据文件生成在 output 目录中

    运行脚本命令：output$ ns ../cubic-2flows-dumbbell.tcl

    tcl文件中已经加入画图语句，运行后可直接显示cwnd图像
         （生成的cwnd数据存在 cwnd_1_cubic.tr 等文件中，也可通过 xgraph 画图工具画图，命令：xgraph cwnd_1_cubic.tr ）
    ns2中安装 xgraph 命令：apt-get install xgraph



#3 tcp_cubic.c 文件是ns2中的cubic源文件 ，目录为：ns-allinone-2.35/ns-2.35/tcp/linux/src/

#4 tcp_cubic-linux2.6.22.6.c 是Linux-2.6.22.6内核中的cubic 源文件 ，目录为： linux-2.6.22.6/net/ipv4/
