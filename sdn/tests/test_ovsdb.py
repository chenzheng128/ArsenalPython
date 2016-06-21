#!/usr/bin/python
# --*-- coding:utf-8 --*--

try:
    import mock  # Python 2
except ImportError:
    from unittest import mock  # Python 3

import json
import os
import sys
import warnings
import unittest
import logging
import random

from sdn.myovsdb import ovsdb_client

LOG = logging.getLogger('test_ovsdb')


class test_ovsdb_client(unittest.TestCase):
    def test_get_reposne(self):
        self.assertEqual(ovsdb_client.get_resposne() ,'{"id":0,"result":["Open_vSwitch"],"error":null}')
