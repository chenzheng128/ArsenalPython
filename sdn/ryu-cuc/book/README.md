# Ryu Book 代码

参考：
- 中文: https://osrg.github.io/ryu-book/zh_tw/html/index.html
- 英文: https://osrg.github.io/ryu-book/en/html/index.html (比中文增加了QoS内容)


## 1. `simple_switch_13.py` 交換器（ Switching Hub ）
对应章节代码
## 2. `simple_monitor.py` 流量監控（ Traffic Monitor ）
对应章节代码
## 3. `simple_switch_rest_13.py` REST API

对应章节代码， REST 操作 mac 表命令

```
# 插入mac表
curl -X PUT -d '{"mac" : "00:00:00:00:00:01", "port" : 1}' http://192.168.57.2:8080/simpleswitch/mactable/0000000000000001
curl -X PUT -d '{"mac" : "00:00:00:00:00:02", "port" : 2}' http://192.168.57.2:8080/simpleswitch/mactable/0000000000000001

# 取回mac表
curl -X GET http://192.168.57.2:8080/simpleswitch/mactable/0000000000000001
```

预插入 2条 mac 表后， h1 ping h2 只有一个 arp 产生的 `pack_in (packet in 1 00:00:00:00:00:01 ff:ff:ff:ff:ff:ff 1)`, 而不是 3个 pack_in 消息。

TODO: 结合例子2, 实现REST monitor 查询

## 4. `simple_switch_lacp_13.py` 網路聚合（ Link Aggregation ）

对应章节代码

ryu自带代码 `ryu/appsimple_switch_lacp.py`是1.0版本, 这里是1.3版本, 需要mininet和linux bonding配合, 未测试.

## 5.  生成樹（ Spanning Tree ）
这里无源码, app代码位于自带目录 `ryu/app/simple_switch_stp.py`  中.

## 6.  OpenFlow 通訊協定

源码位于ryu自带库目录 `ryu/ofproto/ofproto_v1_3.py`， Instruction中包含指定該封包到所定義的 meter table中. 对 `ip_dscp` `ecn` `mpls_tc` 等协议字段进行定义。

## 7. ofproto 函式庫¶

这个部分比较重要，清晰之后对OF协议以及Ryu的协议实现会有更好理解。
台式中文的翻译可能不如直接阅读英文原文。

 每個 OpenFlow（ 版本 X.Y ）都有相對應的常數模組（ ofproto_vX_Y ）和解析模組（ ofproto_vX_Y_parser ）每個 OpenFlow 版本的实现基本上是獨立的。

 OpenFlow 版本|	常數模块（消息常量）|	解析模块（解析消息）
 ----|-------------------------|--------
1.0.x|	ryu.ofproto.ofproto_v1_0|	ryu.ofproto.ofproto_v1_0_parser
1.2.x|	ryu.ofproto.ofproto_v1_2|	ryu.ofproto.ofproto_v1_2_parser
1.3.x|	ryu.ofproto.ofproto_v1_3|	ryu.ofproto.ofproto_v1_3_parser
1.4.x|	ryu.ofproto.ofproto_v1_4|	ryu.ofproto.ofproto_v1_4_parser

## 8. `icmp_responder.py` 封包函式庫
以 `icmp_responder.py` 为例，介绍ryu的包封装函数库。 OpenFlow 中 Packet-In 和 Packet-Out 訊息是用來產生封包，可以在當中的欄位放入 Byte 資料並轉換為原始封包的方法。Ryu 提供了相當容易使用的封包產生函式庫給應用程式使用。 具体内容可参考 [API文档][1]

[1]: http://ryu.readthedocs.io/en/latest/ryu_app_api.html

## 8. OF-Config 函式庫

OF-Config 是用來管理 OpenFlow 交換器的一個通訊協定。 OF-Config 通訊協定被定義在 NETCONF（ RFC 6241 ）的標準中，它可以對邏輯交換器的通訊埠（ Port ）和佇列（ Queue ）進行設定以及資料擷取。

