# -*- coding:utf-8 -*-
"""
filename:
author:
version:
url: http://www.pythonchallenge.com/pc/def/equality.html
solution: http://www.pythonchallenge.com/pc/def/linkedlist.php
"""
import math
import mylib

with open('data/04.txt') as f:
    lines = f.readlines()
orig_str="".join(lines).replace("\n", "")


print "=== mylib.uniq_count ==="
for chunk_size in range(1, 5):
    dict_count = mylib.uniq_count(orig_str, chunk_size)
    print "长度为 ", chunk_size, " 发现独立字典字符为 ", len(dict_count)
    if len(dict_count) < 60:
        print dict_count

"""
遍历 orig_str 查找
  One small letter, surrounded by EXACTLY three big bodyguards on each of its sides.
"""
new_str=""
match_count={}
for x in range(1, len(orig_str)):
    if not str.istitle(orig_str[x-1]):
        if str.istitle(orig_str[x]):
            if str.istitle(orig_str[x+1]):
                if str.istitle(orig_str[x+2]):
                    if not str.istitle(orig_str[x+3]):
                        if str.istitle(orig_str[x+4]):
                            if str.istitle(orig_str[x+5]):
                                if str.istitle(orig_str[x+6]):
                                        if not str.istitle(orig_str[x+7]):
                                            #new_str =orig_str[x-1:x+8] #显示头尾字符，确保匹配成功
                                            new_str =orig_str[x:x+7]
                                            match_count[new_str]=1
                                            print "istitle() 方法： \t", new_str

print "读入 字符串长度为 len(orig_str) = %s " % len(orig_str)
print "找到 len(match_count) = %s 个匹配字符串 " % len(match_count)

"""
从下面的小写字符串中可以读出 linkedlist
istitle() 方法： 	IQNlQSL
istitle() 方法： 	OEKiVEY
istitle() 方法： 	ZADnMCZ
istitle() 方法： 	ZUTkLYN
istitle() 方法： 	CNDeHSB
istitle() 方法： 	OIXdKBF
istitle() 方法： 	XJVlGZV
istitle() 方法： 	ZAGiLQZ
istitle() 方法： 	CJAsACF
istitle() 方法： 	KWGtIDC
"""
