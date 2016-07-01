# 进程速度测试

copy from ipc-bench

TODO: 将 `unix_lat`的 `socketpair`无名管道方法, 修改为 C/S 架构.
- C: client 为检查tc出现队列拥塞的进程, 考虑用独立程序, 或是内嵌在 ovs 中. 当发现拥塞时, 向Server发出拥塞产生 / 队列状态 / 或是降低速率的要求.
- S: Server 为需要被控制的网卡主机, 例如 h1/h2 或 s1/2.
- `tc_shell_p_lat` 修补strok存在指针异常情况

## 完成unix domain socket 延时测试

ipc-bench 完成 C /  python / tc 的unix延时测试
其单方向延时如下
- C:    3us  较小, 可忽略
- Python: 60us 较大, 不可忽略
- 调用tc查询代码: 30us (比之前有睡眠的50us的速度提高了,)


### 扩展测试4: Python -> C(tc)

- 客户端 `python unix_lat_client.py /var/sdn/bench.socket "class show dev s1-eth1" 250 100000`
- 服务端 `while true; do  make && ./tc/tc bench; done`

```
polling_interval: 10 (等候数据回写间隔)
roundtrip count: 100000
total_bytes: 25000250
avg_bytes(should equals to interactive mode): 250 bytes
average latency: 71036 ns
```
从时间上看: Time(扩展测试4) = Time(扩展测试3) + Time(扩展测试2); 增加的时间差不多是python的效率(60us), 加上tc效率(30us) 

### 扩展测试3: C -> C(tc) *最优方式*
比echo服务增加了 tc 的查询内容

- 客户端 `./unix_lat_client "class show dev s1-eth1" 300 10000`
- 服务端 `while true; do  make && ./tc/tc bench; done`
效率如下 27us 不低; 日志都打印出也很快; TODO 如果 expect_recv_size 很小不是 300 程序会崩溃, why?  
```
message content: class show dev s1-eth1
message size: 23 octets
roundtrip count: 1
debug: connet on socket_path: /var/sdn/bench.socket
average latency: 27175 ns
```

### 扩展测试2: Python -> C(echo)
比echo服务增加了 tc 的查询内容

- 客户端 `python unix_lat_client.py /tmp/bench.socket "class show dev s1-eth1" 100 100000`
- 服务端 `make && while true; do ./unix_lat_server 22 100; done`
延时为 53us 不高; python的效率还是有待提高  
```
polling_interval: 10 (等候数据回写间隔)
roundtrip count: 100000
total_bytes: 10000100
avg_bytes(should equals to interactive mode): 100 bytes
average latency: 52939 ns
closing socket
```

### 基准测试1: C -> C(echo)
原有的 ./unix_lat 用的是fork 无名管道, 这里我们将它拆分为 
- 客户端 `./unix_lat_client "class show dev s2-eth1" 100 100000`
- 服务端 `make && while true; do ./unix_lat_server 23 100; done`
这里 "class show dev s2-eth1" 的长度正好是 23, 如果两边的长度对齐之后, 
 发送效率是最高的, 约 2us 左右
 没对齐的情况下如果发送消息很多超过缓存, 时间就不容易保证了.
```
essage content: class show dev s2-eth1
message size: 23 octets
roundtrip count: 100000
debug: connet on socket_path: /tmp/bench.socket
average latency: 2087 ns
```


## tc shell 测试命令
`make && sudo ./tc_shell_lat 100 10000` 测试tc change速度; (TODO strtok 函数崩溃问题)

```
make && ./tc_shell_p_lat 1 # 检查tc队列 1 的队列状态
```

## tc 测试结果


tc change 延时为 1ms 左右
```
# 评估命令 tc class change dev s2-eth2 parent 1:fffe classid 1:2 htb rate 4mbit burst 15k
make && sudo ./tc_shell_lat 100 10000  # 总时间 10 秒左右
message size: 100 octets
roundtrip count: 10000
average latency: 932472 ns  # 0.9 ms
# 评估命令 "tc -s -d class show dev s2-eth1 >/dev/null 2>&1") # change 和 show 时间接近
message size: 100 octets
roundtrip count: 10000
average latency: 847618 ns  # 0.8 ms
```

## udp 测试
* 新增 udp_lat.c 文件: 基于 `tcp_lat.c` 复制 `udp_lat.c` 文件, 增加编译代码;
* 对比情况: unix_lat < udp_lat < tcp_lat
* 测试结果: 3us;   
```
$ make && ./udp_lat 100 100000
debug: listen_ip=127.0.0.1 port=33333
message size: 100 octets
roundtrip count: 100000
average latency: 3326 ns
```

ipc-bench
=========


TCP/Unix性能对比: http://stackoverflow.com/questions/14973942/performance-tcp-loopback-connection-vs-unix-domain-socket; TCP 比 Unix Socket 慢2倍, 大约是有封包和拆包的缘故.


## ipc测试结果
在 minient 虚拟机中 Unix Socket(unix_lat) 延时级别为 2us, 效率很高.
```

# Linux (mininet) msgsize=100 # 基准测试, 约2us, Linux虚拟机比Mac效果还好
./unix_lat 100 100000
message size: 100 octets
roundtrip count: 100000
average latency: 2115 ns

# Mac air
./unix_lat 100 100000
message size: 100 octets
roundtrip count: 100000
average latency: 3537 ns


# Linux msgsize=1500 增长到1500之后, 延时变化不大, 整体增加了 200-300ns (0.3 us)

./unix_lat 1500 1024000
message size: 1500 octets
roundtrip count: 1024000
average latency: 2272 ns  # 2us Unix Socket 延时

./tcp_lat 1500 1024000
message size: 1500 octets
roundtrip count: 1024000
average latency: 3586 ns  # 4us 大约为Unix Socket两倍

./pipe_lat 1500 1024000
message size: 1500 octets
roundtrip count: 1024000
average latency: 2062 ns

# Linux msg size 1 的效果

$ ./unix_lat 1 1024000
message size: 1 octets
roundtrip count: 1024000
average latency: 1907 ns

$ ./pipe_lat 1 1024000
message size: 1 octets
roundtrip count: 1024000
average latency: 1634 ns


$ ./tcp_lat 1 1024000
message size: 1 octets
roundtrip count: 1024000
average latency: 3345 ns
```


Some very crude IPC benchmarks.

ping-pong latency benchmarks:
* pipes
* unix domain sockets
* tcp sockets

throughput benchmarks:
* pipes
* unix domain sockets
* tcp sockets

This software is distributed under the MIT License.

Credits
-------

* *desbma* for adding cross platform support for clock_gettime
