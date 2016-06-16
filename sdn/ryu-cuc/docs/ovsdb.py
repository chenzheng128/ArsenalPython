#!/usr/bin/python
# --*-- coding:utf-8 --*--


import uuid

from ryu.base import app_manager
from ryu.services.protocols.ovsdb import api as ovsdb
from ryu.services.protocols.ovsdb import event as ovsdb_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls


class MyApp(app_manager.RyuApp):
    """
    此代码未运行通过
    """
    @set_ev_cls(ovsdb_event.EventNewOVSDBConnection)
    def handle_new_ovsdb_connection(self, ev):
        system_id = ev.system_id
        self.logger.info('New OVSDB connection from system id %s',
                         system_id)

    def create_port(self, system_id, bridge_name, name):
        new_iface_uuid = uuid.uuid4()
        new_port_uuid = uuid.uuid4()

        def _create_port(tables, insert):
            bridge = ovsdb.row_by_name(self, system_id, bridge_name)

            iface = insert(tables['Interface'], new_iface_uuid)
            iface.name = name
            iface.type = 'internal'

            port = insert(tables['Port'], new_port_uuid)
            port.name = name
            port.interfaces = [iface]

            bridge.ports = bridge.ports + [port]

            return (new_port_uuid, new_iface_uuid)

        req = ovsdb_event.EventModifyRequest(system_id, _create_port)
        rep = self.send_request(req)

        if rep.status != 'success':
            self.logger.error('Error creating port %s on bridge %s: %s',
                              name, bridge, rep.status)
            return None

        return reply.insert_uuid[new_port_uuid]