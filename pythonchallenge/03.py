# -*- coding:utf-8 -*-
"""
filename:
author:
version:
url: http://www.pythonchallenge.com/pc/def/ocr.html
solution: http://www.pythonchallenge.com/pcc/def/equality.html
"""
import math

"""
读取完整文件拼接，去掉换行为一个字符
"""
with open('data/03.txt') as f:
    lines = f.readlines()
orig_str="".join(lines).replace("\n", "")

"""Out[35]: (98765, 19753)"""


def uniq_count(check_size):
    """
    分割统计函数，将字符串按check_size分割统计
    便于观察字符串的出现频率
    """
    chunks, chunk_length = len(orig_str), len(orig_str)/chunk_size
    dict_count={}
    for i in range(0, chunks, chunk_size):
        tmp_str=orig_str[i:i+chunk_size]
        if dict_count.has_key(tmp_str):
            dict_count[tmp_str]+=1
        else:
            dict_count[tmp_str]=1
    return dict_count

for chunk_size in range(1, 5):
    dict_count = uniq_count(chunk_size)
    print "长度为 ", chunk_size, " 发现独立字典字符为 ", len(dict_count)
    if len(dict_count) < 30:
        print dict_count
"""
结果如下， 说明 a,b,c,d的出现概率很低, 是重要字符
{'!': 6079, '#': 6115, '%': 6104, '$': 6046, '&': 6043, ')': 6186, '(': 6154, '+': 6066, '*': 6034, '@': 6157, '[': 6108, ']': 6152, '_': 6112, '^': 6030, 'a': 1, 'e': 1, 'i': 1, 'l': 1, 'q': 1, 'u': 1, 't': 1, 'y': 1, '{': 6046, '}': 6105
"""

"""
遍历 orig_str 去掉里面的特殊字符
"""
new_str=""
for x in range(len(orig_str)):
    if not orig_str[x].isalpha():
        tmp_str=""
    else:
        tmp_str=orig_str[x]
    new_str += tmp_str
print "isalpha() 方法： \t", new_str
