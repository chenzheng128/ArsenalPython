# -*- coding:utf-8 -*-
"""
常用的library函数定义在这里
filename: mylib.py
author:
version:
"""

def uniq_count(input_str, chunk_size):
    """
    分割统计函数，将input_str字符串按check_size分割统计
    便于观察字符串的出现频率
    """
    chunks, chunk_length = len(input_str), len(input_str)/chunk_size
    dict_count={}
    for i in range(0, chunks, chunk_size):
        tmp_str=input_str[i:i+chunk_size]
        if dict_count.has_key(tmp_str):
            dict_count[tmp_str]+=1
        else:
            dict_count[tmp_str]=1
    return dict_count
