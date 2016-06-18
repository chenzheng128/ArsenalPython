# zhchen revised from ryu.testsunit.cmd.test_manager.py

# Copyright (C) 2013,2014 Nippon Telegraph and Telephone Corporation.
# Copyright (C) 2013,2014 YAMAMOTO Takashi <yamamoto at valinux co jp>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import unittest
import mock
from nose.tools import eq_, raises

try:
    # Python 3
    from imp import reload
except ImportError:
    # Python 2
    pass

from ryu.cmd.manager import main
#from cuc.docs import l2


class Test_Manager(unittest.TestCase):
    """Test ryu-manager command
    """

    def __init__(self, methodName):
        super(Test_Manager, self).__init__(methodName)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    #@raises(SystemExit)
    #@mylib.patch('sys.argv', new=['ryu-manager', 'ryu.app.simple_switch'])
    #def test_simple_switch(self):
    #    main()

    #@raises(SystemExit)
    @mock.patch('sys.argv', new=['ryu-manager', 'cuc.docs.l2'])
    def test_l2_switch(self):
        pass
        #raises(SystemExit("exit"))
        #main()


    @raises(SystemExit)
    @mock.patch('sys.argv', new=['ryu-manager', '--version'])
    def test_version(self):
        main()

    @raises(SystemExit)
    @mock.patch('sys.argv', new=['ryu-manager', '--help'])
    def test_help(self):
        main()

    @staticmethod
    def _reset_globals():
        # hack to reset globals like SERVICE_BRICKS.
        # assumption: this is the only test_mylib which actually starts RyuApp.
        import ryu.base.app_manager
        import ryu.ofproto.ofproto_protocol

        reload(ryu.base.app_manager)
        reload(ryu.ofproto.ofproto_protocol)

    @mock.patch('sys.argv', new=['ryu-manager', '--verbose',
                                 'ryu.tests.unit.cmd.dummy_app'])
    def test_no_services(self):
        self._reset_globals()
        main()
        self._reset_globals()

    @mock.patch('sys.argv', new=['ryu-manager', '--verbose',
                                 'ryu.tests.unit.cmd.dummy_openflow_app'])
    def test_openflow_app(self):
        self._reset_globals()
        main()
        self._reset_globals()
