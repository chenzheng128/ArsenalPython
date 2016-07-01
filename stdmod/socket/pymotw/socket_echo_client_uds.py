#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import sys

BUFFER_SIZE = 1024

# Create a UDS socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = '/tmp/pymotw_uds.socket'  #default socket

print ("debug: argc:%s argv:%s" % (len(sys.argv), sys.argv));
if len(sys.argv) >1:
    server_address = sys.argv[1]

print >>sys.stderr, 'connecting to %s' % server_address
try:
    sock.connect(server_address)
except socket.error, msg:
    print >>sys.stderr, msg
    sys.exit(1)

try:

    while(True):
        # Send data
        message = 'This is the message.  It will be repeated.'
        message = 'class show dev s1-eth2'

        line = raw_input("please input command:")
        if line.startswith("quit"):
            break
        message = line # 使用输入作为发送msg
        print >>sys.stderr, 'sending "%s"' % message

        sock.sendall(message)

        amount_received = 0
        amount_expected = len(message)

        while amount_received < amount_expected:
            data = sock.recv(BUFFER_SIZE)
            amount_received += len(data)
            print >>sys.stderr, 'received "%s"' % data

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()