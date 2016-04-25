# -*- coding:utf-8 -*-
"""
filename:
author:
version:
url: http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing=12345
solution: http://www.pythonchallenge.com/pc/def/peak.html
"""
import math
import mylib
import requests

"""
循环抓取，直到最后一个页面
"""
urlprefix = "http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing="
url = urlprefix+"12345"
response = requests.get(url)
while response.status_code == 200:
    content = response.text
    print "content: ", content
    if (len(content.split(" "))>=6):
        newid = content.split(" ")[-1] #取出后缀id
        print "newid", newid
        url = urlprefix + newid
        print "get url: ", url
        response = requests.get(url) #抓取新id页面
    else:  #如果缺少id， 停止
        break
