#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Elephant'

import requests
from lxml import etree


def main():
    url = 'http://xw.qq.com/index.htm'
    response = requests.get(url)
    content = response.text
    print "response:",response
    print "content:",response.encoding

    tree = etree.HTML(content)
	
    ########腾讯新闻mobile版导航栏########
    #<div class="nav">
    #<ul>
    #    <li><a href="http://xw.qq.com/m/news/">新闻</a></li>
    #    <li><a href="http://xw.qq.com/m/finance/">财经</a></li>
    #    ... ...
    #</ul>
    #</div>
    ######################################

    # 在标签<div>下查找属性class的值为"nav"下的所有<a>的节点
    a_nodes = tree.xpath(u'//div[@class="nav"]/ul/li/a')
    print "a_nodes_length:", len(a_nodes)
    for a_node in a_nodes:
        #print "<a>:", a_node.text    # 腾讯用的什么中文字符格式,为什么无法输出
        print "<a>:", a_node.text.encode('utf-8')
        print "<href>:", a_node.attrib['href']
    print "\n"

if __name__ == "__main__":
    main()
