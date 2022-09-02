# -*- coding: utf-8 -*-
# Copyright 2013-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import ServiceEvent


class LiveReloadEditedEvent(ServiceEvent):
    name = 'live_reload_edited'
    routing_key_fmt = 'config.live_reload.edited'

    def __init__(self, live_reload_enabled):
        content = {'live_reload_enabled': live_reload_enabled}
        super(LiveReloadEditedEvent, self).__init__(content)
