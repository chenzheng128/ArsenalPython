#coding:utf-8
#TextProBarV1.py
print("\n=== 版本V1 ===")

import time
scale = 10
print("------执行开始------")
for i in range(scale+1):
    a = '*' * i
    b = '.' * (scale - i)
    c = (i/scale)*100
    print("\r{:^3.0f}%[{}->{}]".format(c,a,b), end="")
    time.sleep(0.1)
print("\n------执行结束------")
