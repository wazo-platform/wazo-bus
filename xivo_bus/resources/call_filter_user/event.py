# -*- coding: utf-8 -*-
# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals


class CallFilterUserConfigEvent(object):

    def __init__(self, call_filter_id, user_uuids):
        self.call_filter_id = call_filter_id
        self.user_uuids = user_uuids

    def marshal(self):
        return {
            'call_filter_id': self.call_filter_id,
            'user_uuids': self.user_uuids,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['call_filter_id'],
            msg['user_uuids']
        )

    def __eq__(self, other):
        return (self.call_filter_id == other.call_filter_id
                and self.user_uuids == other.user_uuids)

    def __ne__(self, other):
        return not self == other


class CallFilterRecipientUsersAssociatedEvent(CallFilterUserConfigEvent):
    name = 'users_associated'
    routing_key = 'config.callfilters.recipients.users.updated'


class CallFilterSurrogateUsersAssociatedEvent(CallFilterUserConfigEvent):
    name = 'users_associated'
    routing_key = 'config.callfilters.surrogates.users.updated'
