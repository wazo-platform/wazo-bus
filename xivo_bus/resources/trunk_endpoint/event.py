# -*- coding: utf-8 -*-

# Copyright (C) 2016 Avencall
# Copyright (C) 2016 Proformatique Inc.
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

from __future__ import unicode_literals


class TrunkEndpointConfigEvent(object):

    def __init__(self, trunk_id, endpoint_id):
        self.trunk_id = trunk_id
        self.endpoint_id = endpoint_id

    def marshal(self):
        return {
            'trunk_id': self.trunk_id,
            'endpoint_id': self.endpoint_id,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['trunk_id'],
            msg['endpoint_id'])

    def __eq__(self, other):
        return (self.trunk_id == other.trunk_id and
                self.endpoint_id == other.endpoint_id)

    def __ne__(self, other):
        return not self == other


class TrunkEndpointAssociatedEvent(TrunkEndpointConfigEvent):
    name = 'trunk_endpoint_associated'
    routing_key = 'config.trunks.endpoints.updated'


class TrunkEndpointDissociatedEvent(TrunkEndpointConfigEvent):
    name = 'trunk_endpoint_dissociated'
    routing_key = 'config.trunks.endpoints.deleted'
