# 进程速度测试

copy from ipc-bench

TODO: 将 `unix_lat`的 `socketpair`无名管道方法, 修改为 C/S 架构.
- C: client 为检查tc出现队列拥塞的进程, 考虑用独立程序, 或是内嵌在 ovs 中. 当发现拥塞时, 向Server发出拥塞产生 / 队列状态 / 或是降低速率的要求.
- S: Server 为需要被控制的网卡主机, 例如 h1/h2 或 s1/2.
- `tc_shell_p_lat` 修补strok存在指针异常情况

## tc 测试命令
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
