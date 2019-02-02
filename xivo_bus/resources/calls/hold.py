# -*- coding: utf-8 -*-
# Copyright (C) 2016 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals


class _BaseHoldEvent(object):

    def __init__(self, call_id, user_uuid=None):
        self._call_id = call_id
        self._user_uuid = user_uuid
        self.required_acl = 'events.calls.{}'.format(user_uuid) if user_uuid else None

    def marshal(self):
        return {'call_id': self._call_id,
                'user_uuid': self._user_uuid}

    @classmethod
    def unmarshal(cls, msg):
        return cls(msg['call_id'], msg['user_uuid'])

    def __eq__(self, other):
        return self.marshal() == other.marshal()

    def __ne__(self, other):
        return not self == other


class CallOnHoldEvent(_BaseHoldEvent):

    name = 'call_held'
    routing_key = 'calls.hold.created'


class CallResumeEvent(_BaseHoldEvent):

    name = 'call_resumed'
    routing_key = 'calls.hold.deleted'