```python
from ryu.lib.of_config.capable_switch import OFCapableSwitch
#使用 SSH Transport 連線到交換器。 回呼（ callback ）函式 unknown_host_cb 是用來對應未知的 SSH Host Key 時所被執行的函式。 下面的範例中我們使用無條件信任對方並繼續進行連結。
sess = OFCapableSwitch(
    host='localhost',
    port=1830,
    username='linc',
    password='linc',
    unknown_host_cb=lambda host, fingeprint: True)
#使用 NETCONF GET 來取得交換器的狀態
csw = sess.get()
for p in csw.resources.port:
    print p.resource_id, p.current_rate    
```

Book 中未提供完整的参考代码。 可参考 `ryu/tests/integrated/test_of_config.py` 测试代码, 以及 `/ryu/cmd/of_config_cli.py` 命令行代码中对类 `OFCapableSwitch`的使用

## 9. 防火牆（ Firewall ）
源码位于ryu自带库目录 `ryu/app/rest_firewall.py`
启动命令
```
ryu-manager ryu.app.rest_firewall
```

TODO: 这里的防火墙需要在两个方向上作flow管理, 并不支持TCP会话管理.

## 10. 路由器（ Router ）¶

源码位于ryu自带库目录 `ryu/app/rest_router.py`
启动命令
```
python bin/ryu-manager ryu/app/rest_router.py
```
例子1容易理解, 是标准的路由器
- 設定交換器 s1 的 IP 位址為「172.16.20.1/24」和「172.16.30.30/24」。这里设定的ip在什么位置上呢? 通过ifconfig 没看到对应ip, 因此 ip 被放在控制器内部.

通过dump-flows流表可以可以看到流表3(172.16.20.10)是主机地址, 会直接转发到对应端口, 而流表1,2 上的(172.16.20.1 172.16.30.30)路由ip则被转发至控制器进行处理

```
# ovs-ofctl -O OpenFlow13 dump-flows s1
OFPST_FLOW reply (OF1.3) (xid=0x2):
1 cookie=0x1, duration=10913.051s, table=0, n_packets=5, n_bytes=490, priority=1037,ip,nw_dst=172.16.20.1 actions=CONTROLLER:65535
2 cookie=0x2, duration=10815.451s, table=0, n_packets=0, n_bytes=0, priority=1037,ip,nw_dst=172.16.30.30 actions=CONTROLLER:65535
3 cookie=0x1, duration=434.775s, table=0, n_packets=121542, n_bytes=8022396, idle_timeout=1800, priority=35,ip,nw_dst=172.16.20.10 actions=dec_ttl,set_field:7a:97:5e:dd:f2:8c->eth_src,set_field:00:00:00:00:00:01->eth_dst,output:1
 cookie=0x1, duration=10913.051s, table=0, n_packets=0, n_bytes=0, priority=36,ip,nw_src=172.16.20.0/24,nw_dst=172.16.20.0/24 actions=NORMAL
 cookie=0x2, duration=10815.451s, table=0, n_packets=0, n_bytes=0, priority=36,ip,nw_src=172.16.30.0/24,nw_dst=172.16.30.0/24 actions=NORMAL
 cookie=0x1, duration=10913.051s, table=0, n_packets=0, n_bytes=0, priority=2,ip,nw_dst=172.16.20.0/24 actions=CONTROLLER:65535
 cookie=0x2, duration=10815.451s, table=0, n_packets=0, n_bytes=0, priority=2,ip,nw_dst=172.16.30.0/24 actions=CONTROLLER:65535
 cookie=0x0, duration=10962.886s, table=0, n_packets=213, n_bytes=8946, priority=1,arp actions=CONTROLLER:65535
 cookie=0x10000, duration=10648.559s, table=0, n_packets=245604, n_bytes=15946198628, priority=1,ip actions=dec_ttl,set_field:12:15:b8:55:4f:64->eth_src,set_field:d6:3a:6f:cd:9f:df->eth_dst,output:2
 cookie=0x0, duration=10962.886s, table=0, n_packets=0, n_bytes=0, priority=0 actions=NORMAL
```

