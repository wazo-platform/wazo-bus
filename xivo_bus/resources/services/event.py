# -*- coding: utf-8 -*-

# Copyright (C) 2015 Avencall
# Copyright (C) 2016 Proformatique, Inc.
#
# SPDX-License-Identifier: GPL-3.0+


class ServiceRegisteredEvent(object):

    name = 'service_registered_event'
    routing_key_fmt = 'service.registered.{service_name}'

    def __init__(self, service_name, service_id, advertise_address, advertise_port, tags):
        self.routing_key = self.routing_key_fmt.format(service_name=service_name)
        self.service_name = service_name
        self.service_id = service_id
        self.advertise_address = advertise_address
        self.advertise_port = advertise_port
        self.tags = tags

    def marshal(self):
        return {'service_name': self.service_name,
                'service_id': self.service_id,
                'address': self.advertise_address,
                'port': self.advertise_port,
                'tags': self.tags}

    @classmethod
    def unmarshal(cls, body):
        return cls(body['service_name'],
                   body['service_id'],
                   body['address'],
                   body['port'],
                   body['tags'])

    def __eq__(self, other):
        return (self.service_name == other.service_name and
                self.service_id == other.service_id and
                self.advertise_address == other.advertise_address and
                self.advertise_port == other.advertise_port and
                sorted(self.tags) == sorted(other.tags))

    def __ne__(self, other):
        return not self.__eq__(other)


class ServiceDeregisteredEvent(object):

    name = 'service_deregistered_event'
    routing_key_fmt = 'service.deregistered.{service_name}'

    def __init__(self, service_name, service_id, tags):
        self.routing_key = self.routing_key_fmt.format(service_name=service_name)
        self._service_name = service_name
        self._service_id = service_id
        self._tags = tags

    def marshal(self):
        return {'service_name': self._service_name,
                'service_id': self._service_id,
                'tags': self._tags}

    def __eq__(self, other):
        return (self._service_name == other._service_name and
                self._service_id == other._service_id and
                sorted(self._tags) == sorted(other._tags))

    def __ne__(self, other):
        return not self.__eq__(other)
