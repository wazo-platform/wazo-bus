# -*- coding: utf-8 -*-
# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals


class CallDTMFEvent(object):

    name = 'call_dtmf_created'
    routing_key = 'calls.dtmf.created'

    def __init__(self, call_id, digit, user_uuid=None):
        self._call_id = call_id
        self._digit = digit
        self._user_uuid = user_uuid
        self.required_acl = 'events.calls.{}'.format(user_uuid) if user_uuid else None

    def marshal(self):
        return {'call_id': self._call_id,
                'digit': self._digit,
                'user_uuid': self._user_uuid}

    @classmethod
    def unmarshal(cls, msg):
        return cls(msg['call_id'], msg['digit'], msg['user_uuid'])

    def __eq__(self, other):
        return self.marshal() == other.marshal()

    def __ne__(self, other):
        return not self == other
