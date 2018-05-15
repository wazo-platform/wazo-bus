# -*- coding: utf-8 -*-
# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class OutcallCallPermissionConfigEvent(ResourceConfigEvent):

    def __init__(self, outcall_id, call_permission_id):
        self.outcall_id = outcall_id
        self.call_permission_id = call_permission_id

    def marshal(self):
        return {
            'outcall_id': self.outcall_id,
            'call_permission_id': self.call_permission_id,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['outcall_id'],
            msg['call_permission_id'])

    def __eq__(self, other):
        return (self.outcall_id == other.outcall_id
                and self.call_permission_id == other.call_permission_id)

    def __ne__(self, other):
        return not self == other


class OutcallCallPermissionAssociatedEvent(OutcallCallPermissionConfigEvent):
    name = 'call_permission_associated'

    def __init__(self, outcall_id, call_permission_id):
        super(OutcallCallPermissionAssociatedEvent, self).__init__(outcall_id, call_permission_id)
        self.routing_key = 'config.outcalls.{}.callpermissions.updated'.format(self.outcall_id)
        self.required_acl = 'events.{}'.format(self.routing_key)


class OutcallCallPermissionDissociatedEvent(OutcallCallPermissionConfigEvent):
    name = 'call_permission_dissociated'

    def __init__(self, outcall_id, call_permission_id):
        super(OutcallCallPermissionDissociatedEvent, self).__init__(outcall_id, call_permission_id)
        self.routing_key = 'config.outcalls.{}.callpermissions.deleted'.format(self.outcall_id)
        self.required_acl = 'events.{}'.format(self.routing_key)
