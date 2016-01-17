# -*- coding:utf-8 -*-
import unittest
import sys
import main


class MyTestCase(unittest.TestCase):
    def test_go(self):
        pass

    @unittest.skip("demonstrating skipping")
    def test_nothing(self):
        self.fail("shouldn't happen")

    @unittest.skipIf(main.__version__ < (1, 3),
                     "not supported in this library version")
    def test_format(self):
        # Tests that work for only a certain version of the library.
        pass

    @unittest.skipUnless(sys.platform.startswith("darwin"), "requires Mac")
    def test_mac_support(self):
        # mac specific testing code
        pass

    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    def test_windows_support(self):
        # windows specific testing code
        pass


class ExpectedFailureTestCase(unittest.TestCase):
    @unittest.expectedFailure
    def test_fail(self):
        self.assertEqual(1, 0, "broken")

    def test_unless_has_attr(self):
        skipUnlessHasattr({"name":"chen"}, "age")

def skipUnlessHasattr(obj, attr):
    """
    如果没有属性的话也不skip任何测试
    :param obj:
    :param attr:
    :return:
    """
    if hasattr(obj, attr):
        return lambda func: func
    return unittest.skip("{!r} doesn't have {!r}".format(obj, attr))
