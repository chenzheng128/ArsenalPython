# coding: utf-8

"""
使用 hist magic 保存 ipython 命令， 便于命令行调试
%hist
"""

import time
from datetime import datetime
from douban_client import DoubanClient
from douban_mongo import StorageClient
import logging

log = logging.getLogger(__name__)

level = logging.WARNING
level = logging.DEBUG
logging.basicConfig(format='%(name)s \t\t%(levelname)-8s %(filename)8s %(funcName)8s() [%(message)-60s] %(module)s',
                    level=level)
douban_client = DoubanClient()
mongo_client = StorageClient()
content, error = douban_client.movie_in_theaters()

type(content)
print("将这些代码复制到 ipython 中，便于调试 ..")