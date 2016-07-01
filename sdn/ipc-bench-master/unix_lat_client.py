#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
和其他 _latency 程序不同, 需要和server一起使用
配合 ArsenalPython/stdmod/socket/pymotw 下


`python socket_echo_server_uds.py` 结果
配合 iproute2 tc `while true; do  make && ./tc/tc bench; done` 结果
"""
import socket
import sys
import time

usleep = lambda x: time.sleep(x / 1000000.0)

expect_recv_size = 0
expect_send_size = 0
BENCH_MODE = True
send_cmd = ""
bench_total = 0
# Create a UDS socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = '/tmp/bench.socket'  # default socket

print ("debug: argc:%s argv:%s" % (len(sys.argv), sys.argv))
if len(sys.argv) != 5:
    print ("usage: ./unix_lat_client name.socket \"command\" <expect_recv_size> <roundtrip-count>");
    exit(1)
else:
    server_address = sys.argv[1]
    send_cmd = sys.argv[2]
    expect_send_size = len(send_cmd)
    expect_recv_size = int(sys.argv[3])
    bench_total = int(sys.argv[4])


if server_address.find("bench") == -1: # socket 字符参数中不包含 bench 以禁止bench模式
    print ("debug: not in BENCH_MODE, display all output ...\n")
    BENCH_MODE = True


print >> sys.stderr, 'connecting to %s' % server_address
try:
    sock.connect(server_address)
except socket.error, msg:
    print >> sys.stderr, msg
    sys.exit(1)

try:

    # 采样间隔时间, 默认0，不休眠
    polling_interval = 0
    # bench_total = 100000  # 测速 循环数 average latency: 3506 ns (4us) /
    polling_interval = 10
    #bench_total = 1000000

    bench_count = 0
    delta = 0
    total_bytes = 0
    start = time.time()

    while True:
        # Send data
        message = 'This is the message.  It will be repeated.'
        message = 'class show dev s1-eth2'  # len 323
        # print message


        if not BENCH_MODE:
            print >> sys.stderr, 'sending "%s"' % message

        # sock.sendall(message)
        sock.sendall(send_cmd)
        usleep(polling_interval)

        amount_received = 0
        amount_expected = 327  # len(message)

        # while amount_received < amount_expected:
        if True:
            data = sock.recv(expect_recv_size)
            amount_received += len(data)
            if BENCH_MODE:
                if ((bench_count % 100) == 0): print ".",
            else:
            #if True:
                print "recv len(data)=%s" % len(data)
                print >> sys.stderr, 'received "%s"' % data

        bench_count += 1
        total_bytes += len(data)
        if bench_count > bench_total:
            break

    if (BENCH_MODE) :
        print ""
        print "polling_interval: %s (等候数据回写间隔)" % polling_interval
        print "roundtrip count: %s" % bench_total
        print "total_bytes: %s" % total_bytes
        print "avg_bytes(should equals to interactive mode): %s bytes " % (total_bytes/bench_total)

    delta = time.time() - start
    print("average latency: %s ns" % int(delta / (bench_total * 2) * 1000000000))

finally:
    print >> sys.stderr, 'closing socket'
    sock.close()
