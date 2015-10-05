# -*- coding: utf-8 -*-

# Copyright (C) 2015 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>


class ServiceRegisteredEvent(object):

    name = 'service_registered_event'
    routing_key_fmt = 'service.registered.{service_name}'

    def __init__(self, service_name, service_id, advertise_address, advertise_port, tags):
        self.routing_key = self.routing_key_fmt.format(service_name=service_name)
        self._service_name = service_name
        self._service_id = service_id
        self._advertise_address = advertise_address
        self._advertise_port = advertise_port
        self._tags = tags

    def marshal(self):
        return {'service_name': self._service_name,
                'service_id': self._service_id,
                'address': self._advertise_address,
                'port': self._advertise_port,
                'tags': self._tags}


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
