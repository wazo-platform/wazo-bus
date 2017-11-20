# -*- coding: utf-8 -*-
# Copyright (C) 2016 Avencall
# Copyright (C) 2016 Proformatique Inc.
# SPDX-License-Identifier: GPL-3.0+

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
