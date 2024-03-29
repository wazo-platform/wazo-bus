# Copyright 2017-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import ServiceEvent


class ConfBridgeWazoDefaultBridgeEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'confbridge_wazo_default_bridge_edited'
    routing_key_fmt = 'config.confbridge_wazo_default_bridge.edited'

    def __init__(self) -> None:
        super().__init__()


class ConfBridgeWazoDefaultUserEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'confbridge_wazo_default_user_edited'
    routing_key_fmt = 'config.confbridge_wazo_default_user.edited'

    def __init__(self) -> None:
        super().__init__()
