#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
用 mock 替换, 不用真正发生 mock 操作
"""

import unittest

import mock

import mylib.req_module

from requests import Response


class ReqPatchTestCase(unittest.TestCase):

    @mock.patch('mylib.req_module.send_request')
    def test_req(self, req_mock):
        """
        mock patch 之后 传入的对象, 可以设置返回值等各种东西
        :param req_mock:
        :return:
        """
        req_mock.return_value = 404
        req_mock(1, 4, 7)
        self.assertEqual( mylib.req_module.visit_ustack(), 404)
        #req_mock.assert_called_with(1, 4, 7)
        #rm_mock("hello")
        #pass
        #rm("any path")
        # test_mylib that rm called os.remove with the right parameters
        #mock_os.remove.assert_called_with("any path")

    @mock.patch('mylib.req_module.requests')
    def test_req2(self, req_mock):
        r = Response()
        r.status_code = 200
        req_mock.get.return_value = r
        self.assertEqual(mylib.req_module.send_request("url"), 200)
        #req_mock.return_value


class ReqTestCase(unittest.TestCase):
    def test_success_request(self):
        success_send = mock.Mock(return_value='200')
        mylib.req_module.send_request = success_send
        self.assertEqual(mylib.req_module.visit_ustack(), '200')

    def test_fail_request(self):
        fail_send = mock.Mock(return_value='404')
        mylib.req_module.send_request = fail_send
        self.assertEqual(mylib.req_module.visit_ustack(), '404')
