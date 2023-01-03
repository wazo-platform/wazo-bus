# Copyright 2018-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import ServiceEvent


class QueueGeneralEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'queue_general_edited'
    routing_key_fmt = 'config.queue_general.edited'

    def __init__(self):
        super(QueueGeneralEditedEvent, self).__init__()
