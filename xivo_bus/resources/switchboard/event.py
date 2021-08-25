# -*- coding: utf-8 -*-
# Copyright 2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from ..common.event import BaseEvent


class _BaseSwitchboardEvent(BaseEvent):
    def __init__(self, body):
        self._body = body
        super(_BaseSwitchboardEvent, self).__init__()
        self.required_acl = self.required_acl_fmt.format(**body)


class EditSwitchboardFallbackEvent(_BaseSwitchboardEvent):
    name = 'switchboard_fallback_edited'
    routing_key_fmt = 'config.switchboards.fallbacks.edited'
    required_acl_fmt = 'switchboards.fallbacks.edited'
