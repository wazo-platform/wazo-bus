# -*- coding: utf-8 -*-
# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals


class CallPickupUserConfigEvent(object):

    def __init__(self, call_pickup_id, user_uuids):
        self.call_pickup_id = call_pickup_id
        self.user_uuids = user_uuids

    def marshal(self):
        return {
            'call_pickup_id': self.call_pickup_id,
            'user_uuids': self.user_uuids,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['call_pickup_id'],
            msg['user_uuids']
        )

    def __eq__(self, other):
        return (
            self.call_pickup_id == other.call_pickup_id
            and self.user_uuids == other.user_uuids,
        )

    def __ne__(self, other):
        return not self == other


class CallPickupInterceptorUsersAssociatedEvent(CallPickupUserConfigEvent):
    name = 'users_associated'
    routing_key = 'config.callpickups.interceptors.users.updated'


class CallPickupTargetUsersAssociatedEvent(CallPickupUserConfigEvent):
    name = 'users_associated'
    routing_key = 'config.callpickups.targets.users.updated'


class CallPickupGroupConfigEvent(object):

    def __init__(self, call_pickup_id, group_ids):
        self.call_pickup_id = call_pickup_id
        self.group_ids = group_ids

    def marshal(self):
        return {
            'call_pickup_id': self.call_pickup_id,
            'group_ids': self.group_ids,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['call_pickup_id'],
            msg['group_ids']
        )

    def __eq__(self, other):
        return (
            self.call_pickup_id == other.call_pickup_id
            and self.group_ids == other.group_ids,
        )

    def __ne__(self, other):
        return not self == other


class CallPickupInterceptorGroupsAssociatedEvent(CallPickupGroupConfigEvent):
    name = 'groups_associated'
    routing_key = 'config.callpickups.interceptors.groups.updated'


class CallPickupTargetGroupsAssociatedEvent(CallPickupGroupConfigEvent):
    name = 'groups_associated'
    routing_key = 'config.callpickups.targets.groups.updated'
