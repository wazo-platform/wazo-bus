# Copyright 2016-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import ServiceEvent


class SIPGeneralEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'sip_general_edited'
    routing_key_fmt = 'config.sip_general.edited'

    def __init__(self):
        super().__init__()
