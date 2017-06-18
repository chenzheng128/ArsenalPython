# ns tutorial

Source: https://www.isi.edu/nsnam/ns/tutorial/

* IV. The first Tcl script 
    - `ns ../example1b.tcl`  2个节点发送 1 条 UDP CBR 流
* V. Making it more interesting
    - `ns ../example2.tcl`  4个节点发送 2 条 UDP CBR 流
* VI. Network dynamics
    - `ns ../example3.tcl`  动态生成 8 个节点, 发送 1 条 UDP CBR 流, 采用动态路由, 使链路中断时, 数据可以重新路由
* VII. A new protocol for ns
    - TODO
* VIII. Creating Output Files for Xgraph
    - `ns ../example4.tcl` 使用 `xgraph` 绘制 3 条 UDP (Exponential) 流的带宽 (in MBit/s) 
* IX. Running Wireless Simulations in ns
    - `ns ../wireless1.tcl` 无线测试1
* X. Creating Wired-cum-Wireless and MobileIP Simulations in ns
    - `ns ../wireless2.tcl` 无线测试2
* XI. Generating node-movement and traffic-connection files for large wireless scenarios
    - `ns ../wireless3.tcl` 无线测试3
    - `./ns-2.35/indep-utils/cmu-scen-gen/``
        + `cbrgen.tcl`
            *生成对应的流量生成 tcl 文件 ns ns-2.35/indep-utils/cmu-scen-gen/cbrgen.tcl -type tcp -nn 25 -seed 0.0 -mc 8 > tcp-25-test.tcl
        + `setdest/setdest`