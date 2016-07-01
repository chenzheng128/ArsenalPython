#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import sys
import os

BENCH_MODE = True
server_address = '/tmp/bench.socket'
BUF_SIZE=100

if len(sys.argv) >1:
    server_address = sys.argv[1]

if server_address.find("bench") == -1: # socket 字符参数中不包含 bench 以禁止bench模式
    print ("debug: not in BENCH_MODE, display all output ...\n")
    BENCH_MODE = False

# Make sure the socket does not already exist
try:
    os.unlink(server_address)
except OSError:
    if os.path.exists(server_address):
        raise

# Create a UDS socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# Bind the socket to the port
print >>sys.stderr, 'starting up on %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    if not BENCH_MODE:
        print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()
    try:
        if not BENCH_MODE:
            print >>sys.stderr, 'connection from', client_address

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(BUF_SIZE)
            if not BENCH_MODE:
                print >>sys.stderr, 'received "%s"' % data
            if data:
                if not BENCH_MODE:
                    print >>sys.stderr, 'sending data back to the client'
                connection.sendall('0'*BUF_SIZE)
            else:
                if not BENCH_MODE:
                    print >>sys.stderr, 'no more data from', client_address
                break

    finally:
        # Clean up the connection
        connection.close()