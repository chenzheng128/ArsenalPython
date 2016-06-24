# 进程速度测试

copy from ipc-bench

`get_tc_queue_lat` 测试tc速度; (TODO strtok 函数崩溃问题)

```
make && get_tc_queue_lat 1 # 检查tc队列 1 的队列状态
```


ipc-bench
=========

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
