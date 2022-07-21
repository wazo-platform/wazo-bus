# -*- coding: utf-8 -*-
# Copyright 2018-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import ServiceEvent


class QueueGeneralEditedEvent(ServiceEvent):
    name = 'queue_general_edited'
    routing_key_fmt = 'config.queue_general.edited'

    def __init__(self):
        super(QueueGeneralEditedEvent, self).__init__()