在控制器上 `_packetin_icmp_req()` 函数中实现了网关的 icmp 回应, 其 ping 延时在 2ms (用户态) 左右, 比主机的 0.07ms (内核态) 延时要大的多.


例子2加入了 vlan 租户分离, 需要注意的是:
- 拓扑图一个vlan对应的是一个租户, 每个租户下存在不同路由策略与子网
- 这里区别与过去的vlan. 过去的一个vlan对应的是一个子网, 而不是一个租户

## 11. QoS
 英文Book才有的内容(晕): https://osrg.github.io/ryu-book/en/html/rest_qos.html
 需要 ovs 库支持 `pip install ovs`

在mininet中启动网络, 并设置交换机协议与ovsdb管理端口6632, 正常设置后6632将开始监听
```
# mn --mac --topo linear --controller remote,ip=127.0.0.1 #如果ryu在本机, 此ip为 controller ip,  ryu在本机时应为127.0.0.1
# ovs-vsctl set-manager ptcp:6632
# netstat -nat | grep 6632
tcp        0      0 0.0.0.0:6632            0.0.0.0:*               LISTEN
# ovs-vsctl set Bridge s1 protocols=OpenFlow13 #设置交换机协议, 设置正常ryu 将显示 [QoS][INFO] dpid=0000000000000001: Join qos switch. 
# ovs-vsctl set Bridge s2 protocols=OpenFlow13 #设置交换机协议, 设置正常ryu 将显示 [QoS][INFO] dpid=0000000000000002: Join qos switch.
```


 参考book 用sed命令创建 `qos_simple_switch_13.py` 文件 (在文件中仅增加 tableid=1 增加qos控制) 
 
运行 ryu qos app, ( 为便于显示调试信息, 可追加日志输出 `./bin/ryu-manager --verbose --log-config-file cuc/logging_config.ini` )
```
# cd $RYU_HOME 
# PYTHONPATH=. ./bin/ryu-manager ryu.app.rest_conf_switch ryu.app.rest_qos  cuc/book/qos_simple_switch_13.py
```

3个app作用
- `qos_simple_switch_13.py` 维护 tableid=1 转发flow操作 
- `rest_qos.py _set_qos()` 维护 tableid=0 SET_QUEUE 等qos操作, 然后 GOTO_TABLE id=1 进行转发 (TODO 待实验验证)
- `rest_conf_switch.py` 维护rest方式的交换机 ovsdb 配置 http://localhost:8080/v1.0/conf/switches/0000000000000001/ovsdb_addr 

通过 `rest_conf_switch.py` rest配置ovsdb_addr地址 
```
# curl -X PUT -d '"tcp:127.0.0.1:6632"' http://localhost:8080/v1.0/conf/switches/0000000000000001/ovsdb_addr # book命令中如果ryu在本机, 则此ip应为127.0.0.1
```

通过 `rest_qos.py` rest配置htb队列, 格式化json输出
```
# time curl -X POST -d '{"port_name": "s1-eth1", "type": "linux-htb", "max_rate": "1000000", "queues": [{"max_rate": "500000"}, {"min_rate": "800000"}]}' http://localhost:8080/qos/queue/0000000000000001 | python -mjson.tool
"result": "success" #配置成功的返回信息
real	0m0.07s # 设置的运行时间
```

检查端口 tc 配置
```
# tc qdisc show dev s1-eth1
class htb 1:1 parent 1:fffe prio 0 rate 12000bit ceil 500000bit burst 1563b cburst 1564b
class htb 1:fffe root rate 1000Kbit ceil 1000Kbit burst 1500b cburst 1500b
class htb 1:2 parent 1:fffe prio 0 rate 800000bit ceil 1000Kbit burst 1564b cburst 1564b
```

## 12. 测试

使用下面的指令來執行測試工具。
```
$ ryu-manager [--test-switch-target DPID] [--test-switch-tester DPID]
 [--test-switch-dir DIRECTORY] ryu/tests/switch/tester.py
```

選項	|說明	|預設值
-------------------|-----------------------|------------------
–test-switch-target	| 待測交換器的 datapath ID | 	0000000000000001
–test-switch-tester	| 輔助交換器的 datapath ID |	0000000000000002
–test-switch-dir	| 測試樣板的存放路徑	| ryu/tests/switch/of13

