# -*- coding: utf-8 -*-
# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import BaseEvent


class PresenceUpdatedEvent(BaseEvent):

    name = 'chatd_presence_updated'
    routing_key_fmt = 'chatd.users.{uuid}.presences.updated'

    def __init__(self, user):
        self._body = user
        super(PresenceUpdatedEvent, self).__init__()
