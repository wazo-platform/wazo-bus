# -*- coding: utf-8 -*-

# Copyright (C) 2013-2016 Avencall
#
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class ConfigurationEvent(ResourceConfigEvent):

    @classmethod
    def unmarshal(cls, msg):
        return cls(msg['live_reload_enabled'])


class LiveReloadEditedEvent(ConfigurationEvent):
    name = 'live_reload_edited'
    routing_key = 'config.live_reload.edited'

    def __init__(self, live_reload_enabled):
        self.live_reload_enabled = live_reload_enabled

    def marshal(self):
        return {
            'live_reload_enabled': self.live_reload_enabled
        }

    def __eq__(self, other):
        return self.live_reload_enabled == other.live_reload_enabled

    def __ne__(self, other):
        return not self == other
