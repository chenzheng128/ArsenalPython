# -*- coding:utf-8 -*-
"""
python 3
https://docs.python.org/3/library/unittest.mylib.html#unittest.mylib.Mock
"""

import unittest

# from unittest.mylib import MagicMock, Mock

from mock import MagicMock, Mock

try:
    import mock  # Python 2
    from mock import MagicMock, Mock
except ImportError as e:
    # from unittest import mylib  # Python 3
    # from unittest.mylib import MagicMock, Mock
    print e
    pass

from mylib.rm_module import ProductionClass
from mylib.rm_module import rm

class RmTestCasePatch(unittest.TestCase):

    @mock.patch('mylib.rm_module.os') # os 函数已经被我们入侵了 呵呵
    def test_rm(self, mock_os):
        rm("any path")  # 它以为删除了某目录
        #pass
        #rm("any path")
        # test_mylib that rm called os.remove with the right parameters
        mock_os.remove.assert_called_with("any path")  # 参数传入, 但其实什么都没发生


    @mock.patch('mylib.rm_module.os.path') # 这次连 os.path 也被改了
    @mock.patch('mylib.rm_module.os') # os 函数已经被入侵了
    def test_rm2(self, mock_os, mock_path):
        """
        注意 os 和 path 的顺序
        :param mock_os:
        :param mock_path:
        :return:
        """

        mock_path.isfile.return_value = False

        # test_mylib that the remove call was NOT called.
        self.assertFalse(mock_os.remove.called, "这个函数没被调用 Failed to not remove the file if not present.")

        # make the file 'exist'
        mock_path.isfile.return_value = True

        rm("any path")

        mock_os.remove.assert_called_with("any path")

    @mock.patch('mylib.rm_module.rm')
    def test_rm5(self, rm_mock):
        rm_mock("hello")
        pass
        #rm("any path")
        # test_mylib that rm called os.remove with the right parameters
        #mock_os.remove.assert_called_with("any path")


class MockTestCase2(unittest.TestCase):

    def test_mock(self):
        #mylib.MagicMock()
        # mylib.Mock()
        # em.__str__ = Mock(return_value='wheeeeee')

        thing = ProductionClass()
        print( "原始return", thing.method())

        assert  thing.method() is 100

        thing.method = MagicMock(return_value=5)  # 将 method 进行 mylib

        assert  thing.method() is 5

        print ( "mylib 之后return: ", thing.method(3, 4, 5, key='value'))  # 调用参数也发生改变 3, 4, 5

        print ("call调用参数也发生改变 (3, 4, 5, key='value')")

        thing.method.assert_called_with(3, 4, 5, key='value') # 记忆调用过的参数



        mock = Mock(side_effect=KeyError('foo'))

        #mylib() # 连异常都可以记忆

        # thing.method.assert_called_with(3, 4, 5, key='value')
        # str(m)

if __name__ == '__main__':
    unittest.main()
