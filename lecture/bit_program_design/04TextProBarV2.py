#coding:utf-8
#TextProBarV2.py
print("\n=== 版本V2 ===")
import time
for i in range(101):
    print("\r{:3}%".format(i), end="") #TODO \r 的作用？
    time.sleep(0.1)
