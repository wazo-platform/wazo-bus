# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import ServiceEvent


class ConfBridgeWazoDefaultBridgeEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'confbridge_wazo_default_bridge_edited'
    routing_key_fmt = 'config.confbridge_wazo_default_bridge.edited'

    def __init__(self):
        super(ConfBridgeWazoDefaultBridgeEditedEvent, self).__init__()


class ConfBridgeWazoDefaultUserEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'confbridge_wazo_default_user_edited'
    routing_key_fmt = 'config.confbridge_wazo_default_user.edited'

    def __init__(self):
        super(ConfBridgeWazoDefaultUserEditedEvent, self).__init__()
