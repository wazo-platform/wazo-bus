# -*- coding: utf-8 -*-
# Copyright (C) 2016 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class CustomEndpointConfigEvent(ResourceConfigEvent):

    def __init__(self, custom_id, interface):
        self.id = int(custom_id)
        self.interface = interface

    def marshal(self):
        return {
            'id': self.id,
            'interface': self.interface,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(msg['id'], msg['interface'])


class EditCustomEndpointEvent(CustomEndpointConfigEvent):
    name = 'custom_endpoint_edited'
    routing_key = 'config.custom_endpoint.edited'


class CreateCustomEndpointEvent(CustomEndpointConfigEvent):
    name = 'custom_endpoint_created'
    routing_key = 'config.custom_endpoint.created'


class DeleteCustomEndpointEvent(CustomEndpointConfigEvent):
    name = 'custom_endpoint_deleted'
    routing_key = 'config.custom_endpoint.deleted'
