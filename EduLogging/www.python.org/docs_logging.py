# -*- coding:utf-8 -*-

"""
官方文档与帮助
https://docs.python.org/2/library/logging.html
"""

# -*- coding: utf-8 -*-
import logging

"""
https://docs.python.org/2/library/logging.html#module-logging

命令行配置 --log=INFO 无用
采用 logging.basicConfig()

"""


# numeric_level = getattr(logging, loglevel.upper(), None)
# if not isinstance(numeric_level, int):
#     raise ValueError('Invalid log level: %s' % loglevel)

def log1():
    """
    this is root logger
    :return:
    """
    #logging.basicConfig(format='%(levelname)-8s %(message)-60s', level=logging.INFO)
    logging.debug('debug message')
    logging.info('info message')
    logging.warn('warn message')
    logging.error('error message')
    logging.critical('critical message')
    #logging.log("hello")
    logging.warn( "root 打印不出info/ debug信息, 因为默认的root logger 是warning")
    logging.warn("--- log1 end ---\n")

def log2():
    #logging.basicConfig(format='%(levelname)-8s %(message)-60s', level=logging.INFO)
    #logging.basicConfig(level=logging.INFO)
    logger2 = logging.getLogger(__name__ + ".log2")
    logger2.setLevel(logging.DEBUG) #改变 logger2 等级
    logger2.debug('debug message')
    logger2.debug('debug message')
    logger2.info('info message')
    logger2.info('info message')
    logger2.info("--- log2 end --- 重设level的log2可以正常显示了\n")


def log3():
    FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
    logger3 = logging.getLogger(__name__ + ".log3")
    logger3.setLevel(logging.DEBUG) #改变 logger2 等级
    logger3.debug('debug message')
    logger3.debug('debug message')
    logger3.info('info message')
    logger3.info('info message')
    logger3.info("--- log3 end ---\n")

def log4():
    FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    data = {'clientip': '192.168.0.1', 'user': 'zhchen'}
    logger = logging.getLogger('tcpserver')
    logger.warning('Protocol problem: %s', 'connection reset', extra=data)

    logging.info("--- log3 end ---")

def main():
    # logging.basicConfig 需要最开始被调用
    log1()
    log2()
    log3()

if __name__ == "__main__":
    main()