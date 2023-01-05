# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import ServiceEvent


class IAXCallNumberLimitsEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'iax_callnumberlimits_edited'
    routing_key_fmt = 'config.iax_callnumberlimits.edited'

    def __init__(self):
        super().__init__()
