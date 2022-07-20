# -*- coding: utf-8 -*-
# Copyright 2019-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import ServiceEvent


class HAEditedEvent(ServiceEvent):
    name = 'ha_edited'
    routing_key_fmt = 'config.ha.edited'

    def __init__(self):
        super(HAEditedEvent, self).__init__()
