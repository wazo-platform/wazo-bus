# -*- coding: utf-8 -*-
# Copyright 2019-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import ServiceEvent


class HEPGeneralEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'hep_general_edited'
    routing_key_fmt = 'config.hep_general.edited'

    def __init__(self):
        super(HEPGeneralEditedEvent, self).__init__()