原始碼	| 說明
--------------------------------|----------------
ryu/tests/switch/tester.py |	測試工具
ryu/tests/switch/run_mininet.py	| 建立測試環境的腳本
ryu/tests/switch/of13	| 測試樣板的一些範例

ryu/tests/switch/of13 包含 `action group match meter` 四个目录, 通过这些目录可以更详细学习openflow的协议内容实现

Ryu 原始碼當中利用腳本实现了一個在 mininet 上的測試環境，當中是採用 Open vSwtich 做為待測交換器

首先在mininet vm启动 `run_mininet.py` mininet 拓扑网络 (默认ip使用 127.0.0.1 和book文档保持一致便于命令测试, 不使用我们自定义的192.168.57 ), 然后运行 `tester.py`
```
mininet-vm:/opt$ sudo python ryu/ryu/tests/switch/run_mininet.py
mininet-vm:/opt$ PYTHONPATH=. python ./ryu/bin/ryu-manager --test-switch-dir ryu/ryu/tests/switch/of13 ryu/ryu/tests/switch/tester.py
```

在交换机 ovs_version: "2.4.0" ( sudo ovs-vsctl show ) 测试结果如下, 522条通过.

```
...
match: 33_IPV6_ND_TLL                    ethernet/vlan/ipv6/icmpv6(data=nd_neighbor(option=nd_option_tla(hw_src='aa:aa:aa:aa:aa:aa')))-->'ipv6_nd_tll=22:22:22:22:22:22,actions=output:2'
    match: 36_MPLS_BOS                       ethernet/mpls(bsb=0)/mpls(bsb=1)/ipv6/tcp-->'mpls_bos=1,actions=output:2'
OK(522) / ERROR(469)
```


## 13. 組織架構
这里可以了解 ryu 的  Application programming model  应用开发模型. 对于一些台语词进行整理

台语 |  中文 | 英语 | 说明
-------|--|---------------|----------------------------------------
應用程式 |应用程序|（ Application ） | 應用程式是繼承 ryu.base.app_manager.RyuApp 而來。User logic 被視作是一個應用程式。
事件 ||（ Event ） | 事件是繼承 ryu.controller.event.EventBase 而來，並藉由 Transmitting 和 receiving event 來相互溝通訊息。
事件佇列  |事件队列| （ Event queue ） | 每個應用程式都有一個自己的佇列用來接受事件訊息。
執行緒 |线程| （ Thread ）| Ryu 採用 eventlet 來實現多執行緒。因為執行緒是不可插斷的（ non-preemptive ），因此在使用上要特別注意長時間運行所帶來的風險。
事件迴圈  |事件循环| （ Event loop ） | 當應用程式執行時，將會有一個執行緒自動被產生用來執行該應用程式。 該執行緒將會做為事件迴圈的模式來執行。如果在事件佇列中發現有事件存在，該事件迴圈將會讀取該事件並且呼叫相對應的事件處理器來處理它。
額外的執行緒 |额外线程| （ Additional thread ） | 如果需要的話，你可以使用 hub.spawn 產生額外的執行緒用來執行特殊的應用程式功能。

 || eventlet  | 雖然你可以直接使用 eventlet 所提供的所有功能，但不建議你這麼做。 請使用 hub module 所包裝過的功能取代直接使用 eventlet。

事件處理器 || （ Event handler ） | 藉由使用 ryu.controller.handler.set_ev_cls 裝飾器類別來定義自己的事件管理器。當定義的事件發生時，應用程式中的事件迴圈將會偵測到並呼叫對應的事件管理器。

## 14. 協助專案開發
注意:
- 不支持 python 3.0
- 应符合 符合 PEP8 的規範 http://www.python.org/dev/peps/pep-0008/
- 单元测试脚本 `cd ryu/;  ./run_tests.sh`
- 补丁提交与 maillist 交流 `git format-patch origin -s; git send-email 0001-sample.patch`

## 15. 應用案例
跳过
