# -*- coding: utf-8 -*-
# Copyright 2016-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class UserCallPermissionConfigEvent(ResourceConfigEvent):

    def __init__(self, user_uuid, call_permission_id):
        self.user_uuid = user_uuid
        self.call_permission_id = call_permission_id

    def marshal(self):
        return {
            'user_uuid': self.user_uuid,
            'call_permission_id': self.call_permission_id,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['user_uuid'],
            msg['call_permission_id'])

    def __eq__(self, other):
        return (self.user_uuid == other.user_uuid
                and self.call_permission_id == other.call_permission_id)

    def __ne__(self, other):
        return not self == other


class UserCallPermissionAssociatedEvent(UserCallPermissionConfigEvent):
    name = 'call_permission_associated'

    def __init__(self, user_uuid, call_permission_id):
        super(UserCallPermissionAssociatedEvent, self).__init__(user_uuid, call_permission_id)
        self.routing_key = 'config.users.{}.callpermissions.updated'.format(self.user_uuid)
        self.required_acl = 'events.{}'.format(self.routing_key)


class UserCallPermissionDissociatedEvent(UserCallPermissionConfigEvent):
    name = 'call_permission_dissociated'

    def __init__(self, user_uuid, call_permission_id):
        super(UserCallPermissionDissociatedEvent, self).__init__(user_uuid, call_permission_id)
        self.routing_key = 'config.users.{}.callpermissions.deleted'.format(self.user_uuid)
        self.required_acl = 'events.{}'.format(self.routing_key)
