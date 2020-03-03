# -*- coding: utf-8 -*-
# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from ..common.event import BaseEvent


class PJSIPGlobalUpdatedEvent(BaseEvent):

    name = 'pjsip_global_updated'
    routing_key_fmt = 'config.pjsip_global.updated'

    def __init__(self):
        self._body = {}
        super(PJSIPGlobalUpdatedEvent, self).__init__()


class PJSIPSystemUpdatedEvent(BaseEvent):

    name = 'pjsip_system_updated'
    routing_key_fmt = 'config.pjsip_system.updated'

    def __init__(self):
        self._body = {}
        super(PJSIPSystemUpdatedEvent, self).__init__()
