# -*- coding:utf-8 -*-
# REF: http://pyunit.sourceforge.net/pyunit_cn.html#USING

import unittest
from main.widget import Widget


class SimpleWidgetTestCase(unittest.TestCase):
    """
    使用setUp和teardown方法
    """

    def setUp(self):
        self.widget = Widget("The widget")
        #print "  setUp()"

    def tearDown(self):
        self.widget.dispose()
        self.widget = None
        #print "  tearDown()"


class DefaultWidgetSizeTestCase(SimpleWidgetTestCase):
    def runTest(self):
        assert self.widget.size() == (50, 50), 'incorrect default size'


class WidgetResizeTestCase(SimpleWidgetTestCase):
    """
    runTest 和 test_ 两种方法不能同时存在, 同时存在时将只执行test_
    """

    def runTest(self):
        print __name__, "runTest"
        self.widget.resize(100, 150)
        assert self.widget.size() == (100, 150), \
            'wrong size after resize'

    def test_nothing(self):
        print "test_nothing"

    def test_runTest(self):
        print self.runTest()


if __name__ == '__main__':
    unittest.main()
