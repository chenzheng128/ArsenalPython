#!/usr/bin/python
# --*-- coding:utf-8 --*--

# Source https://fredhsu.wordpress.com/2013/10/15/ovsdb-client-in-python/

import socket

OVSDB_IP = '127.0.0.1'
OVSDB_PORT = 6632

def get_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((OVSDB_IP, OVSDB_PORT))
    return s

import json

def get_resposne():
    s=get_socket()
    list_dbs_query =  {"method":"list_dbs", "params":[], "id": 0}
    s.send(json.dumps(list_dbs_query))
    response = s.recv(4096)
    return response

if __name__ == '__main__':
    print get_resposne()