# -*- coding: utf-8 -*-
# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class GroupCallPermissionConfigEvent(ResourceConfigEvent):

    def __init__(self, group_id, call_permission_id):
        self.group_id = group_id
        self.call_permission_id = call_permission_id

    def marshal(self):
        return {
            'group_id': self.group_id,
            'call_permission_id': self.call_permission_id,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['group_id'],
            msg['call_permission_id'])

    def __eq__(self, other):
        return (self.group_id == other.group_id
                and self.call_permission_id == other.call_permission_id)

    def __ne__(self, other):
        return not self == other


class GroupCallPermissionAssociatedEvent(GroupCallPermissionConfigEvent):
    name = 'call_permission_associated'

    def __init__(self, group_id, call_permission_id):
        super(GroupCallPermissionAssociatedEvent, self).__init__(group_id, call_permission_id)
        self.routing_key = 'config.groups.{}.callpermissions.updated'.format(self.group_id)
        self.required_acl = 'events.{}'.format(self.routing_key)


class GroupCallPermissionDissociatedEvent(GroupCallPermissionConfigEvent):
    name = 'call_permission_dissociated'

    def __init__(self, group_id, call_permission_id):
        super(GroupCallPermissionDissociatedEvent, self).__init__(group_id, call_permission_id)
        self.routing_key = 'config.groups.{}.callpermissions.deleted'.format(self.group_id)
        self.required_acl = 'events.{}'.format(self.routing_key)
