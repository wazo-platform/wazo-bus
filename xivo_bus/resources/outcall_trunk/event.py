# -*- coding: utf-8 -*-
# Copyright (C) 2016 Avencall
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class OutcallTrunkConfigEvent(ResourceConfigEvent):

    def __init__(self, outcall_id, trunk_ids):
        self.outcall_id = outcall_id
        self.trunk_ids = trunk_ids

    def marshal(self):
        return {
            'outcall_id': self.outcall_id,
            'trunk_ids': self.trunk_ids,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['outcall_id'],
            msg['trunk_ids'])

    def __eq__(self, other):
        return (self.outcall_id == other.outcall_id and
                self.trunk_ids == other.trunk_ids)

    def __ne__(self, other):
        return not (self == other)


class OutcallTrunksAssociatedEvent(OutcallTrunkConfigEvent):
    name = 'trunks_associated'
    routing_key = 'config.outcalls.trunks.updated'
