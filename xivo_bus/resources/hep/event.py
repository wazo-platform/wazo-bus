# Copyright 2019-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import ServiceEvent


class HEPGeneralEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'hep_general_edited'
    routing_key_fmt = 'config.hep_general.edited'

    def __init__(self):
        super(HEPGeneralEditedEvent, self).__init__()
