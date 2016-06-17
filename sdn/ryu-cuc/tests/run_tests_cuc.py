#!/usr/bin/python
# --*-- coding:utf-8 --*--

"""
运行测试
cd RYU_HOME
PYTHONPATH=. ./cuc/run_tests_cuc.sh
"""

import os
import sys

from nose import config
from nose import core

sys.path.append(os.getcwd())
sys.path.append(os.path.dirname(__file__))


import ryu.tests.unit
import cuc
from cuc.tests.test_lib import run_tests


if __name__ == '__main__':
    exit_status = False

    # if a single test case was specified,
    # we should only invoked the tests once
    invoke_once = len(sys.argv) > 1

    cwd = os.getcwd()
    c = config.Config(stream=sys.stdout,
                      env=os.environ,
                      verbosity=int(os.environ.get('NOSE_VERBOSE', 3)),
                      includeExe=True,
                      traverseNamespace=True,
                      plugins=core.DefaultPluginManager())

    # 原始测试
    #c.configureWhere(ryu.tests.unit.__path__)
    # c.configureWhere("ryu/tests/unit") #等于上一句的测试
    # 独立测试

    c.configureWhere("ryu/tests/unit/cmd")
    c.configureWhere("cuc/tests/unit/")
    #c.configureWhere("ryu/tests/unit/cuc")
    # c.configureWhere("")

    exit_status = run_tests(c)
    sys.exit(exit_status)
