# -*- coding: utf-8 -*-
# Copyright 2015-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import ServiceEvent


class ServiceRegisteredEvent(ServiceEvent):
    name = 'service_registered'
    routing_key_fmt = 'service.registered.{service_name}'

    def __init__(
        self, service_name, service_id, advertise_address, advertise_port, tags
    ):
        content = {
            'service_name': service_name,
            'service_id': service_id,
            'address': advertise_address,
            'port': advertise_port,
            'targs': tags,
        }
        super(ServiceRegisteredEvent, self).__init__(content)


class ServiceDeregisteredEvent(ServiceEvent):
    name = 'service_deregistered'
    routing_key_fmt = 'service.registered.{service_name}'

    def __init__(self, service_name, service_id, tags):
        content = {
            'service_name': service_name,
            'service_id': service_id,
            'tags': tags,
        }
        super(ServiceDeregisteredEvent, self).__init__(content)
