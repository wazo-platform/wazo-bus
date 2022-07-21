# -*- coding: utf-8 -*-
# Copyright 2016-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import ServiceEvent


class SIPGeneralEditedEvent(ServiceEvent):
    name = 'sip_general_edited'
    routing_key_fmt = 'config.sip_general.edited'

    def __init__(self):
        super(SIPGeneralEditedEvent, self).__init__()
