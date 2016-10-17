## Practical TCP/IP Sockets in C, Second Edition

Book: http://cs.baylor.edu/~donahoo/practical/CSockets2/

```

在 Mac 上编译


原始 build
Generally, compilation is as follows:
Linux: gcc -o TCPEchoClient -std=gnu99 TCPEchoClient.c DieWithMessage.c TCPClientUtility.c
Solaris: gcc -o TCPEchoClient TCPEchoClient.c DieWithMessage.c TCPClientUtility.c -lsocket -lnsl
Both: Add -lpthread to both Linux and Solaris for the threads example
```

All practical serial: http://cs.baylor.edu/~donahoo/practical/
