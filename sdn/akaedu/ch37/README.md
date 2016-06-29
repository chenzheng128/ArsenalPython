
### Unix Socket 实验

实验1. bind() `ex37.unix.bind` bind创建文件套接字, 重复绑定(文件已存在时)时会报`bind error: Address already in use`错误.  
```
rm -f /tmp/sdn/aka*.socket; make && sudo ./ex37.unix.bind
```

实验2. server/client 连接. 
ada book 提供的 unix 代码不完整. 改为使用这里的代码[UNIX domain sockets](http://troydhanson.github.io/network/Unix_domain_sockets.html)
```
./unix_server
./unix_client
```

### UDP 代码实验
ada book 提供的代码 `ex37.udp_server` 运行不了. 代码陈旧, 不再使用. 

改为使用 rutgers CS417 的 `udp_server(udp-recv)` `udp_client(udp-send)` 代码

参考: [CS417 Introduction to Sockets Programming] (https://www.cs.rutgers.edu/~pxk/417/notes/sockets/index.html)

### TCP 代码实验

```
./ex37.tcp_client
./ex37.tcp_server
```