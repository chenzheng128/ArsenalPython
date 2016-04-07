# -*- coding:utf-8 -*-
"""
filename:
author:
version:
url: http://www.pythonchallenge.com/pc/def/map.html
solution: http://www.pythonchallenge.com/pcc/def/ocr.html
"""
import math

orig_str="""g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj."""
new_str=""
for x in range(len(orig_str)):
    """
    In [7]: ord('k')
    Out[7]: 107

    In [8]: ord('m')
    Out[8]: 109

    In [9]: ord('o')
    Out[9]: 111

    In [10]: ord('q')
    Out[10]: 113

    In [11]: ord('e')
    Out[11]: 101

    In [12]: ord('g')
    Out[12]: 103

    if orig_str[x]=='m':
        tmp_str='k'
    elif orig_str[x]=='q':
        tmp_str='o'
    elif orig_str[x]=='g':
        tmp_str='e'
    else:
        tmp_str=orig_str[x]
    """
    if orig_str[x].isalpha():
        tmp_str=chr(ord(orig_str[x])+2)
    else:
        tmp_str=orig_str[x]
    new_str += tmp_str

print "原始字符串: \t\t", orig_str

print "ord()/chr()方法： \t", new_str

import string
intab  = "abcdefghijklmnopqrstuvwxyz"
outtab = "cdefghijklmnopqrstuvwxyzab"
trantab = string.maketrans(intab, outtab)

print "maketrans()方法：\t",  orig_str.translate(trantab)

url="/map."

print "to url：\t",  url.translate(trantab)
