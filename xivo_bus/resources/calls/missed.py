# -*- coding: utf-8 -*-
# Copyright 2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import BaseEvent


class UserMissedCall(BaseEvent):

    name = 'user_missed_call'
    routing_key_fmt = 'calls.missed'

    def __init__(self, body):
        self._body = body
        super(UserMissedCall, self).__init__()
        self.required_acl = 'events.calls.{}'.format(body['user_uuid'])
