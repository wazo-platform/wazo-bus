# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals


class _ConfBridgeConfigurationEvent(object):
    def marshal(self):
        return {}

    @classmethod
    def unmarshal(cls, msg):
        return cls()

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self == other


class EditConfBridgeDefaultBridgeEvent(_ConfBridgeConfigurationEvent):
    name = 'confbridge_default_bridge_edited'
    routing_key = 'config.confbridge_default_bridge.edited'


class EditConfBridgeDefaultUserEvent(_ConfBridgeConfigurationEvent):
    name = 'confbridge_default_user_edited'
    routing_key = 'config.confbridge_default_user.edited'
