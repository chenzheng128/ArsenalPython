#coding=utf-8
"""
50行python代码实现个代理服务器（你懂的）
revised from http://blog.csdn.net/handsomekang/article/details/39347357
add argv support
"""
import socket  
import select  
import sys  
  
to_addr = ('202.205.22.197', 80)#转发的地址
listen_port = 10080
  
class Proxy:  
    def __init__(self, addr):  
        self.proxy = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.addr = addr
        self.proxy.bind(addr)  
        self.proxy.listen(10)  
        self.inputs = [self.proxy]  
        self.route = {}  
  
    def serve_forever(self):  
        print 'proxy listen in :%s forward to %s:%s ...' % (self.addr[1], to_addr[0], to_addr[1])
        while 1:  
            readable, _, _ = select.select(self.inputs, [], [])  
            for self.sock in readable:  
                if self.sock == self.proxy:  
                    self.on_join()  
                else:  
                    data = self.sock.recv(8096)  
                    if not data:  
                        self.on_quit()  
                    else:  
                        self.route[self.sock].send(data)  
  
    def on_join(self):  
        client, addr = self.proxy.accept()  
        print addr,'connect'  
        forward = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        forward.connect(to_addr)  
        self.inputs += [client, forward]  
        self.route[client] = forward  
        self.route[forward] = client  
  
    def on_quit(self):  
        for s in self.sock, self.route[self.sock]:  
            self.inputs.remove(s)  
            del self.route[s]  
            s.close()  
  
if __name__ == '__main__':
    if len(sys.argv) >1:
        if len(sys.argv) !=4:
            print "Usage: %s local_port remote_ip remote_port" % (sys.argv[0])
            exit(1)
        else:
            listen_port = int(sys.argv[1])
            to_addr = (sys.argv[2], int(sys.argv[3]))
    try:
        Proxy(('',listen_port)).serve_forever()#代理服务器监听的地址
    except KeyboardInterrupt:  
        sys.exit(1)  