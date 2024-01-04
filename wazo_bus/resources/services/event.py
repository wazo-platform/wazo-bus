# Copyright 2015-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import ServiceEvent


class ServiceRegisteredEvent(ServiceEvent):
    name = 'service_registered'
    routing_key_fmt = 'service.registered.{service_name}'

    def __init__(
        self,
        service_name: str,
        service_id: str,
        advertise_address: str,
        advertise_port: int,
        tags: list[str],
    ):
        content = {
            'service_name': service_name,
            'service_id': service_id,
            'address': advertise_address,
            'port': advertise_port,
            'tags': tags,
        }
        super().__init__(content)


class ServiceDeregisteredEvent(ServiceEvent):
    name = 'service_deregistered'
    routing_key_fmt = 'service.registered.{service_name}'

    def __init__(self, service_name: str, service_id: str, tags: list[str]):
        content = {
            'service_name': service_name,
            'service_id': service_id,
            'tags': tags,
        }
        super().__init__(content)
